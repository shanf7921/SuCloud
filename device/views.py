from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from device.models import DeviceMd

# Create your views here.
def device_list(request):
    devices = DeviceMd.objects.all()
    return render(request, "device/device_list.html", {"devices": devices})

@csrf_exempt
def del_device(request):
    device_id = request.POST["device_id"]
    print(device_id)
    try:
        line = DeviceMd.objects.get(id=device_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")