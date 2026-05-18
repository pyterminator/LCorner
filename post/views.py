from post.models import Post
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test 

@login_required
def post_create_view(request):
    if request.method == "POST":
        foreign_lang = request.POST.get("foreign_lang")
        sentence = request.POST.get("sentence")
        description = request.POST.get("desc")
        author = request.user

        new_post = Post.objects.create(
            author = author, 
            lang = foreign_lang,
            sentence = sentence,
            description = description
        )

        return redirect("dashboard")

    return render(request, "post/create.html")

@user_passes_test(lambda u: u.is_superuser)
def posts_view(request):
    posts = Post.objects.all()

    data = {
        "posts": posts
    }

    return render(request, "dashboard/posts.html", context = data)




