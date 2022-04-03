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

usage = """Script to convert csv file with walking data to list.
Place the csv file at data folder"""""

p = optparse.OptionParser(usage=usage)
p.add_option("-f", "--file", dest="filename",
                  help="csv file name with walk info. Must be at data folder", metavar="FILE")
p.set_defaults(filename="walk1.csv")
(opts, args) = p.parse_args()

def setup():
    global model, fuzzy, walk_file, walk_parser, walk_interpolation
    this_file_loc = os.path.abspath(__file__)
    this_file_path = Path(this_file_loc)
    simulation_folder = this_file_path.parents[0]
    sys.path.append(f"{simulation_folder}/physical")
    sys.path.append(f"{simulation_folder}/fuzzy")
    sys.path.append(f"{simulation_folder}/data_proccessing")
    walk_file = f"{simulation_folder}/data/{opts.filename}"
    import model2 as model
    from fuzzy import fuzzy 
    from parser_walk_jp import walk_parser
    from parser_walk_jp import walk_interpolation

def trainning():
    global fuzzy_answer, angles, momentums, walk_data
    fuzzy_answer = {}
    angles = {}
    momentums = {}
    #walk_data = walk_interpolation(walk_parser(walk_file),0.1)
    walk_data = walk_parser(walk_file)
    epocas = 5
    max_membership = 200

    input_dict = {}
    output_dict = {}
    for data_name, data_list in walk_data.items():
        #the range of input list is the number of delays,
        #e.g range(4) -> input list will be a list with:
        #[data(t), data(t-1), data(t-2), data(t-3)]
        input_list = [[] for i in range(10)]
        output_list = []

        if "angle" in data_name.lower():
            #shift in time
            for i in range(len(input_list)):
                if i == 0:
                    input_list[i] = data_list
                    continue
                temp_list = collections.deque(data_list) 
                temp_list.rotate(i)
                data_list_delay= list(temp_list)
                data_list_delay[i-1] = 0
                input_list[i] = data_list_delay

            body_part = data_name.split(" ")[0]
            input_dict[body_part] = input_list
            angles[body_part] = data_list

        elif "momentum" in data_name.lower():
            output_list = data_list
            body_part = data_name.split(" ")[0]
            output_dict[body_part] = output_list
            momentums[body_part] = data_list

    total_inputs = []
    for body_part, inputs in input_dict.items():
        for data in inputs:
            total_inputs.append(data)
    for body_part, inputs in input_dict.items():
        input_ = input_dict[body_part]
        output = output_dict[body_part]
        fuzzy_answer[body_part] = fuzzy(input_,output,epocas=epocas,max_membership=max_membership)

def plot_graphs():
    #generate "time" array

    #hip, knee = get_angles_trainned().values()
    with open("hip", "wb") as fp:   #Pickling
        pickle.dump(momentums['Hip'], fp)
    with open("knee", "wb") as fp:   #Pickling
        pickle.dump(momentums['Knee'], fp)

    t = list(range(101))
    dt = 0.1
    t = np.arange(0.0, 100, dt)
    t = walk_data['time']
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    for body_part in fuzzy_answer.keys():
        ax.plot(t,momentums[body_part], label=f"{body_part} angle")
        ax.plot(t,fuzzy_answer[body_part], label=f"{body_part} fuzzy")
    ax.legend(loc="best")
    ax.grid()
    plt.title(f"{body_part} results")
    plt.show()

def main():
    setup()
    trainning()
    plot_graphs()

def get_angles_trainned():
    setup()
    trainning()
    return fuzzy_answer
    
if __name__ == "__main__":
    main()

    
