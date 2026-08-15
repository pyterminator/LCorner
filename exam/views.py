import json, random, re
from post.models import Post
from django.db.models import Max
from django.db import transaction
from member.models import Account
from django.contrib import messages
from django.http import JsonResponse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from exam.models import Exam, Tag, Quiz, QuizOption
from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.decorators import login_required, user_passes_test
from notifications.models import Notification

# Sentence Builder Game Ucun post.sentence-i liste cevirir
def GenerateWordsForSB(sentence:str)-> list:
    sentence = sentence.replace("’", "'").replace("`", "'").replace("‘", "'")

    sentence = re.sub(
        r"[^a-zA-Z0-9ÄäÖöÜüẞßА-Яа-яЁё'\s]",
        "",
        sentence
    )
    words = sentence.split() 
    return words

@user_passes_test(lambda u: u.is_staff)
def MyExams(request):
    my_exam_list = request.user.account.exams.order_by("-id").all()

    data = {
        "my_exam_count": len(my_exam_list),
        "exams": my_exam_list,
        "participants": Account.objects.filter(enrolled_exams__isnull=False ).count(),
        "my_active_exam_count": my_exam_list.filter(is_active=True).count(),
        "my_deactive_exam_count": my_exam_list.filter(is_active=False).count(),
    }

    return render(request, "exam/my-exams.html", context=data)

@user_passes_test(lambda u: u.is_staff)
def CreateNewExam(request):

    if (not request.user.is_superuser) and request.user.account.xp <= 100:
        messages.error(request, "İmtahan yaratmaq üçün minimum 100 XP lazımdır.")
        return redirect("myexams")

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

                if not request.user.is_superuser:
                    request.user.account.add_xp(-100)
                    Notification.objects.create(
                        account=request.user.account,
                        type="SYSTEM",
                        message=f"İmtahan üçün hesabdan 100xp silindi."
                    )
            
    

            return JsonResponse({
                "success": True,
                "message": "İmtahan uğurla yaradıldı!"
            })
        except Exception as e:   
            return JsonResponse({
                "success": False,
                "message": "İmtahan yaradılmadı!",
                "error": f"{e}"
            })

    return render(request, "exam/create-new-exam.html") 

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
        answer = GenerateWordsForSB(answer)

        answer = " ".join([w.strip() for w in answer]) 
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
    lang = request.GET.get("lang", "").upper()
    if lang not in ["EN", "RU", "GE"]:
        lang = "EN"

    queryset = Post.objects.filter(likes_set__account=my_account)

    if lang:
        queryset = queryset.filter(lang=lang)

    count = queryset.count() 
    if count == 0: return None

    post = queryset[random.randint(0, count - 1)] 

    if p:
        while post.id == p.id:
            post = queryset[random.randint(0, count - 1)] 
    return post


def GenerateWordsForSB(sentence:str)-> list:
    sentence = sentence.replace("’", "'").replace("`", "'").replace("‘", "'")

    sentence = re.sub(
        r"[^a-zA-Z0-9ÄäÖöÜüẞßА-Яа-яЁё'\s]",
        "",
        sentence
    )
    words = sentence.split() 
    return words

def PrepareQuizForSentenceBuilder(post:Post):
    sentence = post.sentence.lower()
    words = GenerateWordsForSB(sentence)
    
    while GenerateWordsForSB(sentence) == words:
        random.shuffle(words) 

    return {
        "words": words,
        "title": "Sözləri düzgün ardıcıllıqla yerləşdir",
        "description": post.description,
        "id": post.id,
        "answer": " ".join(GenerateWordsForSB(sentence))
    }

@user_passes_test(lambda u: u.is_staff)
def UpdateExam(request, slug: str):
    try: 
        exam = get_object_or_404(Exam, slug=slug)
        quizzes = exam.quizzes.all().order_by("-id")
        
            

        if request.method == "POST":
            data = json.loads(request.body)

            quiz_text_title = data.get("question", "")
            options = data.get("options", [])
            correct_answer = data.get("correct_answer", "")

            last_order = (
                exam.quizzes.aggregate(Max("order"))["order__max"] or 0
            )


            options = {
                "a": options[0],
                "b": options[1],
                "c": options[2],
                "d": options[3],
            }

            try:
                with transaction.atomic():
                    new_quiz = Quiz.objects.create(
                        exam = exam,
                        question = quiz_text_title,
                        order = last_order + 1
                    )

                    for key, text in options.items():
                        QuizOption.objects.create(
                            quiz=new_quiz,
                            text=text,
                            is_correct=(correct_answer == key)
                        )

                return JsonResponse({
                    "success":True,
                    "id": new_quiz.id,
                    "question": new_quiz.question,
                    "options": list(new_quiz.options.values("id", "text", "is_correct"))
                })
            except:
                return JsonResponse({
                    "success": False
                })


        data = {
            "exam": exam,
            "quizzes": quizzes,
            "quizzes_count": quizzes.count()
        }
        return render(request, "exam/update-exam.html", context=data)
    
    except:
        return redirect("dashboard")


