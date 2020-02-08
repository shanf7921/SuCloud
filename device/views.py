from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from device.models import DeviceMd, DeviceRepair


# Create your views here.
from rbac.models import UserInfo


def device_list(request):
    devices = DeviceMd.objects.all()
    users = UserInfo.objects.all()
    return render(request, "device/device_list.html", {"devices": devices, "users": users})

def device_status(request):
    devices = DeviceMd.objects.all()
    return render(request, "device/device_status.html", {"devices": devices})



def device_maintain(request):
    devices = DeviceMd.objects.all()
    device_repair = DeviceRepair.objects.all()
    return render(request, "device/device_maintain.html", {"devices": devices, "device_repair": device_repair})