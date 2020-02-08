import datetime
import json
import re
import time
from SuCloud import celery_app
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from account.forms import LoginForm, UserInfoForm, RegistrationForm
from django.utils import timezone

from account.task import sendtime
from alarm.forms import RuleForm
from alarm.models import ParamError
from device.models import DeviceMd, DeviceRepair
from mold.models import Mold, Repair
from produce.models import Order, OrderDevice
from rbac.models import UserInfo, Role, Permission


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


# 模具维修
@csrf_exempt
def mold_repair(request):
    mold_id = request.POST["mold_id"]
    mr_user = request.POST.get('data[mr_user]')
    mr_appear = request.POST.get('data[mr_appear]')
    mr_method = request.POST.get('data[mr_method]')
    mr_des = request.POST.get('data[mr_des]')
    try:
        line = Mold.objects.get(id=mold_id)
        status = line.m_status
        if status == '2':
            line.m_status = 3
            line.save()

            # 增加一条维修记录
            r = Repair()
            r.mr_num = line
            r.mr_name = line.m_name
            # r.mr_start = timezone.now()
            r.mr_user = mr_user
            # r.mr_end = ""
            r.mr_appear = mr_appear
            r.mr_method = mr_method
            r.mr_des = mr_des
            r.save()
            return HttpResponse("1")
        else:
            return HttpResponse("5")
    except Exception as e:
        print(e)
        return HttpResponse("2")

# 模具保养
@csrf_exempt
def mold_maintain(request):
    mold_id = request.POST["mold_id"]
    try:
        line = Mold.objects.get(id=mold_id)
        status = line.m_status
        if status == '2':
            line.m_status = 4
            line.save()
            return HttpResponse("1")
        else:
            return HttpResponse('5')
    except:
        return HttpResponse("2")

# 结束模具维修、保养
@csrf_exempt
def mold_end(request):
    mold_id = request.POST["mold_id"]
    try:
        line = Mold.objects.get(id=mold_id)
        status = line.m_status
        line.m_status = 2
        line.save()
        print(status)
        if status == '3':
            # 找到此模具的维修记录，并按照开始时间逆序排列，选取第一条记录
            repair = Repair.objects.filter(mr_num=line).order_by('-mr_start').first()
            repair.mr_end = timezone.now()
            repair.save()
            return HttpResponse("1")
        elif status == '4':
            return HttpResponse("4")
        else:
            return HttpResponse("3")
    except Exception as e:
        print(e)
        print('----2')
        return HttpResponse("2")

