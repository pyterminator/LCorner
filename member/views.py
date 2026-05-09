from django.shortcuts import render

def MemberLogin(request):
    return render(request, 'login.html')