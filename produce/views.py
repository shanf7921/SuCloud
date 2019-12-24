from django.shortcuts import render

# Create your views here.
from alarm.views import generate_param, check_error


def produce_order(request):
    generate_param()
    return render(request, 'produce/produce_order.html')


def produce_dispense(request):
    check_error(request)
    return render(request, 'produce/produce_dispense.html')


def produce_speed(request):
    return render(request, 'produce/produce_speed.html')