from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from device.models import DeviceMd
from produce.models import Order


def kanban_produce(request):
    status1 = len(Order.objects.filter(o_status=1))
    status2 = len(Order.objects.filter(o_status=2))
    status3 = len(Order.objects.filter(o_status=3))
    status4 = len(Order.objects.filter(o_status=4))
    status5 = len(Order.objects.filter(o_status=5))

    d_status1 = len(DeviceMd.objects.filter(d_status=1))
    d_status2 = len(DeviceMd.objects.filter(d_status=2))
    d_status3 = len(DeviceMd.objects.filter(d_status=3))

    context = {
        'status1': status1,
        'status2': status2,
        'status3': status3,
        'status4': status4,
        'status5': status5,
        'd_status1': d_status1,
        'd_status2': d_status2,
        'd_status3': d_status3,
    }
    return render(request, 'kanban/kanban_product.html', context=context)


def kanban_device(request):
    devices = DeviceMd.objects.all()
    return render(request, 'kanban/kanban_device.html', {"devices": devices})


def kanban_order(request):
    orders = Order.objects.all()
    return render(request, 'kanban/kanban_order.html', {"orders": orders})