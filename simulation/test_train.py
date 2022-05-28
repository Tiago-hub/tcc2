#!/usr/bin/env python3
import numpy as np
from scipy.integrate import odeint, solve_ivp
import matplotlib.pyplot as plt
from anime import Anime
from pid_class import PID
import sys, os
import csv
sys.path.append(os.path.join(os.path.dirname(__file__), "physical"))
sys.path.append(os.path.join(os.path.dirname(__file__), "fuzzy"))
root = os.path.dirname(os.path.dirname(__file__))
data_folder = os.path.join(root,"data")
walk_file = os.path.join(data_folder,"walk1.csv")
import model2 as model
from classes import NFN, neuron

total_mass = 73
total_height = 1.731
m1 = (0.105/2)*total_mass
m2 = ((0.0475+0.0143)/2)*total_mass
w1 = 0.232*total_height
w2 = 0.247*total_height
l1 = 0.433*w1
l2 = 0.434*w2
print(m1,m2,w1,w2,l1,l2)
pendulum_model = model.double_pendulum(m1, m2, l1, l2, w1, w2,b1=0.001,b2=0.001)

with open(walk_file) as file:
    walk_data_temp = csv.DictReader(file)
    walk_keys = walk_data_temp.fieldnames
    walk_data = {'Ankle Angle': [], 'Hip Angle': [], 'Knee Angle': [], 'Ankle Momentum': [], 'Hip Momentum': [], 'Knee Momentum': [], 'Ankle Power': [], 'Hip Power': [], 'Knee Power': []}
    for data in walk_data_temp:
        for key in data.keys():
            walk_data[key].append(float(data[key]))

print(walk_data['Ankle Angle'])

t = list(range(1,101+1))
print(t)
fig = plt.figure()
plt.plot(t, walk_data['Ankle Angle'], 'b', label='x1(t)')
#ax.plot(t, result[1], 'g', label='x2(t)')
#ax.plot(t, result[2], 'r', label='x3(t)')
#ax.plot(t, result[3], 'y', label='x4(t)')
plt.legend(loc='best')
#plt.xlim([0, 5])
#plt.ylim([-20, 20])
plt.grid()
plt.show()


