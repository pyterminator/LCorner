import json
from django.shortcuts import render, redirect 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from post.models import Post 
from member.models import Account
from django.http import JsonResponse
from dashboard.models import Like
from django.shortcuts import get_object_or_404
from django.db.models import F
 
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

@login_required
def PostLike(request):

    if request.method != "POST":
        return JsonResponse({"success": False})
    
    try: 
        account = get_object_or_404(Account, user=request.user)

        data = json.loads(request.body)
        post_id = data.get("id")

        post = get_object_or_404(Post, id=post_id)



        like = Like.objects.filter(account=account, post=post).first()

        created = False

        if like is None:
            like = Like.objects.create(
                account=account,
                post=post
            )
            created = True

        if not created:
            liked = False
        else:
            liked = True

            post.likes = F("likes") + 1
            post.save(update_fields=["likes"])
            post.refresh_from_db()
            
            if account.id != post.author.id:
                Account.objects.filter(id=post.author_id).update(
                    xp=F("xp") + 10
                )
            

        return JsonResponse({
            "success": True, 
            "new_like_count":post.likes,
            "liked": liked
        })

    except:
        return JsonResponse({"success": False}) 