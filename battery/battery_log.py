#!/home/dylan/anaconda3/envs/battery/bin/python

import psutil
import csv
import datetime
import time as t

file_path = '/home/dylan/PycharmProjects/battery/'

def get_battery():
    battery = psutil.sensors_battery()

    plugged = battery.power_plugged
    percent = battery.percent
    time = datetime.datetime.now()


    # print(percent+'% | '+plugged)
    return time, percent, plugged

while True:

    with open(file_path+'battery_logs.csv', mode='a') as logs:
        writer = csv.writer(logs, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        time, percent, plugged = get_battery()
        writer.writerow([time, percent, plugged])

    t.sleep(120)
