import os
import json
import uuid
from post.models import Post 
from django.conf import settings
from member.models import Account
from django.utils.text import slugify
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

 
# Butun userlər girə bilər
@login_required
def Dashboard(request):
     
    
    posts = Post.objects.filter(approved=True).filter(is_public=True).order_by('-id')[:12]
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


@user_passes_test(lambda u: u.is_superuser)
def CreateDefaultPosts(request):
    if Post.objects.count() == 0:
        json_file = os.path.join(settings.BASE_DIR, "default-posts.json")
        account = get_object_or_404(Account, user=request.user)


        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)



        posts = [
            Post(
                author = account,
                lang = item["lang"],
                sentence = item[item["lang"].lower()],
                description = item['az'],
                approved = True,
                is_public = True,
                slug = f"{slugify(item[item['lang'].lower()])[:50]}-{uuid.uuid4().hex[:6]}"
            )
            for item in data
        ]

        Post.objects.bulk_create(posts)

    return redirect("dashboard")

    