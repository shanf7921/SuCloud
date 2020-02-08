from django.shortcuts import render

# Create your views here.
from alarm.views import generate_param, check_error
from device.models import DeviceMd
from produce.models import Order, OrderDevice


def produce_order(request):
    orders = Order.objects.all()
    return render(request, 'produce/produce_order.html', {"orders": orders})


def produce_dispense(request):
    # orders = Order.objects.filter(o_status=1)
    order_devices = OrderDevice.objects.filter(od_active=True)
    device_list = []
    for order_device in order_devices:
        device_list.append(order_device.d_id)
    orders = Order.objects.filter(o_status__in=[1, 2, 5]).order_by('o_status')
    devices = DeviceMd.objects.exclude(id__in=device_list)
    return render(request, 'produce/produce_dispense.html', {"orders": orders, "devices": devices})


def produce_speed(request):
    orders = Order.objects.all()
    return render(request, 'produce/produce_speed.html', {"orders": orders})