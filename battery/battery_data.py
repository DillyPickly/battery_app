#!/home/dylan/anaconda3/envs/battery/bin/python

import csv
from datetime import datetime,timedelta
# import matplotlib.pyplot as plt
import numpy as np

def update_data():
    array = []

    file_path = '/home/dylan/PycharmProjects/battery/'

    with open(file_path+'battery_logs.csv', mode='r') as logs:
            reader = csv.reader(logs, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for row in reader:
                array.append([row[0],row[1],row[2]])

    return np.array(array)


def get_data(array):
    
    date_time = []
    for t_str in array[:,0]:
        date = datetime.strptime(t_str, '%Y-%m-%d %H:%M:%S.%f')
        date_time.append(date)

    # # base data
    date_time = np.asarray(date_time)
    percent = np.asarray(array[:,1], dtype=float)
    plugged = array[:,2] == 'True'

    on_battery = date_time[plugged], percent[plugged]
    off_battery = date_time[plugged^True], percent[plugged^True]

    return date_time, percent, plugged, on_battery, off_battery


def date_limits(date_time, percent, plugged, on_battery, off_battery, delta = timedelta(days=1)):
    now = datetime.now()
    indices = []
    
    for i in range(len(date_time)):
        if now - date_time[i] < delta :
            indices.append(i)
            
#     print(indices)
    date_time_out   = date_time[indices]
    percent_out     = percent[indices]
    plugged_out     = plugged[indices]
    
    on_battery_out  = date_time_out[plugged_out],      percent_out[plugged_out]
    off_battery_out = date_time_out[plugged_out^True], percent_out[plugged_out^True]            
            
    return date_time_out, percent_out, plugged_out, on_battery_out, off_battery_out