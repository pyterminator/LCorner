from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test


@user_passes_test(lambda u: u.is_staff)
def MyExams(request):
    return render(request, "exam/my-exams.html")