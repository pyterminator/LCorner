import re
from datetime import timedelta
from django.utils import timezone
from contact.models import Message
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required

def contact_view(request):
    data = {}

    # HoneyPot
    if request.POST.get("website"): 
        data["message_validator"] = "Yanlış cəhd!"

    if request.method == "POST":
        last_sent = request.session.get("last_message_time")

        if last_sent:
            last_time = timezone.datetime.fromisoformat(last_sent) 

            cooldown_end = last_time + timedelta(hours=1)
            remaining = cooldown_end - timezone.now()


            if remaining.total_seconds() > 0:
                minutes = int(remaining.total_seconds() // 60)
                data["message_validator"] = f"{minutes} dəqiqə sonra yenidən mesaj göndərə bilərsiniz!"

        else:

            name = request.POST.get("name", "").strip()
            email = request.POST.get("email", "").strip()
            message = request.POST.get("message", "").strip()

            name_regex = r"^[A-ZÇŞƏĞÖÜİ][a-zçşəğöüıi]+$"
            message_regex = r"^[A-Za-zÇŞƏĞÖÜİçşəğöüıi0-9\s.!?]+$"
            email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"

            data['name'] = name 
            data['email'] = email
            data['message'] = message

            # NAME
            if not name:
                data["name_validator"] = "Ad boş ola bilməz!"
            elif len(name) < 3:
                data["name_validator"] = "Ad minimum 3 simvol olmalıdır!"
            elif not re.match(name_regex, name):
                data["name_validator"] = "Ad yalnız birinci hərfi böyük, qalanları kiçik olmalıdır!"

            # EMAIL
            if not email:
                data["email_validator"] = "Email boş ola bilməz!"
            elif not re.match(email_regex, email):
                data["email_validator"] = "Email düzgün formatda deyil!"

            # MESSAGE
            if not message:
                data["message_validator"] = "Mesaj boş ola bilməz!"
            elif len(message) < 5:
                data["message_validator"] = "Mesaj minimum 5 simvol olmalıdır!"
            elif len(message) > 255:
                data["message_validator"] = "Mesaj maksimum 255 simvol ola bilər!"
            elif not re.match(message_regex, message):
                data["message_validator"] = "Mesajda icazə verilməyən simvollar var!"

            # SUCCESS
            if "name_validator" not in data and "email_validator" not in data and "message_validator" not in data:
                Message.objects.create(
                    name=name, email=email, message=message
                )
                data["success"] = "Mesajınız qeydə alındı, tezliklə sizinlə əlaqə saxlanılacaq!"
                data.pop("name")
                data.pop("email")
                data.pop("message")
                request.session["last_message_time"] = timezone.now().isoformat()
            

    return render(request, "contact.html", context=data)


@user_passes_test(lambda u: u.is_superuser)
def messages_view(request):

    data = {
        "messages": Message.objects.all()
    }

    return render(request, "dashboard/messages.html", context=data)

@user_passes_test(lambda u: u.is_superuser)
def message_detail_view(request, id):
    msg = Message.objects.filter(id=id).first()
    if not msg:
        return redirect("messages")
    msg.is_read = True 
    msg.save()
    return render(request, "dashboard/message-detail.html", context={"message": msg})

@user_passes_test(lambda u: u.is_superuser)
def delete_contact_message_view(request):
    if request.method == "POST":
        id = request.POST.get("id")
        msg = Message.objects.filter(id=id).first()
        if msg: msg.delete()
    return redirect("contactmessages")

def message_read_view(request, id):
    if not request.user.is_superuser:
        return JsonResponse(
            {
                "success": False
            }
        )
    
    if request.method == "POST":
        msg = Message.objects.filter(id=id).first()
        if msg:
            if msg.is_read:
                msg.is_read = False 
            else:
                msg.is_read = True 
            msg.save()
            return JsonResponse({
                "success":True
            })
        
    return JsonResponse({
        "success":False
    })


def message_public_view(request, id):
    if not request.user.is_superuser:
        return JsonResponse(
            {
                "success": False
            }
        )
    
    if request.method == "POST":
        msg = Message.objects.filter(id=id).first()
        if msg:
            if msg.is_public:
                msg.is_public = False 
            else:
                msg.is_public = True 
            msg.save()
            return JsonResponse({
                "success":True
            })
        
    return JsonResponse({
        "success":False
    })

