#!/usr/bin/env python3

from sqlite3 import OptimizedUnicode
import time
from classes import NFN, membership,neuron
import numpy as np
import matplotlib.pyplot as plt
from fuzzy import fuzzy
import sys, os
import csv
import optparse

usage = """Script to train neural network with
some chemistry data"""""

p = optparse.OptionParser(usage=usage)
p.add_option("-f", "--file", dest="filename",
                  help="csv file name with walk info. Must be at data folder", metavar="FILE")
p.set_defaults(filename="entumescimento.csv")
(opts, args) = p.parse_args()

root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_folder = os.path.join(root,"simulation","data")
walk_file = os.path.join(data_folder,opts.filename)

number_of_inputs = 2
epocas = 3
max_membership = 100

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def parser(path_to_file):
    with open(path_to_file) as file:
        data_temp = csv.DictReader(file)
        data_keys = data_temp.fieldnames
        data_dict = {key.strip():[] for key in data_keys}
        for data in data_temp:
            for key in data.keys():
                data_dict[key].append(float(data[key]))

    return data_dict

def setup(data_dict,input_keys,output_key):

    x = [[] for i in range(number_of_inputs)]
    y = [value for value in data_dict[output_key]]
    
    for index, key in enumerate(input_keys):
        if key in data_dict.keys():
            x[int(index)] = data_dict[key]

    return x, y
    # for key in output_key:

    # return 

if __name__ == "__main__":
    data_dict = parser(walk_file)
    x, y = setup(data_dict,['temperatura','ph'],'grau de entumescimento')
    fuzzy_ntw = fuzzy(x,y,epocas=epocas,max_membership=max_membership, return_network=True)
    output = fuzzy(x,y,epocas=epocas,max_membership=max_membership, return_network=False)
    
    extended_input = list(range(50))
    extended_output = [fuzzy_ntw.calc([tempe,8.5]) for tempe in extended_input]
    print(extended_output)
    print(output)
    print(fuzzy_ntw.calc([20,8.5]))
    
    ph4, ph7, ph8 = 0,1,2
    temperature = data_dict["temperatura"]
    entum = data_dict["grau de entumescimento"]

    fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1)
    # ax.plot(temperature,entum, "o", label="Sinal original")
    # ax.plot(temperature,output,"*",label="Replicação pela rede nebulosa")
    # ax.grid()
    # # ax.annotate(f"MSE: {mean_squared_error(y,output):.3}",(0,-0.5))
    # plt.title('Rede neo-nebulosa replica grau de entumescimento')
    # plt.xlabel("Temperatura [°C]")
    # plt.ylabel('Grau de entumescimento [g/g]')
    # plt.grid(visible=True)
    # plt.legend(loc="best")

    ax = fig.add_subplot(1, 1, 1)
    ax.plot(temperature,entum, "o", label="Sinal original")
    ax.plot(extended_input,extended_output,"*", label="Replicação pela rede nebulosa")
    ax.grid()
    # ax.annotate(f"MSE: {mean_squared_error(y,output):.3}",(0,-0.5))
    plt.title('Grau de entumescimento com mais variação de temperaturas')
    # plt.ylabel('Torque (Nm)')
    plt.grid(visible=True)
    plt.legend(loc="best")
    plt.xlabel("Temperatura [°C]")
    plt.ylabel('Grau de entumescimento [g/g]')

    #print()
    plt.show()