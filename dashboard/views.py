from django.shortcuts import render, redirect 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from post.models import Post 
from member.models import Account

from datetime import date

START_DATE = date(2026, 5, 7)

# Butun userlər girə bilər
@login_required
def Dashboard(request):
    today = date.today()
    days = (today - START_DATE).days + 1
    
    posts = Post.objects.filter(approved=True).all().order_by('-id')
    my_account = Account.objects.filter(user=request.user).first()


    data = {
        "days": days,
        "has_post": Post.objects.filter(author=my_account).first(),
        "posts": posts
    }
    return render(request, "dashboard/index.html", context=data)
