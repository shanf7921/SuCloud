from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
def report_produce(request):
    return HttpResponseRedirect('/kanban/produce/')


def report_device(request):
    return HttpResponseRedirect('/kanban/produce/')


def report_mold(request):
    return HttpResponseRedirect('/kanban/produce/')


def report_quality(request):
    return HttpResponseRedirect('/kanban/produce/')