#!/usr/bin/env python3

import os
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import odeint, solve_ivp
from pid_class import PID
import matplotlib.pyplot as plt
import csv
import optparse
import collections
import pickle
import time

epocas, max_membership, t_minus_1 = None, None, None

start_time = time.time()
usage = """Script to convert csv file with walking data to list.
Place the csv file at data folder"""""

p = optparse.OptionParser(usage=usage)
p.add_option("-f", "--file", dest="filename",
                  help="csv file name with walk info. Must be at data folder", metavar="FILE")
p.set_defaults(filename="Subject1.mat")
(opts, args) = p.parse_args()

def mean_squared_error(array1,array2):
    difference_array = np.subtract(array1, array2)
    squared_array = np.square(difference_array)
    mse = squared_array.mean()
    return mse

def delay_list(data_list, i):
    temp_list = collections.deque(data_list)
    temp_list.rotate(i)
    data_list_delay= list(temp_list)
    for j in range(i):
        data_list_delay[j] = 0
    return data_list_delay

def setup():
    global model, fuzzy, walk_file, walk_parser, walk_interpolation, epocas, max_membership, t_minus_1
    this_file_loc = os.path.abspath(__file__)
    this_file_path = Path(this_file_loc)
    simulation_folder = this_file_path.parents[0]
    sys.path.append(f"{simulation_folder}/physical")
    sys.path.append(f"{simulation_folder}/fuzzy")
    sys.path.append(f"{simulation_folder}/data_proccessing")
    walk_file = f"{simulation_folder}/data/{opts.filename}"
    import model as model
    from fuzzy import fuzzy
    from parser_mat import walk_parser

    epocas = 3
    max_membership = 200
    t_minus_1 = 1

def trainning():

    walk_data = walk_parser(walk_file)
    momentum = {
        "hip": walk_data["steps"][0]["momentum"]["hip"],
        "knee": walk_data["steps"][0]["momentum"]["knee"]
    }
    angle = {
        "hip": [np.deg2rad(an) for an in walk_data["steps"][0]["angle"]["hip"]],
        "knee": [np.deg2rad(an) for an in walk_data["steps"][0]["angle"]["knee"]]
    }
    t = walk_data["steps"][0]["time"]
    time_holder = t
    angle_holder = angle

    total_inputs = [
        angle["hip"],
        angle["knee"],
        t,
        delay_list(angle["hip"],1),
        delay_list(angle["hip"],2),
        delay_list(angle["hip"],3),
        delay_list(angle["knee"],1),
        delay_list(angle["knee"],2),
        delay_list(angle["knee"],3),
        delay_list(t,1),
        delay_list(t,2),
        delay_list(t,3),
    ]
    output = momentum["hip"]
    t = time_holder
    angle = angle_holder
    fuzzy_answer_hip = fuzzy(total_inputs,output,epocas=epocas,max_membership=max_membership)

    output = momentum["knee"]
    fuzzy_answer_knee = fuzzy(total_inputs,output,epocas=epocas,max_membership=max_membership)

    return fuzzy_answer_hip, fuzzy_answer_knee, walk_data

def plot_graphs(fuzzy_answer_hip, fuzzy_answer_knee, walk_data):
    global epocas, max_membership, t_minus_1
    #generate "time" array
    t = walk_data["steps"][0]["time"]
    momentums = {
        "Hip": walk_data["steps"][0]["momentum"]["hip"],
        "Knee": walk_data["steps"][0]["momentum"]["knee"]
    }
    angles = {
        "Hip": walk_data["steps"][0]["angle"]["hip"],
        "Knee": walk_data["steps"][0]["angle"]["knee"]
    }

    plt.subplot(1, 1, 1)
    plt.plot(t, momentums['Hip'], 'g', label='Refer??ncia')
    plt.plot(t, fuzzy_answer_hip, 'r', label='Rede neural')
    plt.annotate(f"MSE: {mean_squared_error(momentums['Hip'],fuzzy_answer_hip):.3}",(0,-0.3))
    plt.title('Torque gerado pela rede neo-nebulosa para o quadril')
    plt.ylabel('Torque (Nm)')
    plt.xlabel('Tempo (s)')
    plt.grid()
    plt.legend(loc="best")

    # when saving, specify the DPI
    #plt.savefig(f"epocas_{epocas}_membership_{max_membership}_delays_{t_minus_1}.png", dpi = 200)
    figure = plt.gcf() # get current figure
    figure.set_size_inches(10.8, 7.2)
    plt.show()

    plt.subplot(1, 1, 1)
    plt.plot(t, momentums['Knee'], 'g', label='Refer??ncia')
    plt.plot(t, fuzzy_answer_knee, 'r', label='Rede neural')
    plt.annotate(f"MSE: {mean_squared_error(momentums['Knee'],fuzzy_answer_knee):.3}",(0,-0.3))
    plt.title('Torque gerado pela rede neo-nebulosa para o joelho')
    plt.ylabel('Torque (Nm)')
    plt.xlabel('Tempo (s)')
    plt.grid()
    plt.legend(loc="best")

    #plt.savefig(f"epocas_{epocas}_membership_{max_membership}_delays_{t_minus_1}.png", dpi = 200)
    figure = plt.gcf() # get current figure
    figure.set_size_inches(10.8, 7.2)
    plt.show()
    

def main():
    setup()
    fuzzy_answer_hip, fuzzy_answer_knee, walk_data = trainning()
    print("--- Trainning took %s seconds ---" % (time.time() - start_time))
    plot_graphs(fuzzy_answer_hip, fuzzy_answer_knee, walk_data)

def get_angles_trainned():
    setup()
    trainning()
    print("--- Trainning took %s seconds ---" % (time.time() - start_time))
    return fuzzy_answer
    
if __name__ == "__main__":
    main()

    
