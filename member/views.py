import re
import os  
import json
import time
from PIL import Image
from post.models import Post
from django.db.models import F
from string import ascii_letters
from django.conf import settings
from member.models import Account
from django.http import JsonResponse
from django.utils.html import strip_tags
from django.utils.timezone import localtime
from django.contrib.auth.models import User
from notifications.models import Notification
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

    ref_code = request.GET.get("ref", None)
    
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
        if len(username) > 12:
            invalid_data = True
            data["username_abc"] = "İstifadəçi adı maksimum 12 simvoldan ibarət ola bilər!"

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

            account = new_user.account
            if ref_code:
                try:
                    ref_user = Account.objects.get(referral_code=ref_code)
                    account.referred_by = ref_user
                    account.save()

                    ref_user.add_xp(50)

                    Notification.objects.create(
                        title="Uğurlu dəvət",
                        account=ref_user,
                        actor=new_user,
                        type="SYSTEM",
                        message=f"Dəvətinlə yeni istifadəçi qeydiyyatdan keçdiyi üçün sistem balansına 50xp əlavə etdi."
                    )

                except: ...

            return redirect('login')

    if ref_code:
        session_key = f"ref_xp_{ref_code}"
        last_time = request.session.get(session_key)

        one_month = 60 * 60 * 24 * 30

        if not last_time or (time.time() - last_time) > one_month:
            try:
                ref_user = Account.objects.get(referral_code=ref_code)

                ref_user.add_xp(5)

                Notification.objects.create(
                    title="Referans linkdən",
                    account=ref_user,
                    type="SYSTEM",
                    message="Referans linkə klik gəldiyi üçün balansına 5xp əlavə edildi."
                )

                request.session[session_key] = time.time()

            except Account.DoesNotExist:
                pass


    return render(request, "register.html", context=data)

@login_required
def MemberLogout(request):
    logout(request)
    return redirect("login")


def GetUserPosts(request, user, page=1):
    try: 
        account = user.account

        # Sehifeye gelen user
        my_account = Account.objects.filter(user=request.user).first()

        # Sehifeni acan userin beyendikleri
        liked_posts = set(
            my_account.likes.values_list("post_id", flat=True)
        )


        my_query = Post.objects.filter(author=account).all().order_by("-id") 
        post_count = my_query.count()
        page_count = (post_count // 10)+ 1
        pagination_data = page

        if pagination_data > page_count or pagination_data < 0:
            pagination_data = 1
        
        if pagination_data == page_count:
            next_page = pagination_data
        else:
            next_page = pagination_data+1
        

        sdmax = pagination_data * 10
        sdmin = (pagination_data - 1) * 10

        if (sdmax - post_count) < 10 and sdmax > post_count: sdmax = post_count

        data = {
            "account": account,
            "posts": my_query.order_by("-id")[sdmin:sdmax],
            "post_count": post_count,
            "liked_posts": liked_posts,
            "my_likes": Post.objects.filter(likes_set__account=my_account).order_by("-id")[:10],
            "next_page":next_page,
            "showing": sdmax
        }

        return data

    except:
        return None


@login_required
def GetPostsAjax(request):
    try:
        page = int(request.GET.get("page", 0))

        username = request.GET.get("username", None)

        if (not page) or (not username):
            return JsonResponse({
                "success": False
            })
 
        user = User.objects.filter(username=username).first()

        data = GetUserPosts(request, user, page) 

        posts = data.get("posts").values(
            "id",
            "author",
            "lang",
            "sentence",
            "description",
            "slug",
            "likes",
            "view",
            "is_public",
            "created_at",
            "updated_at",
            "approved",
        )

 

        return JsonResponse({
            "success":True,
            "posts": list(posts),
            "next_page": data.get("next_page"),
            "showing":data.get("showing"),
            "liked_posts": list(data.get("liked_posts")),
            "post_count":data.get("post_count")
        })
    except:
        return JsonResponse({"success":False})


@login_required
def UserAccount(request, username):
    user = User.objects.filter(username=username).first()
    if not user: return redirect("dashboard")

    
    data = GetUserPosts(request, user)
 
    if request.user == user: 
        return render(request, "dashboard/account.html", context=data)
    
    return render(request, "public_account.html", context=data)

        
    
    

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
            if not account.user.is_superuser:
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
                "success":True,
                "new_xp": account.xp
            })
    
    return JsonResponse({
        "success":False,
        "error":"İcazəsiz cəhd"
    })