# 删除报警规则
@csrf_exempt
def del_rule(request):
    rule_id = request.POST["rule_id"]
    try:
        line = ParamError.objects.get(id=rule_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

# 添加报警规则
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

# 改变权限
@csrf_exempt
def change_permission(request):
    if request.method == "POST":
        try:
            permissions = request.POST.get('permissions')
            rolename = request.POST.get('rolename')
            permissions = permissions.split(',')
            role = Role.objects.get(title=rolename)
            # 获取当前所具有的权限
            role_permissions = role.permissions.all()
            # 删除当前所具有的全部权限
            role.permissions.remove(*role_permissions)
            for id in permissions:
                id = int(id)
                permission = Permission.objects.filter(id=id).first()
                # 添加权限
                role.permissions.add(permission)
            return HttpResponse("1")
        except Exception as e:
            print(e)
            return HttpResponse("2")

# 获取权限
@csrf_exempt
def get_permission(request):
    if request.method == "POST":
        try:
            rolename = request.POST.get('rolename')
            role = Role.objects.filter(title=rolename).first()
            permissions = role.permissions.all()
            dict1 = {}
            for permission in permissions:
                dict1[permission.id] = permission.title
            dict2 = json.dumps(dict1),
            return HttpResponse(dict2, content_type="application/json")
        except Exception as e:
            print(e)
            return HttpResponse("2")
    return None

@csrf_exempt
def rule_change(request):
    device_id = request.POST['device_id']
    try:
        t = ParamError.objects.filter(t_device=device_id).first()
        t.e_error = not t.e_error
        t.save()
        return HttpResponse("1")
    except Exception as e:
        print(e)
        return HttpResponse('2')

@csrf_exempt
def add_device_repair(request):
    try:
        dr_num = request.POST.get('data[t_device]')
        dr_start = request.POST.get('data[dr_start]') or None
        dr_end = request.POST.get('data[dr_end]') or None
        dr_user = request.POST.get('data[dr_user]') or None
        dr_des = request.POST.get('data[dr_des]') or None
        dr_start = re.sub(r'[：]+', ":", dr_start)
        dr_end = re.sub(r'[：]+', ":", dr_end)
        D = DeviceMd.objects.filter(d_num=dr_num)
        d = DeviceRepair()
        print(dr_num, dr_start, dr_end, dr_user, dr_des)
        d.dr_num = D.first()
        d.dr_start = dr_start
        d.dr_end = dr_end
        d.dr_user = dr_user
        d.dr_des = dr_des
        d.save()
        return HttpResponse("1")
    except Exception as e:
        print(e)
        return HttpResponse("2")

@csrf_exempt
def add_order(request):
    try:
        product_id = request.POST.get('data[product_id]')
        customer = request.POST.get('data[customer]')
        product_name = request.POST.get('data[product_name]')
        product_count = request.POST.get('data[product_count]')
        product_start = request.POST.get('data[product_start]')
        product_end = request.POST.get('data[product_end]')
        product_des = request.POST.get('data[product_des]')

        # d1 = datetime.datetime.strptime(product_start, '%Y-%m-%d %H:%M:%S')
        d1 = datetime.datetime.strptime(product_start, '%Y-%m-%d')
        d2 = datetime.datetime.strptime(product_end, '%Y-%m-%d')

        # 调用delta的days属性即可得到int值
        interval = (d2-d1).days
        int_day = interval if interval > 0 else 1
        o_exit = Order.objects.filter(o_id=product_id)
        if o_exit:
            return HttpResponse('0')
        o = Order()
        o.o_id = product_id
        o.o_customer = customer
        o.o_name = product_name
        o.o_count = product_count
        o.o_start = product_start
        o.o_end = product_end
        o.o_day = int_day
        o.o_des = product_des
        o.save()
        return HttpResponse("1")
    except Exception as e:
        print(e)
        return HttpResponse("2")

@csrf_exempt
def edit_order(request):
    try:
        order_id = request.POST.get('data[order_id]')
        customer = request.POST.get('data[customer]')
        product_count = request.POST.get('data[product_count]')
        product_start = request.POST.get('data[product_start]')
        product_end = request.POST.get('data[product_end]')
        product_des = request.POST.get('data[product_des]')
        d1 = datetime.datetime.strptime(product_start, '%Y-%m-%d')
        d2 = datetime.datetime.strptime(product_end, '%Y-%m-%d')

        # 调用delta的days属性即可得到int值
        interval = (d2 - d1).days
        int_day = interval if interval > 0 else 1
        order_id = int(order_id)

        o = Order.objects.get(id=order_id)
        o.o_customer = customer
        o.o_count = product_count
        o.o_start = product_start
        o.o_end = product_end
        o.o_day = int_day
        o.o_des = product_des
        o.save()
        return HttpResponse("1")
    except Exception as e:
        print(e)
        return HttpResponse("2")

@csrf_exempt
def order_dispense(request):
    try:
        order_id = request.POST.get('data[order_id]')
        device_id = request.POST.get('data[device_id]')
        if device_id == '0':
            od = OrderDevice.objects.filter(o_id=order_id, od_active=True).first()
            if od:
                od.od_active = False
                od.save()
                device = DeviceMd.objects.get(id=od.d_id)
                order = Order.objects.get(id=od.o_id)
                order.o_status = 5 # 订单状态为5表示，分发之后又解除机台
                order.save()
                return HttpResponse('3')
            else:
                return HttpResponse('4')
        else:
            # device_id = DeviceMd.objects.filter(d_num=t_device).first()
            od = OrderDevice.objects.filter(d_id=device_id, od_active=True).first()
            if not od:
                device = DeviceMd.objects.get(id=device_id) # 找到机台对象
                order = Order.objects.get(id=order_id) # 找到订单 并设置其状态
                order.o_status = 2
                order.save()
                od = OrderDevice() # 创建对象
                od.o_id = order_id
                od.d_id = device_id
                od.o_k = order
                od.d_k = device
                od.save()
                return HttpResponse("1") # 正常分配
            else:
                return HttpResponse("5") # 机台已经分配
    except Exception as e:
        print(e)
        return HttpResponse("2") # 意外错误

@csrf_exempt
def add_device(request):
    try:
        device_num = request.POST.get('data[device_num]')
        device_model = request.POST.get('data[device_model]')
        device_brank = request.POST.get('data[device_brank]')
        device_name = request.POST.get('data[device_name]')
        device_date = request.POST.get('data[device_date]')
        device_user = request.POST.get('data[device_user]')

        # d1 = datetime.datetime.strptime(product_start, '%Y-%m-%d %H:%M:%S')
        d1 = datetime.datetime.strptime(device_date, '%Y-%m-%d %H:%M:%S')

        device_user = UserInfo.objects.get(uname=device_user)
        u = User.objects.get(u_info=device_user)

        d = DeviceMd()
        d.d_type = 1
        d.d_num = device_num
        d.d_brank = device_brank
        d.d_model = device_model
        d.d_name = device_name
        d.d_status = 3
        d.d_created = d1
        d.d_user = u
        d.save()
        return HttpResponse("1")
    except Exception as e:
        print(e)
        return HttpResponse("2")

@csrf_exempt
def change_status(request):
    try:
        device_id = request.POST.get('device_id')
        change_status = request.POST.get('change_status')
        d = DeviceMd.objects.get(id=device_id)
        if change_status != '0':
            d.d_status = change_status
            d.save()  # 注塑机运行状态改变
        try:
            od = OrderDevice.objects.get(d_id=device_id, od_active=True)  # 判断此机器是否分配了工单
            changed_id = od.o_k.id  # 获取工单ID
            if change_status == '1':
                od.o_k.o_status = 3  # 工单状态切换为 生产中
                od.o_k.save()
                # 启动任务
                task = sendtime.delay(device_id, changed_id)
                task_id = task.id
                od.od_taskid = task_id
                od.save()
                print(task_id)
            elif change_status == '0':
                # print('此机器已在运行，不需要改动')
                pass
            else:
                od.o_k.o_status = 2  # 工单状态切换为 暂停中
                od.o_k.save()
                task_id = od.od_taskid
                if task_id:
                    celery_app.control.revoke(task_id, terminate=True)
        except Exception as e:
            # print(e,'---不存在工单')
            pass
        return HttpResponse("1")
    except Exception as e:
        print(e)
        return HttpResponse("2")

