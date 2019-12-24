from alarm.models import ParamTime


def generate_param():
    g = ParamTime()
    g.t_device = 2
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
    g.t_tem3 = 218
    g.t_tem4 = 200
    g.t_tem5 = 200

    g.t_open_place = 506
    g.t_ejection1 = 141.5
    g.t_ejection2 = 10.1
    g.save()
    print('生产一条数据')

if __name__ == "__main__":
    generate_param()