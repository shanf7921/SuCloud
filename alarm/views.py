import random
import time

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from device.models import DeviceMd

# 发送邮件
import smtplib
from email.mime.text import MIMEText
# Create your views here.
from alarm.models import ParamTime, ParamError, ParamSet


def alarm_rule1(request):
    m = DeviceMd.objects.filter(id=2).first()
    pe = ParamError.objects.filter(t_device=m).first()
    ps = ParamSet.objects.filter(t_device=m).first()
    pts = ParamTime.objects.filter(t_device=m)
    for pt in pts:
        if pe.e_place:
            place1 = abs(ps.t_open_place - pt.t_open_place)
            if place1 > pe.e_place:
                ctime = pt.t_created
                ctime = str(ctime)
                send_mail_qq(request, m.d_num, '位置', ctime)

                print('位置 超出误差')
        if pe.e_tem:
            tem1 = abs(ps.t_tem1 - pt.t_tem1)
            tem2 = abs(ps.t_tem2 - pt.t_tem2)
            tem3 = abs(ps.t_tem3 - pt.t_tem3)
            tem4 = abs(ps.t_tem4 - pt.t_tem4)
            tem5 = abs(ps.t_tem5 - pt.t_tem5)
            if tem1 > pe.e_tem or tem2 > pe.e_tem or tem3 > pe.e_tem or tem4 > pe.e_tem or tem5 > pe.e_tem:
                ctime = pt.t_created
                ctime = str(ctime)[0:-6]
                send_mail_qq(request, m.d_num, '温度', ctime)
                print('温度 超出误差')
    return render(request, 'alarm/alarm_rule.html')

def alarm_rule(request):
    rules = ParamError.objects.all()
    devices = DeviceMd.objects.all()
    return render(request, 'alarm/alarm_rule.html', {"rules": rules, "devices":devices})


def alarm_warm(request):
    devices = DeviceMd.objects.all()
    return render(request, "alarm/alarm_warm.html", {"devices": devices})


def alarm_record(request):
    perrors_list = ParamTime.objects.filter(t_error=True).order_by('-id')
    page_len = len(perrors_list)
    count_page = 6
    paginator = Paginator(perrors_list, count_page)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        perrors = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        page = 1
        perrors = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        perrors = current_page.object_list
    start = (int(page) - 1) * count_page
    return render(request, 'alarm/alarm_record.html', {"perrors": perrors, "page":current_page, "start":start, "page_len":page_len})

def send_mail_qq(num, param, ctime, remind=["AngusCelt@outlook.com", "anf57@hotmail.com"]):
    # 服务器
    SMTPserver = "smtp.qq.com"
    # 发送邮件的地址
    sender = "2106398886@qq.com"
    # 授权密码
    password = "iendyglxymgjbjjh"

    # msg_to = ['anf57@hotmail.com']
    Message = "编号为"+num+"的机器" +param+"参数超出预定值"+"\n记录产生的时间为"+ctime

    # 转为邮件文本
    msg = MIMEText(Message)
    # 主题
    msg["Subject"] = "报警提示"
    # 邮件的发送者
    msg["From"] = sender
    # msg["To"] = msg_to

    # 连接服务器
    mailServer = smtplib.SMTP(SMTPserver, 25)
    try:
        # 登录
        mailServer.login(sender, password)
        # 发送
        mailServer.sendmail(sender, remind, msg.as_string())
        print("邮件发送成功")
    except Exception as e:
        print('---1---')
        print(e)
        print('---2---')
    finally:
        mailServer.quit()

def generate_param():
    i = 0
    while True:
        # 0~5的随机数
        r5 = random.random() * 5.2
        r10 = random.random() * 10.2
        r5 = float('%.2f' % r5)
        r10 = float('%.2f' % r10)
        t_open_place = 500
        t_open_place = float('%.2f' % (t_open_place + r10))

        g = ParamTime()
        id_list = [1,2,3,4,6,7,8,9]
        id = random.randrange(len(id_list))
        id = id_list[id]
        m = DeviceMd.objects.filter(id=id).first()
        g.t_device = m
        g.t_all = 88.09
        g.t_open_mold = 3.24
        g.t_close_mold = 6.05
        g.t_stock = 22.03
        g.t_ejection = 22.02
        g.t_back = 0.58
        g.t_change = 7.02

        g.t_change_place = 25.00
        g.t_change_pressure = 728

        g.t_tem1 = 220
        g.t_tem2 = 220 
        g.t_tem3 = 218 + r5
        g.t_tem4 = 200
        g.t_tem5 = 200

        g.t_open_place = t_open_place
        g.t_ejection1 = 141.5
        g.t_ejection2 = 10.1
        g.save()
        i +=1
        print('生产%s条数据'%i, t_open_place,g.t_tem3, r5, r10 ,"----",id)
        time.sleep(2)
        if r10 > 10:
            print('-------------10')
        if r5 > 5:
            print('-------------5')

def check_error(request):
    # 得到所有机台（后续筛选出 运行机台）
    device_list = DeviceMd.objects.all()
    for m in device_list:
        pe = ParamError.objects.filter(t_device=m, e_error=True).first()
        # 如果pe存在说明此台机器设置并启动了报警规则
        if pe:
            remind = pe.e_remind.split()  # 获取e_remind字段，并转为列表
            ps = ParamSet.objects.filter(t_device=m).first()  # 获取机台参数的设定值
            pts = ParamTime.objects.filter(t_device=m)  # 获取机台参数的实时变化值
            for pt in pts:
                time.sleep(2)
                # 如果设置了位置参数 则进行校验
                if pe.e_place and ps.t_open_place:
                    place1 = abs(ps.t_open_place - pt.t_open_place)
                    if place1 > pe.e_place:
                        pt.t_error = True  # 将错误记录标记
                        pt.save()  # 修改数据库后进行保存
                        ctime = pt.t_created
                        ctime = str(ctime)
                        send_mail_qq(request, m.d_num, '位置', ctime, remind)
                        print(pt.id, m.d_num)
                        print('位置 超出误差')
                        print('---------------')
                # 如果设置了温度参数 则进行校验
                if pe.e_tem:
                    tem1 = abs(ps.t_tem1 - pt.t_tem1)
                    tem2 = abs(ps.t_tem2 - pt.t_tem2)
                    tem3 = abs(ps.t_tem3 - pt.t_tem3)
                    tem4 = abs(ps.t_tem4 - pt.t_tem4)
                    tem5 = abs(ps.t_tem5 - pt.t_tem5)
                    if tem1 > pe.e_tem or tem2 > pe.e_tem or tem3 > pe.e_tem or tem4 > pe.e_tem or tem5 > pe.e_tem:
                        pt.t_error = True  # 将错误记录标记
                        pt.save()  # 修改数据库后进行保存
                        ctime = pt.t_created
                        ctime = str(ctime)[0:-6]
                        send_mail_qq(request, m.d_num, '温度', ctime, remind)
                        print(pt.id, m.d_num)
                        print('温度 超出误差')
                        print('---------------')