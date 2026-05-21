from post.models import Post 
from member.models import Account
from django.contrib.auth.models import User
from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required

 
# Butun userlər girə bilər
@login_required
def Dashboard(request):
     
    
    posts = Post.objects.filter(approved=True).filter(is_public=True).all().order_by('-id')
    my_account = Account.objects.filter(user=request.user).first()

    liked_posts = set(
        my_account.likes.values_list("post_id", flat=True)
    )


    data = { 
        "has_post": Post.objects.filter(author=my_account).first(),
        "posts": posts,
        "liked_posts":liked_posts
    }
    return render(request, "dashboard/index.html", context=data)



