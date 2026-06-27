from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test


@user_passes_test(lambda u: u.is_staff)
def MyExams(request):
    return render(request, "exam/my-exams.html")

@user_passes_test(lambda u: u.is_staff)
def CreateNewExam(request):
    return render(request, "exam/create-new-exam.html") 


@login_required
def SentenceBuilder(request):

    data = {
        "words":['is', 'what', 'name', 'your'],
        "title":"Sözləri düzgün ardıcıllıqla yerləşdir",
        "answer":"what is your name"
    }

    return render(request, "sentence-builder.html", context=data)