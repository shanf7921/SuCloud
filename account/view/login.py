from django.shortcuts import render, redirect, HttpResponse
from rbac.service import init_permission

def login(request):

    return render(request, "login.html")