import datetime
import time
import os, sys
import yaml
import numpy as np
import ephem
import argparse
from prettytable import PrettyTable
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def reflash_table(table):
    table.clear_rows()
    all_object = {**Stars, **Planets}
    for name, s in all_object.items():
        ra = "%.4f" % (s.ra * 180 / np.pi)
        dec = "%.4f" % (s.dec * 180 / np.pi)
        az = "%.4f" % (s.az * 180 / np.pi)
        alt = "%.4f" % (s.alt * 180 / np.pi)
        if float(alt) < 0:
            obs = "不可见"
        elif 0 <= float(alt) < 10:
            obs = "较低"
        elif 0 <= float(alt) < 30:
            obs = "观测警告"
        elif 0 <= float(az) < 45 or 315 <= float(az) <=360:
            obs = "北"
        elif 45 <= float(az) < 135:
            obs = "东"
        elif 135 <= float(az) < 225:
            obs = "南"
        elif 225 <= float(az) < 315:
            obs = "西"
        table.add_row([name, ra, dec, az, alt, obs])
    #清屏操作
    os.system('cls' if os.name == 'nt' else 'clear')
    #输出   
    sys.stdout.write(table.get_string())
    sys.stdout.flush()
    sys.stdout.write("\n")

def reflash_paint():
    plt.cla()
    ax.axis([0, 360, -90, 90])
    plt.xlabel('Azimuth')
    plt.ylabel('Altitude')
    ax.axhline(y=0,ls="-")  # 水平直线
    for name, p in Planets.items():
        az = p.az * 180 / np.pi
        alt = p.alt * 180 / np.pi
        ax.annotate(name, (az+3, alt+3))
        if name == "Sun":
            ax.scatter(az, alt, s=100, c="r", alpha=0.8, marker="o")
        elif name == "Moon":
            ax.scatter(az, alt, s=80, c="y", alpha=0.8, marker="o")
        elif name == "Jupiter":
            ax.scatter(az, alt, s=30, c="b", alpha=0.8, marker="o")
        else:
            ax.scatter(az, alt, s=50, c="b", alpha=0.8, marker=".")
    for name, s in Stars.items():
        az = s.az * 180 / np.pi
        alt = s.alt * 180 / np.pi
        ax.annotate(name, (az+3, alt+3))
        ax.scatter(az, alt, s=50, c="m", alpha=0.8, marker="*")
    figure.canvas.draw()
    figure.canvas.flush_events()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", required=True)
    args = parser.parse_args()
    with open(args.config, "r", encoding="utf-8") as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
    # 太阳系
    Planets = {
        "Sun": ephem.Sun(),
        "Moon": ephem.Moon(),
        "Mercury": ephem.Mercury(),
        "Venus": ephem.Venus(),
        "Mars": ephem.Mars(),
        "Jupiter": ephem.Jupiter(),
        "Saturn": ephem.Saturn(),
        "Uranus": ephem.Uranus(),
        "Neptune": ephem.Neptune(),
        "Pluto": ephem.Pluto(),
    }
    # 自定义天体
    Stars = {}
    for body in config["stars"]:
        name = body["name"]
        ra = body["Ra"]
        dec = body["Dec"]
        fixbody = ephem.FixedBody()
        fixbody._ra = ra
        fixbody._dec = dec
        Stars[name] = fixbody
        
    # 观察者
    Observer = ephem.Observer()
    Observer.lon = config["observer"]["longitude"]
    Observer.lat = config["observer"]["latitude"]
    Observer.elevation = config["observer"]["elevation"]
    Observer.pressure = config["observer"]["pressure"] 
    # 表格
    table = PrettyTable(['Source','Ra赤经','Dec赤纬','Az方位', 'Alt仰角', '观测'])
    table.padding_width = 5
    # 图
    plt.ion()
    figure, ax = plt.subplots()
    # 刷新
    while True:
        try:
            Observer.date = "%s"%datetime.datetime.utcnow() #观察时间
            for name, p in Planets.items():
                p.compute(Observer)
            for name, s in Stars.items():
                s.compute(Observer)
            reflash_table(table)
            reflash_paint()
            plt.pause(1)
            time.sleep(4)
        except KeyboardInterrupt:
            break
    plt.close()