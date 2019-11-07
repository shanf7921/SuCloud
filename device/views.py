from django.shortcuts import render
from device.models import DeviceMd

# Create your views here.
def device_list(request):
    devices = DeviceMd.objects.all()
    return render(request, "device/device_list.html", {"devices": devices})