import json, random, re
from post.models import Post
from django.db import transaction
from exam.models import Exam, Tag
from member.models import Account
from django.http import JsonResponse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test


@user_passes_test(lambda u: u.is_staff)
def MyExams(request):
    my_exam_list = request.user.account.exams.order_by("-id").all()

    data = {
        "my_exam_count": len(my_exam_list),
        "exams": my_exam_list,
        "my_active_exam_count": my_exam_list.filter(is_active=True).count(),
        "my_deactive_exam_count": my_exam_list.filter(is_active=False).count(),
    }

    return render(request, "exam/my-exams.html", context=data)

@user_passes_test(lambda u: u.is_staff)
def CreateNewExam(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            question_count = 0
            title = data.get("title", "")
            exam_type = data.get("exam_type", "")
            if exam_type == "Limitli":
                question_count = int(data.get("question_count", 0))
            price = data.get("price", 0)
            difficulty = data.get('difficulty', "") 
            description = data.get("description", "")
            tags = data.get("tags", [])

            if price == "Pulsuz": price = 0
            else: price = int(price)

            if exam_type == "Limitli": exam_type = "limited"
            elif exam_type == "Limitsiz": exam_type = "endless"
            else: exam_type = "endless"

            if difficulty == "Asan": difficulty = "easy"
            elif difficulty == "Orta": difficulty = "medium"
            elif difficulty == "Çətin": difficulty = "hard"
            else: difficulty = "easy"
            
            new_tags = []
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                new_tags.append(tag)

    
            with transaction.atomic():

                exam = Exam.objects.create(
                    author = request.user.account,
                    title = title,
                    slug = slugify(title),
                    description = description,
                    difficulty = difficulty,
                    exam_type = exam_type,
                    price = price,
                    duration = question_count * 2 if question_count > 0 and exam_type == "limited" else 0,
                    question_count = question_count if exam_type == "limited" else 0,
                    earn_xp = question_count * 1 
                )

                exam.tags.set(new_tags)
            
    

            return JsonResponse({
                "success": True,
                "message": "İmtahan uğurla yaradıldı!"
            })
        except Exception as e:  
            print(e)
            return JsonResponse({
                "success": False,
                "message": "İmtahan yaradılmadı!",
                "error": f"{e}"
            })

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
            data["xp"] = None
            data["level"] = None

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

    if lang := request.GET.get("lang", ""):
        lang: str = lang.upper()
        if lang not in ["EN", "RU", "GE"]:
            lang = "EN"
        my_likes = [ml for ml in my_likes if ml.lang == lang]



    post = random.choice(my_likes) if my_likes else None
    
    if p:
        while post.id == p.id:
            post = random.choice(my_likes) if my_likes else None

    return post

def GetPostForPublicSentenceBuilder(request, p:Post|None=None):

    if lang := request.GET.get("lang", ""):
        lang: str = lang.upper()
        if lang not in ["EN", "RU", "GE"]:
            lang = "EN"
        posts = Post.objects.filter(approved=True, is_public=True, lang=lang).all()
    else:
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


def UpdateExam(request, slug: str):
    exam = Exam.objects.filter(slug=slug).first()
    if exam:
        data = {
            "exam": exam
        }
        return render(request, "exam/update-exam.html", context=data)
    
    
    return redirect("dashboard")









