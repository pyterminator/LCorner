from post.models import Post
from member.models import Account
from dashboard.models import Like
from django.http import JsonResponse
from django.shortcuts import render, redirect
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
                is_public = True
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
            if p.approved:
                p.approved = False 
            else:
                p.approved = True 
            p.save()
            return JsonResponse({
                "success":True
            })
        
    return JsonResponse({
        "success":False
    })


@login_required
def post_detail_view(request, id):
    post = Post.objects.filter(id=id).first()
    if post:

        data = {
            "post": post
        }

        my_account = Account.objects.filter(user=request.user).first()
        liked_posts = set(
            my_account.likes.values_list("post_id", flat=True)
        )
        if post.id in liked_posts:
            data["liked"] = True 
        else:
            data["liked"] = False
        
        return render(request, "post-detail.html", context=data)
    
    return redirect("dashboard")
