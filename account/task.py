import random
import time

from SuCloud import celery_app
from alarm.models import ParamTime, ParamError, ParamSet
from alarm.views import send_mail_qq
from device.models import DeviceMd
from produce.models import Order

@celery_app.task
def sendtime(device_id, order_id):
    # 看当前机器是否设置了工艺参数值
    ps = DeviceMd.objects.get(id=device_id).paramset.first()
    print('%s机器正在运行......' % (DeviceMd.objects.get(id=device_id).d_num))
    if ps:
        ps_time = int(ps.s_all)  # 取整 得到睡眠时间
        ps_id = ps.id
        while True:
            t = time.sleep(ps_time)
            # 调用函数，生成一条数据
            generate_param(device_id, ps_id)
            # 找到订单，完成数量加1
            o = Order.objects.get(id=order_id)
            o.o_finish += 1
            o.save()
            if o.o_finish >= o.o_count:
                o.o_status = 4
                o.save()
            # 实时工艺参数生产
            print('---1---此时生产的产品为：%s,当前生产总量为：%s' % (o.o_name, o.o_finish))
            # 调用函数，检查生成的数据
            check_error(device_id)
    else:
        time_list = [45, 60, 50]
        sel = random.choice(time_list)
        while True:
            t = time.sleep(sel)
            o = Order.objects.get(id=order_id)
            o.o_finish += 1
            o.save()
            if o.o_finish >= o.o_count:
                o.o_status = 4
                o.save()
            # 实时工艺参数生产
            print('---2---此时生产的产品为：%s,当前生产总量为：%s' % (o.o_name, o.o_finish), sel)

def generate_param(device_id, ps_id):
    # 判断此台机器是否设定了容错规则
    pe_exit = DeviceMd.objects.get(id=device_id).paramerror.first()
    if pe_exit:
        time_error = pe_exit.e_time or 0
        tem_error = pe_exit.e_tem or 0
        place_error = pe_exit.e_place or 0
        pre_error = pe_exit.e_pressure or 0
    else:
        time_error = 0
        tem_error = 0
        place_error = 0
        pre_error = 0
    # 容错值加0.2 乘以随机数
    """后面为了生成实时参数(即每生成一次产品，产生一条记录)"""
    r_time = random.random() * (time_error+0.2)
    r_tem = random.random() * (tem_error+0.2)
    r_place = random.random() * (place_error+0.2)
    r_pre = random.random() * (pre_error+0.2)
    # 保留两位小数
    r_time = float('%.2f' % r_time)
    r_tem = float('%.2f' % r_tem)
    r_place = float('%.2f' % r_place)
    r_pre = float('%.2f' % r_pre)

    g = ParamTime()
    # 选择当前机台
    device = DeviceMd.objects.filter(id=device_id).first()
    ps = ParamSet.objects.get(id=ps_id)

    g.t_device = device
    g.t_all = random.choice((ps.s_all + r_time, ps.s_all - r_time))
    t_open_mold = random.choice((ps.t_open_mold + r_place, ps.t_open_mold - r_place))
    g.t_open_mold = float('%.2f' % t_open_mold)
    t_close_mold = random.choice((ps.t_close_mold + r_place, ps.t_close_mold - r_place))
    g.t_close_mold = float('%.2f' % t_close_mold)
    g.t_stock = round(random.choice((ps.t_stock + r_time, ps.t_stock - r_time)), 2)
    g.t_ejection = round(random.choice((ps.t_ejection + r_time, ps.t_ejection - r_time)), 2)
    g.t_back = round(random.choice((ps.t_back + r_time, ps.t_back - r_time)), 2)
    g.t_change = random.choice((ps.t_change + r_time, ps.t_change - r_time))

    g.t_change_place = random.choice((ps.t_change_place + r_place, ps.t_change_place - r_place))
    g.t_change_pressure = random.choice((ps.t_change_pressure + r_pre, ps.t_change_pressure - r_pre))

    g.t_tem1 = round(random.choice((ps.t_tem1 + r_tem, ps.t_tem1 - r_tem)))
    g.t_tem2 = round(random.choice((ps.t_tem2 + r_tem, ps.t_tem2 - r_tem)))
    g.t_tem3 = round(random.choice((ps.t_tem3 + r_tem, ps.t_tem3 - r_tem)))
    g.t_tem4 = round(random.choice((ps.t_tem4 + r_tem, ps.t_tem4 - r_tem)))
    g.t_tem5 = round(random.choice((ps.t_tem5 + r_tem, ps.t_tem5 - r_tem)))

    g.t_open_place = random.choice((ps.t_open_place + r_place, ps.t_open_place - r_place))
    g.t_ejection1 = round(random.choice((ps.t_ejection1 + r_place, ps.t_ejection1 - r_place)), 2)
    g.t_ejection2 = round(random.choice((ps.t_ejection2 + r_place, ps.t_ejection2 - r_place)), 2)
    g.save()
    print('%s生产一件产品，周期为:%d秒' % (device.d_num, g.t_all))
    print('三段温度：%s,开模位置：%s,转保压压力：%s,注射时间：%s'
          % (g.t_tem3, g.t_open_place, g.t_change_pressure, g.t_ejection))


def check_error(device_id):
    print('检测此条数据是否超出误差...')
    # 得到当前设备
    device = DeviceMd.objects.get(id=device_id)
    pe = ParamError.objects.filter(t_device=device, e_error=True).first()
    # 如果pe存在说明此台机器设置并启动了报警规则
    if pe:
        remind = pe.e_remind.split()  # 获取e_remind字段，并转为列表
        ps = ParamSet.objects.filter(t_device=device).first()  # 获取机台参数的设定值
        pt = ParamTime.objects.filter(t_device=device).last()  # 获取机台参数的最新的一条值
        error_list = []  # 定义一个列表，存储出错的参数名称（温度、压力、位置、时间）

        # 如果设置了位置参数 则进行校验
        if pe.e_place and ps.t_open_place:
            place1 = abs(ps.t_open_place - pt.t_open_place)
            if place1 > pe.e_place:
                pt.t_error = True  # 将错误记录标记
                pt.save()
                error_list.append('位置')
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
                error_list.append('温度')
        # 压力
        if pe.e_pressure:
            pressure1 = abs(ps.t_change_pressure - pt.t_change_pressure)
            if pressure1 > pe.e_pressure:
                pt.t_error = True  # 将错误记录标记
                pt.save()  # 修改数据库后进行保存
                error_list.append('压力')
        # 时间
        if pe.e_time:
            time1 = abs(ps.t_open_mold - pt.t_open_mold)
            time2 = abs(ps.t_close_mold - pt.t_close_mold)
            time3 = abs(ps.t_stock - pt.t_stock)
            time4 = abs(ps.t_ejection - pt.t_ejection)
            time5 = abs(ps.t_back - pt.t_back)
            time6 = abs(ps.t_change - pt.t_change)
            if time1 > pe.e_time or time2 > pe.e_time or time3 > pe.e_time or time4 > pe.e_time or time5 > pe.e_time  or time6 > pe.e_time:
                pt.t_error = True  # 将错误记录标记
                pt.save()  # 修改数据库后进行保存
                error_list.append('时间')
        if error_list:
            param = "、".join(error_list)
            ctime = pt.t_created
            ctime = str(ctime)[0:-6]
            send_mail_qq(device.d_num, param, ctime, remind)
            print('-----------Email----------')
        else:
            print('------------Ok------------')
    else:
        print('---------------------*---------------OK-')