@user_passes_test(lambda u: u.is_staff)
@require_POST
def ActivateExam(request, id):
    try:
        exam = get_object_or_404(Exam, id=id)
        if exam.author.user.id != request.user.id:
            return JsonResponse({
                "success": False,
                "type": "error",
                "message": "İcazəsiz cəhd!"
            })

        if exam.exam_type == "endless" and exam.quizzes.count() < 10: 
            return JsonResponse({
                "success": False, 
                "type": "error",
                "message": "Limitsiz sualdan ibarət olan imtahanı aktiv etmək üçün imtahanda minimum 10-sual olmalıdır."
            })


        if exam.is_active == True:
            exam.is_active = False 
            exam.save()
            return JsonResponse({
                "success": True,
                "type":"success",
                "is_activate": exam.is_active,
                "message": "İmtahan deaktiv edildi!"
            })
        else:
            exam.is_active = True
            exam.save()
            return JsonResponse({
                "success": True,
                "type":"success",
                "is_activate": exam.is_active,
                "message": "İmtahan aktiv edildi!"
            })
        
    except:

        return JsonResponse({
            "success": False,
            "type": "error",
            "message": "Xəta oldu!"
        })



def ExamDetailView(request, slug):
    try:
        exam = get_object_or_404(Exam, slug=slug)
        quizzes = exam.quizzes.all().order_by("-id")


        data = {
            "exam": exam,
            "quizzes": quizzes,
            "quizzes_count": quizzes.count()
        }
    
        return render(request, "exam/exam-detail.html", context=data)

    except Exam.DoesNotExist:
        return redirect("dashboard")

    
def ExamPano(request, slug):
    try:
        exam = get_object_or_404(Exam, slug=slug)
        # quizzes = exam.quizzes.all().order_by("-id")


        data = {
            "exam": exam,
            # "quizzes": quizzes,
            # "quizzes_count": quizzes.count()
        }
    
        return render(request, "exam/exam-pano.html", context=data)

    except Exam.DoesNotExist:
        return redirect("dashboard")

@require_POST
def GenerateQuizForExamPano(request, slug):
    try:
        exam = get_object_or_404(Exam, slug=slug)

        posted_data = json.loads(request.body)
        quiz_id = posted_data.get("id", None)
        if quiz_id:
            quizzes = exam.quizzes.exclude(id=5)
        else:
            quizzes = exam.quizzes.all()
            
        count = quizzes.count() 

        if count == 0:
            return JsonResponse({
                "success": False,
                "message": "Bu imtahanda sual yoxdur."
            })


        if exam.exam_type == "endless":
            quiz: Quiz = quizzes[random.randint(0, count - 1)]
            return JsonResponse({
                "success": True,
                "id": quiz.id,
                "text": quiz.question,
                "options": [
                    {
                        "id": option.id,
                        "text": option.text,
                        "is_correct": option.is_correct,
                    }
                    for option in quiz.options.all()
                ]
            })

        return JsonResponse({
            "success": False,
            "message": "Limitli sual ucun generasiya hazir deyil"
        })

    except Exam.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Yanlış cəhd!"
        })


@require_POST
def CheckAnswer(request):
    try:
        data = json.loads(request.body)
        id = data.get("id", None)
        answer = data.get("answer", None)

        quiz = get_object_or_404(Quiz, id=id)
        options : QuizOption = quiz.options.all()

        opt_letters = ['a', 'b', 'c', 'd']

        if opt := options[opt_letters.index(answer)]:
            if opt.is_correct:
                return JsonResponse({
                    "success": True
                })

        return JsonResponse({
            "success": False
        })
    
    except:
        return JsonResponse({
            "success": False
        })

@user_passes_test(lambda u: u.is_staff)
@require_POST
def CheckIsFullExamWithQuestions(request):
    try:
        data = json.loads(request.body)
        id = data.get("id")
        exam = get_object_or_404(Exam, id=id)

        if exam.exam_type == "endless":
            return JsonResponse({"success": True})

        if exam.question_count > exam.quizzes.all().count():
            return JsonResponse({"success": False, "message": "İmtahan suallarla doludurulmayıb!"})

        return JsonResponse({"status": True, "message": "İmtahan suallarla doldurulub!"})
    except:
        return JsonResponse({
            "status": False,
            "message": "'İmtahan suallarla dolubmu ?' - yoxlama prosesində xəta oldu!"
        })



@require_POST
@login_required
def EnrollExam(request):
    try:
        data = json.loads(request.body)
        exam_id = data.get("exam_id")

        exam = get_object_or_404(Exam, id=exam_id)

        exam.participants.add(request.user.account)

        return JsonResponse({
            "status": True,
            "message": "İmtahana uğurla yazıldınız!"
        })

    except Exception:
        return JsonResponse({
            "status": False,
            "message": "İmtahana yazılarkən xəta baş verdi!"
        })