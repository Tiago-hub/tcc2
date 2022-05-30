#!/usr/bin/env python3

import os
import sys
from pathlib import Path
this_file_loc = os.path.abspath(__file__)
this_file_path = Path(this_file_loc)
simulation_folder = this_file_path.parents[0]
sys.path.append(os.path.join(os.path.dirname(__file__), "physical"))
sys.path.append(os.path.join(os.path.dirname(__file__), "fuzzy"))
sys.path.append(f"{simulation_folder}/data_proccessing")


import numpy as np
from scipy.integrate import odeint, solve_ivp
from pid_class import PID
import matplotlib.pyplot as plt
import csv
import optparse
import collections
import model2 as model
from real_walk_train import get_angles_trainned
from parser_walk import walk_parser
from parser_walk import walk_interpolation

usage = """Script to convert csv file with walking data to list.
Place the csv file at data folder"""""

p = optparse.OptionParser(usage=usage)
p.add_option("-f", "--file", dest="filename",
                  help="csv file name with walk info. Must be at data folder", metavar="FILE")
p.set_defaults(filename="walk1.csv")
(opts, args) = p.parse_args()

walk_file = f"{simulation_folder}/data/{opts.filename}"
walk_data = walk_interpolation(walk_parser(walk_file),0.1)

#constants
total_mass = 73
total_height = 1.731
m1 = (0.105/2)*total_mass
m2 = ((0.0475+0.0143)/2)*total_mass
w1 = 0.232*total_height
w2 = 0.247*total_height
l1 = 0.433*w1
l2 = 0.434*w2

pendulum_model = model.double_pendulum(m1, m2, l1, l2, w1, w2,b1=0,b2=0)
y0 = [np.deg2rad(33.79816055297852), 0, 0, np.deg2rad(8.202593803405762), 0, 0]  # Initial state of the system
dt = 0.1
t = list(range(101))
t = np.arange(0.0, 100, dt)

ankle, hip, knee = get_angles_trainned().values()

#files
walk_data = walk_interpolation(walk_parser(walk_file),0.1)

result = [[], [], [], [], [], []]
for j in range(len(result)):
    result[j].append(y0[j])
tal1 = hip[0]
tal2 = knee[0]
counter = 0
for i in range(len(t)):
    #print(i)
    if i != 0:
        t_span = (t[i-1], t[i])
        result_solve_ivp = solve_ivp(pendulum_model.dpend_dt, t_span, y0)
        last_column = result_solve_ivp.y.shape[1] - 1
        if counter>1:
            counter = 0
            tal1 = hip[i]/l1
            tal2 = knee[i]/l2
            #tal2 = 0
        y0 = [result_solve_ivp.y[0, last_column],
              result_solve_ivp.y[1, last_column],
              result_solve_ivp.y[2, last_column],
              result_solve_ivp.y[3, last_column],
              tal1,
              tal2
              ]
        for j in range(len(result)):
            result[j].append(y0[j])
        counter += 1

for i in range(len(result[0])):
    result[0][i] = np.rad2deg(result[0][i])
    result[2][i] = np.rad2deg(result[2][i])
fig = plt.figure()
ax = fig.add_subplot(2, 1, 1)
ax.plot(t, result[0], 'b', label='hip(t)')
ax.plot(t, walk_data['Hip Angle'], 'g', label='Hip reference')
ax.plot(t, result[2], 'r', label='knee(t)')
ax.plot(t, walk_data['Knee Angle'], 'y', label='Knee reference')
ax.legend(loc='best')
#plt.xlim([0, 5])
#plt.ylim([-20, 20])
ax.grid()
ax = fig.add_subplot(2, 1, 2)
ax.plot(t, result[4], 'b', label='Angular Acceleration Hip')
ax.plot(t,hip,'g', label='fuzzy hip')
#ax.plot(t, result[1], 'g', label='x2(t)')
ax.plot(t, result[5], 'r', label='Angular Acceleration knee')
ax.plot(t,knee,'y', label='fuzzy knee')
#ax.plot(t, result[3], 'y', label='x4(t)')
ax.legend(loc='best')
#plt.xlim([0, 5])
#plt.ylim([-20, 20])
ax.grid()
plt.show()
