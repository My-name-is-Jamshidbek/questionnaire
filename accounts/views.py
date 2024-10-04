import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponseServerError
from .models import CustomUser
from django.conf import settings  # Import settings to access API_URL


# Define your API URL constants
API_URL = settings.API_URL
LOGIN_URL = f"{API_URL}/auth/login"
ME_URL = f"{API_URL}/account/me"


def login(request):
    """
    Handle user login by authenticating via external API and creating/updating
    the user in the local database with the hemis_token and fullname.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Validate form data
        if not username or not password:
            messages.error(request, "Both username and password are required.")
            return render(request, "accounts/login.html")

        # Step 1: Authenticate with the external API
        token = authenticate_with_external_api(username, password)
        if not token:
            messages.error(request, "Invalid credentials or external login failed.")
            return render(request, "accounts/login.html")

        # Step 2: Fetch user details (fullname) using the token
        fullname = fetch_user_details(token)
        if not fullname:
            messages.error(request, "Unable to fetch user details from external API.")
            return render(request, "accounts/login.html")

        # Step 3: Create or update the local user
        user = create_or_update_local_user(username, fullname, token, password)

        # Step 4: Log in the user and set the session
        auth_login(request, user)
        return redirect('home')  # Redirect to the homepage or another view after login

    return render(request, "accounts/login.html")


def authenticate_with_external_api(username, password):
    """
    Authenticate the user with the external API and return the token if successful.
    """
    # try:
    response = requests.post(LOGIN_URL, json={"login": username, "password": password})
    # response_data = response.json()
    print(LOGIN_URL)
    # if response_data.get("success") and response_data["data"].get("token"):
    #     return response_data["data"]["token"]
    # return None

    # except requests.RequestException as e:
    #     # Log the error if you are using a logger
    #     print(e)
    #     return None
    # except Exception as e:
    #     print(e)


def fetch_user_details(token):
    """
    Fetch user details from the external API using the provided token.
    Returns the fullname if successful, otherwise returns None.
    """
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(ME_URL, headers=headers)
        me_data = response.json()

        if me_data.get("success") and me_data["data"].get("full_name"):
            return me_data["data"]["full_name"]
        return None

    except requests.RequestException:
        return None


def create_or_update_local_user(username, fullname, hemis_token, password):
    """
    Create or update the local user in the database with the given data.
    If the user already exists, update the fullname and hemis_token.
    """
    user, created = CustomUser.objects.get_or_create(username=username)

    # Update user fields
    user.fullname = fullname
    user.hemis_token = hemis_token

    # Only set the password if creating a new user
    if created:
        user.set_password(password)

    user.save()
    return user
