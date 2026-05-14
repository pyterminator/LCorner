import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 

USERNAME_PATTERN = r"^[a-z]+$"

EMAIL_PATTERN = (
    r"^[A-Za-z0-9](?:[A-Za-z0-9._-]{1,}[A-Za-z0-9])?"
    r"@[A-Za-z0-9](?:[A-Za-z0-9-]{0,}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z]{2,})+$"
)

PASSWORD_PATTERN = (
    r"^(?=.*[A-ZÜŞÇİĞÖƏ])"
    r"(?=.*[a-züçşıəöğ])"
    r"(?=.*\d)"
    r"(?=.*\.)"
    r"[A-Za-z0-9.üçşıəöğÜŞÇİĞÖƏ]{8,}$"
)





def MemberLogin(request):
    # Login olubsa dashboarda qaytar
    if request.user.is_authenticated:
        return redirect("dashboard")

    data = dict()

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(
            request=request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        data["wrong_username_or_password"] = "İstifadəçi adı və ya şifrə yanlışdır!"
        

    return render(request, 'login.html', context=data)

def MemberRegistration(request):
    # Login olubsa dashboarda qaytar
    if request.user.is_authenticated:
        return redirect("dashboard")
    
    data = {}

    if request.method == "POST":
        invalid_data = False

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        repassword = request.POST.get("repassword", "").strip()

        data["username"] = username 
        data["email"] = email

        # Username
        if not re.match(USERNAME_PATTERN, username):
            invalid_data = True
            data["username_abc"] = "İstifadəçi adında yalnız ingiliscə kiçik hərflər ola bilər!"
        if len(username) < 3:
            invalid_data = True
            data["username_abc"] = "İstifadəçi adı minimum 3 simvoldan ibarət olmalıdır!"

        # Email
        if not (re.match(EMAIL_PATTERN, email) and isinstance(email, str)):
            invalid_data = True
            data["fake_email"] = "Email formatı doğru deyil!"

        # Password / RePassword 
        if not re.match(PASSWORD_PATTERN, password):
            invalid_data = True
            data['invalid_password'] = "Şifrə minimum 8 simvol olmalı, kiçik/böyük hərf, rəqəm və nöqtədən ibarət olmalıdır."
        if repassword != password:
            invalid_data = True
            data["dontmatch"] = "Şifrə və Təkrar Şifrə uyğun gəlmir."

        if not invalid_data: 
            
            new_user = User.objects.create_user(
                username=username,
                email=email
            )

            new_user.set_password(password)
            new_user.save()
            
            return redirect('login')
        

    return render(request, "register.html", context=data)

@login_required
def MemberLogout(request):
    logout(request)
    return redirect("login")



@login_required
def Account(request, username):
    user = User.objects.filter(username=username).first()

    if user:
        data = {
            "user":user
        }
        return render(request, "dashboard/account.html", context=data)
    
    return redirect("dashboard")

@login_required
def ChangeMyPassword(request):
    data = {
        "errors": []
    }
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        password = request.POST.get("password")
        repassword = request.POST.get("repassword")
        
        
        if not request.user.check_password(old_password):
            data["errors"].append("Şifrə yanlışdır!")

        elif password != repassword:
            data["errors"].append("Yeni şifrə və təkrarı fərqlidir!")

        elif not re.match(PASSWORD_PATTERN, password):
            data["errors"].append(
                "Şifrə minimum 8 simvol olmalı, kiçik/böyük hərf, rəqəm və nöqtədən ibarət olmalıdır."
            )

        else:
            request.user.set_password(password)
            request.user.save()

            update_session_auth_hash(request, request.user)

            return redirect(
                "myaccount",
                username=request.user.username
            )

    return render(request, "dashboard/change-my-password.html", context=data)


def Contact(request):
    return render(request, "contact.html")


