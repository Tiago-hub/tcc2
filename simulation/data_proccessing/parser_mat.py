#!/usr/bin/env python3
from re import M
import sys, os
import csv
import optparse
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np
import scipy.io


sys.path.append(os.path.join(os.path.dirname(__file__), "physical"))
sys.path.append(os.path.join(os.path.dirname(__file__), "fuzzy"))
root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_folder = os.path.join(root,"data")

def walk_parser(path_to_walk_file):
    mat = scipy.io.loadmat(path_to_walk_file)
    data = mat["s"]
    walk = {
        "name": data[0][0]["name"][0],
        "age": data[0][0]["Age"][0][0],
        "gender": data[0][0]["Gender"][0][0],
        "height": data[0][0]["BH"][0][0],
        "mass": data[0][0]["BM"][0][0]
    }
    walk["steps"] = []
    for step in data[0,0]['Data'][0]:
        temp = {}
        temp["foot"] = step["Foot"][0]
        temp["task"] = step["Task"][0]
        temp["duration"] = 60/(0.5*step["cadence"][0][0]) # from article, The cadence (i.e. step/min) was calculated as 60/(0.5*stride duration)
        temp["length"] = step["strideLength"][0]
        temp["width"] = step["stepWidth"][0]
        hipAngle = step["Ang"][3]
        kneeAngle = step["Ang"][6]
        temp["angle"] = {
            "hip": hipAngle,
            "knee": kneeAngle
        }
        hipMoment = step["Mom"][0]
        kneeMoment = step["Mom"][3]
        temp["momentum"] = {
            "hip": hipMoment,
            "knee": kneeMoment
        }
        time_array = []
        t_size = len(hipMoment)
        t_step = temp["duration"]/t_size
        for i in range(t_size):
            if i != 0:
                time_array.append(time_array[i-1]+t_step)
            else:
                time_array.append(i)
        temp["time"] = time_array
        walk["steps"].append(temp)

    return walk

if __name__ == "__main__":
    usage = """Script to convert mat file with walking data to dict.
    Place the mat file at data folder"""""

    p = optparse.OptionParser(usage=usage)
    p.add_option("-f", "--file", dest="filename",
                      help="mat name with walk info. Must be at data folder", metavar="FILE")
    p.set_defaults(filename="Subject1.mat")
    (opts, args) = p.parse_args()

    walk_file = os.path.join(data_folder,opts.filename)
    walk_data = walk_parser(walk_file)
    print(walk_data.keys()) 
    print(walk_data)
