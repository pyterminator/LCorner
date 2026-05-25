import re
import os  
import json
from PIL import Image
from post.models import Post
from django.db.models import F
from string import ascii_letters
from django.conf import settings
from member.models import Account
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect 
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash


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
        if not re.match(settings.USERNAME_PATTERN, username):
            invalid_data = True
            data["username_abc"] = "İstifadəçi adında yalnız ingiliscə kiçik hərflər ola bilər!"
        if len(username) < 3:
            invalid_data = True
            data["username_abc"] = "İstifadəçi adı minimum 3 simvoldan ibarət olmalıdır!"

        # Email
        if not (re.match(settings.EMAIL_PATTERN, email) and isinstance(email, str)):
            invalid_data = True
            data["fake_email"] = "Email formatı doğru deyil!"

        # Password / RePassword 
        if not re.match(settings.PASSWORD_PATTERN, password):
            invalid_data = True
            data['invalid_password'] = "Şifrə minimum 8 simvol olmalı, kiçik/böyük hərf, rəqəm və nöqtədən ibarət olmalıdır!"
        if repassword != password:
            invalid_data = True
            data["dontmatch"] = "Şifrə və Təkrar Şifrə uyğun gəlmir!"

        if User.objects.filter(username=username).first() or User.objects.filter(email=email).first():
            invalid_data = True 
            data["username_abc"] = "İstifadəçi adı və ya email artıq istifadə edilir!"

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
def UserAccount(request, username):
    user = User.objects.filter(username=username).first()

    if user:
        user_account = Account.objects.filter(user=user).first()
        if user_account:
            posts = Post.objects.filter(author=user_account).all()
            post_count = posts.count()
            data = {
                "account":user_account,
                "posts":posts,
                "post_count": post_count,
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

        elif not re.match(settings.PASSWORD_PATTERN, password):
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

@login_required
def ChangeMyAvatar(request):
    if request.method == "POST":

        avatar = request.FILES.get("avatar")
        if not avatar:
            return JsonResponse({"success": False, "error": "Fayl yoxdur"})

        if not avatar.content_type.startswith("image/"):
            return JsonResponse({"success": False, "error": "Şəkil deyil"})
        
        if avatar.size > 1 * 1024 * 1024:
            return JsonResponse({
                "success": False,
                "error": "Şəklin həcmi maksiumum 1Mb ola bilər"
            })

        try:
            img = Image.open(avatar)
            width, height = img.size
            print(width, height)

            if width != height or width != 250:
                return JsonResponse({
                    "success": False,
                    "error": "Şəkil (250x250)px ölçüdə olmalıdır"
                })


            account = Account.objects.filter(user=request.user).first()
            if not account:
                return JsonResponse({
                    "success":False,
                    "error":"Yanlış cəhd, hesabınıza daxil olun"
                })
            
            if account.xp < 500 and not account.user.is_superuser:
                return JsonResponse({
                    "success":False,
                    "error":"Şəkli dəyişmək üçün balansınızda minimum 500 xp olmalıdır"
                })

            if account.avatar: 
                old_avatar_path = account.avatar.path 
                if os.path.isfile(old_avatar_path):
                    os.remove(old_avatar_path)

            account.xp = F("xp") - 500
            account.avatar = avatar  
            account.save(update_fields=["xp", "avatar"]) 
            account.refresh_from_db()
        except: 
            return JsonResponse({
                "success":False,
                "error":"Xəta oldu"
            })
        else:
            return JsonResponse({
                "success":True
            })
    
    return JsonResponse({
        "success":False,
        "error":"İcazəsiz cəhd"
    })

@login_required
def DeleteMyAvatar(request):
    if request.method == "POST": 
        try:
            account = Account.objects.filter(user=request.user).first()
            if not account:
                return JsonResponse({
                    "success":False
                })
            

            if account.avatar: 
                old_avatar_path = account.avatar.path 
                if os.path.isfile(old_avatar_path):
                    os.remove(old_avatar_path)


            account.avatar = None 
            account.save()
            
        except: 
            return JsonResponse({
                "success":False
            })
        else:
            return JsonResponse({
                "success":True
            })
    
    return JsonResponse({
        "success":False
    })

@user_passes_test(lambda u: u.is_superuser)
def AccountList(request):
    accounts = Account.objects.all()

    data = {
        "accounts": accounts
    }

    return render(request, "dashboard/users.html", context=data)

@login_required
def UpdateBaseData(request):
    
    if request.method != "POST": return JsonResponse({"success":False, "error":"Yanlış cəhd!"})

    try:
        user = get_object_or_404(User, id=request.user.id)
        account = get_object_or_404(Account, user=request.user.id)
        data = json.loads(request.body)

        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
        profession = data.get("profession", "")

        # Ad yoxlanışı
        if len(first_name) == 0:
            return JsonResponse({
                "success":False,
                "f_n":"Adınızı daxil edin"
            })
    
        if len(first_name) < 3:
            return JsonResponse({
                "success":False,
                "f_n":"Ad minimum 3 simvol olmalıdır"
            })
        
        if len(first_name) > 15:
            return JsonResponse({
                "success":False,
                "f_n":"Ad maksimum 15 simvol ola bilər"
            })
        
        if first_name[0] != first_name[0].upper():
            return JsonResponse({
                "success":False,
                "f_n":"Adın birinci hərfini böyük hərf daxil edin"
            })


        for letter in first_name:
            if letter not in f"{ascii_letters}ÜüŞşÇçƏəİıĞğÖö":
                return JsonResponse({
                    "success":False,
                    "f_n":"Adın tərkibində yalnız hərf olmalıdır"
                })
         

        # Soyad yoxlanışı
        if len(last_name) == 0:
            return JsonResponse({
                "success":False,
                "l_n":"Soyadınızı daxil edin"
            })
    
        if len(last_name) < 3:
            return JsonResponse({
                "success":False,
                "l_n":"Soyad minimum 3 simvol olmalıdır"
            })
        
        if len(last_name) > 15:
            return JsonResponse({
                "success":False,
                "l_n":"Soyad maksimum 15 simvol ola bilər"
            })
        
        if last_name[0] != last_name[0].upper():
            return JsonResponse({
                "success":False,
                "l_n":"Soyadın birinci hərfini böyük hərf daxil edin"
            })


        for letter in last_name:
            if letter not in f"{ascii_letters}ÜüŞşÇçƏəİıĞğÖö":
                return JsonResponse({
                    "success":False,
                    "l_n":"Soyadın tərkibində yalnız hərf olmalıdır"
                })
         
        
        
        # İxtisas yoxlanışı
        if len(profession) < 5 or (len(profession) > 100):
            return JsonResponse({
                "success":False,
                "p_":"İxtisas minimum 5, maksimum 100 simvoldan ibarət ola bilər!"
            })
        
        for letter in profession:
            if letter not in f"{ascii_letters}ÜüŞşÇçƏəİıĞğÖö.,!™- ":
                return JsonResponse({
                    "success":False,
                    "p_":"İxtisas üçün icazə verilən simvollar : Azərbaycan hərfləri, [.,!-™]"
                })
        
        user.first_name = first_name.title()
        user.last_name = last_name.title()
        user.save()

        account.profession = profession
        account.save()

        return JsonResponse({
            "success": True,
            "data":{
                "first_name": first_name.title(),
                "last_name": last_name.title(),
                "profession": profession
            }
        })


    except Exception as e:
        return JsonResponse({
            "success": False,
            "error":f"{e}"
        })

