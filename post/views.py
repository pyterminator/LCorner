import json
from post.models import Post
from django.db.models import F
from member.models import Account
from dashboard.models import Like
from django.http import JsonResponse
from notifications.models import Notification
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test 

@login_required
def post_create_view(request):
    data = {}
    if request.method == "POST":


        foreign_lang = request.POST.get("foreign_lang")
        sentence = request.POST.get("sentence")
        description = request.POST.get("desc")
        author = request.user

        data["foreign_lang"] = foreign_lang
        data["sentence"] = sentence
        data["desc"] = description 

        account = Account.objects.filter(user=author).first()
        if (account and account.xp >= 100) or (account and account.user.is_superuser):
            if not account.user.is_superuser:
                account.xp -= 100
                account.save()

            Post.objects.create(
                author = account, 
                lang = foreign_lang,
                sentence = sentence,
                description = description,
                is_public = True,
                approved = True if request.user.is_superuser else False
            )

            return redirect("dashboard")

    return render(request, "post/create.html", context=data)

@user_passes_test(lambda u: u.is_superuser)
def posts_view(request):
    posts = Post.objects.all().order_by("-id")

    data = {
        "posts": posts
    }

    return render(request, "dashboard/posts.html", context = data)

@user_passes_test(lambda u: u.is_superuser)
def post_approved_view(request, id):
    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "success": False
            }
        )
    
    if request.method == "POST":
        p = Post.objects.filter(id=id).first()
        if p:
            try:
                if p.approved:
                    p.approved = False 
                else:
                    p.approved = True 
                p.save()

                Notification.objects.create(
                    account=p.author,
                    type="SYSTEM",
                    message=f"🎉 Postunuz təsdiqləndi!"
                )

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

@login_required
def post_detail_view(request, slug):
    try:
        post = get_object_or_404(Post, slug=slug)
        
        data = {
            "post": post
        }


        my_account = get_object_or_404(Account, user=request.user)
        liked_posts = set(
            my_account.likes.values_list("post_id", flat=True)
        )
        
        if post.id in liked_posts:
            data["liked"] = True 
        else:
            data["liked"] = False
        
        return render(request, "post/post-detail.html", context=data)
    except:
        return redirect("dashboard")

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

                Notification.objects.create(
                    account=post.author,
                    actor=account,
                    title="Heyyy!",
                    type="LIKE",
                    message=f"🎉 10 xal qazandın! {account.user.username} sizin postunuzu bəyəndi!",
                    data={
                        "post_slug": post.slug
                    }
                )
            

        return JsonResponse({
            "success": True, 
            "new_like_count":post.likes,
            "liked": liked
        })

    except:
        return JsonResponse({"success": False}) 
