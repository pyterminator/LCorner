from django.shortcuts import render, redirect
# from dashboard.models import Level
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Butun userlər girə bilər
@login_required
def Dashboard(request):
    return render(request, "dashboard/index.html")
