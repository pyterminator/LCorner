import json
from django.shortcuts import render, redirect 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from post.models import Post 
from member.models import Account
from django.http import JsonResponse
from dashboard.models import Like
from django.shortcuts import get_object_or_404
 
# Butun userlər girə bilər
@login_required
def Dashboard(request):
     
    
    posts = Post.objects.filter(approved=True).filter(is_public=True).all().order_by('-id')
    my_account = Account.objects.filter(user=request.user).first()


    data = { 
        "has_post": Post.objects.filter(author=my_account).first(),
        "posts": posts
    }
    return render(request, "dashboard/index.html", context=data)

@login_required
def PostLike(request):

    if request.method != "POST":
        return JsonResponse({"success": False})
    
    try:
        account = Account.objects.filter(user=request.user).first()
        data = json.loads(request.body)
        post_id = data.get("id")

        post = get_object_or_404(Post, id=post_id)

        like, created = Like.objects.get_or_create(
            account=account,
            post=post
        )

        if not created:
            like.delete()
            liked = False
        else:
            liked = True
            post.likes += 1
            post.save()
            

        return JsonResponse({
            "success": True, 
            "new_like_count":post.likes,
            "liked": liked
        })

    except:
        return JsonResponse({"success": False}) 