# Boshdadir
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

@login_required
def SaveBioData(request):

    if request.method != "POST": return JsonResponse({"success":False, "error":"Yanlış cəhd!"})

    try:
        account = get_object_or_404(Account, user=request.user.id)
        data = json.loads(request.body)

        bio = strip_tags(data.get("bio", ""))

        if len(bio) == 0 or bio == "":
            return JsonResponse({"success":False, "error":"Bioqrafiya mətni daxil edin"})


        if bio and len(bio) < 10:
            return JsonResponse({"success":False, "error":"Bioqrafiya mətni minimum 10 simvoldan ibarət olmalıdır"})
        
        if bio and len(bio) > 150:
            return JsonResponse({"success":False, "error":"Bioqrafiya mətni maksimum 150 simvoldan ibarət ola bilər"})
        
        if not re.match(settings.BIO_PATTERN, bio):
            return JsonResponse({"success":False, "error":"Bioqrafiyada icazə verilməyən simvollar var"})

        account.bio = bio 
        account.save()

        return JsonResponse({
            "success": True,
            "bio":bio
        })

    except Exception as e:
        return JsonResponse({"success":False, "error":f"{e}"})


@login_required
def ChangeUsername(request):

    if request.method != "POST": return JsonResponse({"success":False, "error":"Yanlış cəhd!"})

    try:
        account = get_object_or_404(Account, user=request.user.id)
        data = json.loads(request.body)

        u_name = strip_tags(data.get("username", ""))

        if len(u_name) == 0 or u_name == "":
            return JsonResponse({"success":False, "error":"İstifadəçi adı daxil edin"})


        if u_name and len(u_name) < 3:
            return JsonResponse({"success":False, "error":"İstifadəçi adı minimum 3 simvoldan ibarət olmalıdır"})
        
        if u_name and len(u_name) > 12:
            return JsonResponse({"success":False, "error":"İstifadəçi adı maksimum 12 simvoldan ibarət ola bilər"})
        
        if not re.match(settings.USERNAME_PATTERN, u_name):
            return JsonResponse({"success":False, "error": "İstifadəçi adında yalnız ingiliscə kiçik hərflər ola bilər"}) 
        
        if request.user.username == u_name:
            return JsonResponse({"success":False, "error":"Hazırda istifadə edilən istifadəçi adıdır"})

        if not request.user.is_superuser:
            if account.xp < 200:
                return JsonResponse({"success":False, "error":"İstifadəçi adını dəyişmək üçün 200 xal lazımdır"})



        if User.objects.filter(username=u_name).first():
            return JsonResponse({"success":False, "error":"İstifadəçi adı artıq istifadə edilir"}) 

        account.user.username = u_name 
        account.user.save()

        if not request.user.is_superuser:
            account.xp -= 200
            account.save()

        return JsonResponse({
            "success": True,
            "username":account.user.username
        })

    except Exception as e:
        return JsonResponse({"success":False, "error":f"{e}"})

@user_passes_test(lambda u: u.is_superuser)
def ChangeUserStaff(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            is_staff = data.get("is_staff", None)
            id = data.get("id", None)
            user = get_object_or_404(User, id=id)

            if is_staff == None:
                return JsonResponse({"success": False, "error":'Yanlış data formatı'})
            
            user.is_staff = is_staff 
            user.save()
            return JsonResponse({
                "success": True
            })

            
        except:
            return JsonResponse({"success": False, "error":'İstənilməyən xəta!'})

    
    return JsonResponse({"success": False, "error":'Yanlış cəhd!'})

















