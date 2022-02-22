#!/usr/bin/env python3
import sys, os
import csv
import optparse

usage = """Script to convert csv file with walking data to list.
Place the csv file at data folder, use header to inform the column name"""""

p = optparse.OptionParser(usage=usage)
p.add_option("-f", "--file", dest="filename",
                  help="csv file name with walk info. Must be at data folder", metavar="FILE")
p.set_defaults(filename="walk1.csv")
(opts, args) = p.parse_args()

sys.path.append(os.path.join(os.path.dirname(__file__), "physical"))
sys.path.append(os.path.join(os.path.dirname(__file__), "fuzzy"))
root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_folder = os.path.join(root,"data")
walk_file = os.path.join(data_folder,opts.filename)

def walk_parser():
    with open(walk_file) as file:
        walk_data_temp = csv.DictReader(file)
        walk_keys = walk_data_temp.fieldnames
        walk_data = {'Ankle Angle': [], 'Hip Angle': [], 'Knee Angle': [], 'Ankle Momentum': [], 'Hip Momentum': [], 'Knee Momentum': [], 'Ankle Power': [], 'Hip Power': [], 'Knee Power': []}
        for data in walk_data_temp:
            for key in data.keys():
                walk_data[key].append(float(data[key]))

    return walk_data

if __name__ == "__main__":
    walk_data = walk_parser()
    print(walk_data.keys()) 
    print(walk_data)
