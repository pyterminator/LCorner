from django.shortcuts import render, redirect 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from datetime import date

START_DATE = date(2026, 5, 7)

# Butun userlər girə bilər
@login_required
def Dashboard(request):
    today = date.today()
    days = (today - START_DATE).days + 1


    data = {
        "days": days
    }
    return render(request, "dashboard/index.html", context=data)
