#!/usr/bin/env python3

import scipy.io
import os, sys
pat = os.path.join(os.path.dirname(__file__), "Subject1.mat")
mat = scipy.io.loadmat(pat)
teststruct = mat['s']

print(teststruct[0,0]['Data'].dtype)
print(teststruct[0][0]["name"][0])
print(teststruct.dtype)
print(teststruct[0,0]['Data'].dtype)
print(len(teststruct[0,0]['Data'][0,0]['Ang'][3]))

temp = 60/(0.5*teststruct[0,0]['Data'][0,0]['cadence'][0][0])
print(temp)

temp1 = []
t_size = len(teststruct[0,0]['Data'][0,0]['Ang'][3])
t_step = temp/t_size
for i in range(t_size):
    if i != 0:
        temp1.append(temp1[i-1]+t_step)
    else:
        temp1.append(i)

print(temp1)