import json
from post.models import Post
from django.db.models import F
from member.models import Account
from dashboard.models import Like
from django.http import JsonResponse
from notifications.models import Notification
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test 
from django.utils import timezone
from datetime import timedelta, datetime
from django.views.decorators.http import require_POST

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


def post_detail_view(request, slug):
    try:
        post = get_object_or_404(Post, slug=slug)

        # Every Refresh
        now = timezone.now()
        session_key = f"viewed_post_{post.id}"
        last_view = request.session.get(session_key)

        if (not last_view or now - (datetime.fromisoformat(last_view) if isinstance(last_view, str) else last_view) >= timedelta(hours=1)):
            post.increase_view()
            request.session[session_key] = now.isoformat()


        if request.user.is_authenticated and request.user != post.author.user:
            account = get_object_or_404(Account, user=request.user)
            
            Notification.objects.create(
                account=post.author,
                actor=account,
                title="Postun cəlb edir!",
                type="SYSTEM",
                message=f"{account.user.username} postuna baxdı.",
                data={
                    "post_slug": post.slug
                }
            )

        data = {
            "post": post
        }

        if request.user.is_authenticated:
            my_account = get_object_or_404(Account, user=request.user)
            data["liked"] = my_account.likes.filter(post=post).exists()
        
        return render(request, "post/post-detail.html", context=data)
    except:
        return redirect("dashboard")

# Login Required vermek lazim deyil!
def PostLike(request):

    if not request.user.is_authenticated:
        return JsonResponse({"success": False})

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
            post.view = F("view") + 1
            post.save(update_fields=["likes", "view"])
            post.refresh_from_db()
            
            if account.id != post.author.id:

                Account.objects.filter(id=post.author_id).first().add_xp(10)

                Notification.objects.create(
                    account=post.author,
                    actor=account,
                    title="Heyyy!",
                    type="LIKE",
                    message=f"🎉 10 xal qazandın! {account.user.username} postunu bəyəndi!",
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

@require_POST
def LoadPost(request):
    data = json.loads(request.body)
    last_id = data.get("last_id", None)

    if last_id:
        posts = Post.objects.filter(
            id__lt=last_id
        ).order_by("-id")[:6]

        post_list = [
            {
                "is_authenticated": request.user.is_authenticated,
                "id": post.id,
                "sentence": post.sentence,
                "description": post.description,
                "slug": post.slug,
                "likes": post.likes,
                "view": post.view,
                "username": post.author.user.username,
                "smartdate": post.smart_date,
                "avatar": (
                    post.author.avatar.url
                    if post.author.avatar
                    else None
                ),
                "fullname": post.author.user.last_name + " " + post.author.user.first_name,
                "lang": post.lang
            }
            for post in posts
        ]

        last_post_id = posts[len(posts) - 1].id if posts else last_id

        has_more = Post.objects.filter(
            id__lt=last_post_id
        ).exists()

        return JsonResponse({
            "success": True,
            "posts": post_list,
            "has_more": has_more,
        })

    return JsonResponse({
        "success": False,
        "type": "error",
        "message": "Xəta oldu!"
    })

