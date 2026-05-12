from django.shortcuts import render, redirect
from dashboard.models import Level
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def Dashboard(request):
    return render(request, "dashboard/index.html")

@login_required
def Levels(request):

    data = {
        "levels": Level.objects.all()
    }

    return render(request, "dashboard/levels.html", context=data)

@login_required
def CreateLevel(request):

    if request.method == "POST":
        name = request.POST.get("levelname")
        q_count = request.POST.get("questioncount")
        scorepq = request.POST.get("scorepq")
        ispaid = request.POST.get("ispaid")
        price = request.POST.get("price") 

         


        if ispaid == "1": 
            ispaid = True
        else:
            price = 0
            ispaid = False


        try:
            new_level = Level.objects.create(
                name=name,
                q_count=q_count,
                scorepq=scorepq,
                ispaid=ispaid,
                price=price,
                is_public=False
            )
        except: pass 
        else: return redirect("levels")


         

    return render(request, "dashboard/create-new-level.html")


@login_required
def LevelDetail(request, id):
    find_level = Level.objects.filter(id=id).first()

    if find_level:

        data = {
            "level": find_level
        }

        return render(request, "dashboard/level-detail.html", context=data)
    
    else:
        return redirect("levels")

@login_required
def QuizModels(request):
    return render(request, "dashboard/quiz-models.html")

@login_required
def CreateQuizWithOptions(request):
    return render(request, "gamemodels/with-options.html")

@login_required
def Users(request):

    data = {
        "users": User.objects.all()
    }

    return render(request, 'dashboard/users.html', context=data)

@login_required
def UserDetail(request, id):
    user = User.objects.filter(id=id).first()

    # Verilmiş İD ilə user olmasa users səhifəsinə qaytar
    if user is None: return redirect("users")

    if request.method == "POST":
        is_active = request.POST.get("is_active", False )
        is_staff = request.POST.get("is_staff", False)
        is_superuser = request.POST.get("is_superuser", False)

        
        if is_active == "1": is_active = True 
        else: is_active = False 

        if is_staff == "1": is_staff = True 
        else: is_staff = False 

        if is_superuser == "1": is_superuser = True 
        else: is_superuser = False 

       

        user.is_active = is_active
        user.is_staff = is_staff
        user.is_superuser = is_superuser

        user.save()
        

    # user varsa datasını göndər səhifəyə
    data = {
        "user": user
    }

    return render(request, "dashboard/user-detail.html", context=data)

@login_required
def CreateUser(request):
    return render(request, "dashboard/create-new-user.html")

@login_required
def DeleteUser(request, id):
    user = User.objects.filter(id=id).first()

    if user is None: return redirect("users")

    user.is_active = False 
    user.is_staff = False 
    user.is_superuser = False
    user.save()

    return redirect("users")

@login_required
def Account(request, username):
    user = User.objects.filter(username=username).first()

    if user:
        data = {
            "user":user
        }
        return render(request, "dashboard/account.html", context=data)
    
    return redirect("dashboard")















