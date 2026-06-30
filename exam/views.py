import json, random, re
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from member.models import Account
from post.models import Post
from django.http import JsonResponse
from django.contrib.auth.models import User


@user_passes_test(lambda u: u.is_staff)
def MyExams(request):
    return render(request, "exam/my-exams.html")

@user_passes_test(lambda u: u.is_staff)
def CreateNewExam(request):
    return render(request, "exam/create-new-exam.html") 

def PublicSentenceBuilder(request):
    if request.method == "POST": 
        body = json.loads(request.body)
        
        post_id = body.get("id", None) 
        user_answer = body.get("user_answer", None)

        get_post = Post.objects.filter(id=post_id).first() 

        answer = get_post.sentence.lower()
        # answer = re.sub(r"[^a-zA-Z0-9'\s]", "", answer)
        answer = re.sub(r"[^a-zA-Z0-9ÄäÖöÜüẞßА-Яа-яЁё'\s]", "", answer)


        answer = " ".join([w.strip() for w in answer.split()]) 
        
        if answer == user_answer:
            new_post = GetPostForPublicSentenceBuilder(request, get_post)
            data = PrepareQuizForSentenceBuilder(new_post)
            data["success"] = True

            return JsonResponse(data)
        else: 
            return JsonResponse({
                "success": False,
                "message":"Cavab yanlışdır!"
            })
         

    post = GetPostForPublicSentenceBuilder(request)
    if not post: return redirect("dashboard")
    data = PrepareQuizForSentenceBuilder(post)
    return render(request, "public-sentence-builder.html", context=data)

@login_required
def SentenceBuilder(request):

    user = User.objects.filter(username=request.user.username).first()
    my_account:Account = user.account

    if request.method == "POST": 
        body = json.loads(request.body)
        
        post_id = body.get("id", None) 
        user_answer = body.get("user_answer", None)

        get_post = Post.objects.filter(id=post_id).first() 

        answer = get_post.sentence.lower()
        # answer = re.sub(r"[^a-zA-Z0-9'\s]", "", answer)
        answer = re.sub(r"[^a-zA-Z0-9ÄäÖöÜüẞßА-Яа-яЁё'\s]", "", answer)


        answer = " ".join([w.strip() for w in answer.split()]) 
        
        if answer == user_answer:
            new_post = GetPostForSentenceBuilder(request, my_account, get_post)
            data = PrepareQuizForSentenceBuilder(new_post)
            data["success"] = True
            

            # 1 xal ver
            my_account.add_xp(1)

            data["xp"] = my_account.xp 
            data["level"] = my_account.level
 
            return JsonResponse(data)
        else: 
            return JsonResponse({
                "success": False,
                "message":"Cavab yanlışdır!"
            })
         

    post = GetPostForSentenceBuilder(request, my_account)
    if not post: return redirect("dashboard")
    data = PrepareQuizForSentenceBuilder(post)
    return render(request, "sentence-builder.html", context=data)



def GetPostForSentenceBuilder(request, my_account, p:Post|None=None):
    

    my_likes = list(Post.objects.filter(likes_set__account=my_account))

    post = random.choice(my_likes) if my_likes else None
    
    if p:
        while post.id == p.id:
            post = random.choice(my_likes) if my_likes else None

    return post

def GetPostForPublicSentenceBuilder(request, p:Post|None=None):
    posts = Post.objects.filter(approved=True, is_public=True).all()
    post = random.choice(posts) if posts else None
    
    if p:
        while post.id == p.id:
            post = random.choice(posts) if posts else None

    return post

def PrepareQuizForSentenceBuilder(post:Post):
    sentence = post.sentence.lower()
 
    # sentence = re.sub(r"[^a-zA-Z0-9'\s]", "", sentence)
    sentence = re.sub(r"[^a-zA-Z0-9ÄäÖöÜüẞßА-Яа-яЁё'\s]", "", sentence)

    words = sentence.split()
    random.shuffle(words)

    return {
        "words": words,
        "title": "Sözləri düzgün ardıcıllıqla yerləşdir",
        "description": post.description,
        "id": post.id,
        "answer": sentence
    }






