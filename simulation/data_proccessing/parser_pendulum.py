#!/usr/bin/env python3
import sys, os
import csv
import optparse
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np

usage = """Script to convert csv file with walking data to list.
Place the csv file at data folder"""""

p = optparse.OptionParser(usage=usage)
p.add_option("-f", "--file", dest="filename",
                  help="csv file name with walk info. Must be at data folder", metavar="FILE")
p.set_defaults(filename="walk1.csv")
(opts, args) = p.parse_args()

sys.path.append(os.path.join(os.path.dirname(__file__), "physical"))
sys.path.append(os.path.join(os.path.dirname(__file__), "fuzzy"))
root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_folder = os.path.join(root,"simulation","data","dpc_dataset_csv")
dp_file = os.path.join(data_folder,opts.filename)

def dp_parser(path_to_dp_file):
    with open(path_to_dp_file) as file:
        dp_data_temp = csv.reader(file)
        dp_keys = ['x_red', 'y_red', 'x_green', 'y_green', 'x_blue', 'y_blue']
        dp_data = {'x_red': [], 'y_red': [], 'x_green': [], 'y_green': [], 'x_blue': [], 'y_blue': []}
        for data in dp_data_temp:
            for index, key in enumerate(dp_data):
                dp_data[key].append(float(data[index]))
        dp_data_pol = dp_cartesian2pol(dp_data)
    return dp_data_pol

def dp_cartesian2pol(dp_data):
    dp_keys_pol = ['hip angle', 'ankle angle 2']
    dp_data_pol = {'hip angle': [], 'ankle angle': []}
    for index in range(len(dp_data['x_red'])):
        alfa_oposite = dp_data['x_green'][index] - dp_data['x_red'][index]
        alfa_adjacent = dp_data['y_green'][index] - dp_data['y_red'][index]
        if alfa_adjacent == 0:
            alfa_adjacent = 0.0000000000001;
        alfa = np.arctan(alfa_oposite/alfa_adjacent)
        if alfa_adjacent > 0 :
            #angle in 1st or 4th quadrant
            if alfa_oposite > 0:
                #1st quadrant
                alfa = np.pi - alfa
            elif alfa_oposite < 0:
                #4th quadrant
                alfa = alfa + np.pi
        elif alfa_adjacent < 0:
            #angle in 2nd or 3rd quadrant
            if alfa_oposite > 0:
                #angle in 2nd quadrant
                pass
            elif alfa_oposite < 0:
                #angle in 3rd quadrant
                alfa = alfa * -1
                pass

        alfa = np.arctan(alfa_oposite/alfa_adjacent) 
        if (alfa > 0):
            alfa = alfa - np.pi/2
        elif (alfa < 0):
            alfa = alfa + np.pi/2

        #alfa = np.arctan(alfa_oposite/alfa_adjacent)
        alfa = np.rad2deg(alfa)
        #dp_data_pol['alfa'].append(alfa)
        beta_oposite = dp_data['x_green'][index] - dp_data['x_blue'][index]
        beta_adjacent = dp_data['y_green'][index] - dp_data['y_blue'][index]
        if beta_adjacent == 0:
            beta_adjacent = 0.0000000000001;
        beta = np.arctan(beta_oposite/beta_adjacent)

        if (beta > 0):
            beta = beta - np.pi/2
        elif (beta < 0):
            beta = beta + np.pi/2


        beta = np.rad2deg(beta)
        
        alfa = np.arccos(alfa_oposite/np.sqrt(alfa_adjacent**2+alfa_oposite**2)) 
        beta = np.arccos(beta_oposite/np.sqrt(beta_adjacent**2+beta_oposite**2))
        if alfa_adjacent > 0 :
            #angle in 1st or 4th quadrant
            if alfa_oposite > 0:
                #1st quadrant
                alfa = alfa * -1
            elif alfa_oposite < 0:
                #4th quadrant
                alfa = alfa * -1
        elif alfa_adjacent < 0:
            #angle in 2nd or 3rd quadrant
            if alfa_oposite > 0:
                #angle in 2nd quadrant
                alfa = alfa
            elif alfa_oposite < 0:
                #angle in 3rd quadrant
                alfa = alfa 

        if beta_adjacent > 0 :
            #angle in 1st or 4th quadrant
            if beta_oposite > 0:
                #1st quadrant
                beta = beta * -1
            elif beta_oposite < 0:
                #4th quadrant
                beta = beta * -1
        elif beta_adjacent < 0:
            #angle in 2nd or 3rd quadrant
            if beta_oposite > 0:
                #angle in 2nd quadrant
                beta = beta
            elif beta_oposite < 0:
                #angle in 3rd quadrant
                beta = beta 




        beta = np.rad2deg(beta)
        alfa = np.rad2deg(alfa)
        dp_data_pol['hip angle'].append(alfa)
        dp_data_pol['ankle angle'].append(beta)
    return dp_data_pol

def walk_interpolation(walk_data, dt=0.1):
    t2 = np.arange(0.0, 100, dt)
    walk_data_interpolation = {'Ankle Angle': [], 'Hip Angle': [], 'Knee Angle': [], 'Ankle Momentum': [], 'Hip Momentum': [], 'Knee Momentum': [], 'Ankle Power': [], 'Hip Power': [], 'Knee Power': []}
    for key in walk_data.keys():
        t = range(len(walk_data[key]))
        fun = interp1d(t, walk_data[key], kind='cubic')
        walk_data_interpolation[key] = fun(t2)
    return walk_data_interpolation

        

if __name__ == "__main__":
    dp_data = dp_parser(dp_file)
    dp_data_pol = dp_cartesian2pol(dp_data)
    t = np.arange(0, len(dp_data_pol['alfa']), 1)
    fig = plt.figure()
    ax = fig.add_subplot(2,1,1)
    ax.plot(t, dp_data_pol['alfa'])
    ax = fig.add_subplot(2,1,2)
    ax.plot(t, dp_data_pol['beta'])
    plt.show()
    print(dp_data.keys()) 
    for key in dp_data.keys():
        print(len(dp_data[key]))
