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



start_time = time.time()

#================== INSTRUCTIONS AND OPTIONS ===================================
usage = """Script to train a neural network with step 
data using the .mat files on data folder"""

parser = optparse.OptionParser(usage)
parser.add_option("-f",
            "--file",
            dest="filename",
            help="csv file name with walk info. Must be at data folder",
            metavar="FILE")
parser.add_option("-e",
            "--epocas",
            dest="epocas",
            help="number of epocas to neuron network train")
parser.add_option("-d",
            "--delays",
            dest="delays",
            help="number of time delays to apply on each input signal")
parser.add_option("-m",
            "--max",
            dest="max_membership",
            help="maximum number of membership functinos for each neuron")

parser.set_defaults(filename="Subject1.mat")
parser.set_defaults(epocas=2)
parser.set_defaults(delays=3)
parser.set_defaults(max_membership=200)

(opts, args) = parser.parse_args()
#(opts, args) = p.parse_args()
print(opts)
#========================= USER CUSTOM FUNCTIONS ===============================
def delay_list(data_list, i):
    temp_list = collections.deque(data_list)
    temp_list.rotate(i)
    data_list_delay= list(temp_list)
    for j in range(i):
        data_list_delay[j] = 0
    return data_list_delay

def mean_squared_error(array1,array2):
    difference_array = np.subtract(array1, array2)
    squared_array = np.square(difference_array)
    mse = squared_array.mean()
    return mse


def setup():
    opts.epocas = int(opts.epocas)
    opts.delays = int(opts.delays)
    opts.max_membership = int(opts.max_membership)
    global model, fuzzy, walk_file, walk_parser, walk_interpolation
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


def trainning():

    walk_data = walk_parser(walk_file)
    step_counter = 1
    step_total = len(walk_data["steps"])
    print(f"The trainning is about to start, {step_total} steps to be trainned")
    fuzzy_hip = None
    fuzzy_knee = None
    for step in walk_data["steps"]:
        if "Walking" in step["task"] and "R" in step["foot"]:
            print(f"Beggining trainning of step {step_counter}...")
        else:
            print(f"Skipping step. Expected a walking task, got a {step['task']}")
            continue
        momentum = {
            "hip": step["momentum"]["hip"],
            "knee": step["momentum"]["knee"]
        }
        angle = {
            "hip": [np.deg2rad(an) for an in step["angle"]["hip"]],
            "knee": [np.deg2rad(an) for an in step["angle"]["knee"]]
        }
        t = step["time"]
        time_holder = t
        angle_holder = angle

        foot = 1 if "R" in step["foot"] else 0
        total_inputs = [
            angle["hip"],
            angle["knee"],
            t,
            [step["duration"] for i in range(len(t))],
            [step["length"] for i in range(len(t))],
            [step["width"] for i in range(len(t))],
            [foot for i in range(len(t))],
        ]
        for delay in range(opts.delays):
            total_inputs.append(delay_list(angle["hip"],delay))
            total_inputs.append(delay_list(angle["knee"],delay))
            total_inputs.append(delay_list(t,delay))

        output = momentum["hip"]
        t = time_holder
        angle = angle_holder
        
        return_network=True if step_counter < 5 else False

        fuzzy_hip= fuzzy(total_inputs,output,
                                    epocas=opts.epocas,
                                    max_membership=opts.max_membership,
                                    return_network=return_network,
                                    neural_ntw=fuzzy_hip)

        output = momentum["knee"]
        fuzzy_knee = fuzzy(total_inputs,output,
                                    epocas=opts.epocas,
                                    max_membership=opts.max_membership,
                                    return_network=return_network,
                                    neural_ntw=fuzzy_knee)


        print(f"Finished trainning of step {step_counter}...")
        print("--- Trainning took %s seconds ---" % (time.time() - start_time))
        step_counter += 1
        if not return_network:
            return fuzzy_hip, fuzzy_knee, walk_data
            

        step = walk_data["steps"][25]
        total_inputs = [
            angle["hip"],
            angle["knee"],
            t,
            [step["duration"] for i in range(len(t))],
            [step["length"] for i in range(len(t))],
            [step["width"] for i in range(len(t))],
            [foot for i in range(len(t))],
        ]
        for delay in range(opts.delays):
            total_inputs.append(delay_list(angle["hip"],delay))
            total_inputs.append(delay_list(angle["knee"],delay))
            total_inputs.append(delay_list(t,delay))


    fuzzy_hip_answer = [[0]*len(total_inputs[0]) for i in range(1)]
    for i in range(len(total_inputs[0])):
        x_input = []
        for j in range(len(total_inputs)):
            x_input += [total_inputs[j][i]]
        fuzzy_hip_answer[0][j]=(fuzzy_hip.calc(x_input))

    fuzzy_knee_answer = [[0]*len(total_inputs[0]) for i in range(1)]
    for i in range(len(total_inputs[0])):
        x_input = []
        for j in range(len(total_inputs)):
            x_input += [total_inputs[j][i]]
        fuzzy_knee_answer[0][j]=(fuzzy_hip.calc(x_input))


    return fuzzy_hip_answer[0], fuzzy_knee_answer[0], walk_data

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
    plt.plot(t, momentums['Hip'], 'g', label='Referência')
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
    plt.plot(t, momentums['Knee'], 'g', label='Referência')
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

