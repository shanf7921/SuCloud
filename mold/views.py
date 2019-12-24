from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from mold.forms import MoldForm
from mold.models import Mold

def mold_list(request):
    molds = Mold.objects.all()
    if request.method == "POST":
        mold_form = MoldForm(request.POST)
        if mold_form.is_valid():
            mold_form.save()
            return render(request, 'mold/mold_list.html', {"molds": molds, "form": mold_form})
        else:
            return HttpResponse("抱歉，添加失败")
    else:
        mold_form = MoldForm()
        return render(request, 'mold/mold_list.html', {"molds": molds, "form": mold_form})

def mold_maintain(request):
    molds = Mold.objects.all()
    return render(request, 'mold/maintain.html', {"molds": molds})

def mold_record(request):
    molds = Mold.objects.all()
    return render(request, 'mold/maintain.html', {"molds": molds})