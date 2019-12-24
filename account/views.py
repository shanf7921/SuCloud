import re

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from account.forms import LoginForm, UserInfoForm, RegistrationForm
from django.utils import timezone

from alarm.forms import RuleForm
from alarm.models import ParamError
from device.models import DeviceMd
from mold.models import Mold
from rbac.models import UserInfo


def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            print(user)
            if user:
                login(request, user)
                return HttpResponse("欢迎，登录成功")
            else:
                return HttpResponse("密码或者用户名错误")
        else:
            return HttpResponse("无效登录")
    else:
        login_form = LoginForm()
        return render(request, "account/login.html", {"form": login_form})

def register(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid()*userinfo_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userinfo_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            UserInfo.objects.create(user=new_user)
            return HttpResponse("successfully")
        else:
            return HttpResponse("抱歉，注册失败")
    else:
        user_form = RegistrationForm()
        userinfo_form = UserInfoForm()
        return render(request, "account/register.html", {"form": user_form, "userinfo": userinfo_form})


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

@csrf_exempt
def del_mold(request):
    mold_id = request.POST["mold_id"]
    try:
        line = Mold.objects.get(id=mold_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

@csrf_exempt
def mold_repair(request):
    mold_id = request.POST["mold_id"]
    try:
        line = Mold.objects.get(id=mold_id)
        line.m_status = 3
        line.save()

        # 增加一条维修记录
        # mr_start = timezone.now()
        # mr_user = "维修员"
        # mr_end = ""
        # mr_appear = "粘料"
        # mr_method = "打磨"
        # mr_des = "无、空白"
        #
        # r = Repair.createrepair(line.m_num, line.m_name, mr_user, mr_start, mr_end, mr_appear, mr_method, mr_des)
        # print(line.m_num, line.m_name, mr_user, mr_start, mr_end, mr_appear, mr_method, mr_des)
        # r.save()

        return HttpResponse("1")
    except:
        return HttpResponse("2")

@csrf_exempt
def mold_maintain(request):
    mold_id = request.POST["mold_id"]
    try:
        line = Mold.objects.get(id=mold_id)
        line.m_status = 4
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

@csrf_exempt
def mold_end(request):
    mold_id = request.POST["mold_id"]
    try:
        line = Mold.objects.get(id=mold_id)
        line.m_status = 2
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

@csrf_exempt
def del_rule(request):
    rule_id = request.POST["rule_id"]
    try:
        line = ParamError.objects.get(id=rule_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

@csrf_exempt
def add_rule(request):
    if request.method == "POST":
        try:
            t_device = request.POST.get('data[t_device]')
            e_time = request.POST.get('data[e_time]') or None
            e_tem = request.POST.get('data[e_tem]') or None
            e_place = request.POST.get('data[e_place]') or None
            e_pressure = request.POST.get('data[e_pressure]') or None
            e_remind = request.POST.get('data[e_remind]')
            # e_remind = e_remind.replace(",", " ") # 将逗号分隔的邮件转为 空格分隔的邮件
            e_remind = re.sub(r'[\n,]+', " ", e_remind) # 将逗号 回车 替换为空格
            D = DeviceMd.objects.filter(d_num=t_device)
            p = ParamError()
            print(t_device, e_time, e_tem, e_place, e_pressure, e_remind)
            p.t_device = D.first()
            p.e_time = e_time
            p.e_tem = e_tem
            p.e_place = e_place
            p.e_pressure = e_pressure
            p.e_remind = e_remind
            p.save()
            return HttpResponse("1")
        except Exception as e:
            print(e)
            return HttpResponse("2")

