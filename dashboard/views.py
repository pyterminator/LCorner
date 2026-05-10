from django.shortcuts import render, redirect
from dashboard.models import Level
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