from django.shortcuts import render


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

    return render(request, "accounts/login.html")
