#!/usr/bin/env python3

from ast import walk
import os
import sys
import matplotlib.pyplot as plt
from pathlib import Path
import optparse
this_file_loc = os.path.abspath(__file__)
this_file_path = Path(this_file_loc)
simulation_folder = this_file_path.parents[0]
sys.path.append(os.path.join(os.path.dirname(__file__), "physical"))
sys.path.append(os.path.join(os.path.dirname(__file__), "fuzzy"))
sys.path.append(f"{simulation_folder}/data_proccessing")
from parser_mat import walk_parser

usage = """Script to plot subject mat file with walking data.
Place the mat file at data folder"""""

p = optparse.OptionParser(usage=usage)
p.add_option("-f", "--file", dest="filename",
                  help="mat file name with walk info. Must be at data folder", metavar="FILE")
p.set_defaults(filename="Subject1.mat")
(opts, args) = p.parse_args()

walk_file = f"{simulation_folder}/data/{opts.filename}"
walk_data = walk_parser(walk_file)

print(walk_data.keys())

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
for step in walk_data["steps"]:
    if "R" in step["foot"] and "Walk" in step["task"]:
        y = step["momentum"]["hip"]
        x = step["time"]
        ax.plot(x,y)
        ax.grid()
plt.show()