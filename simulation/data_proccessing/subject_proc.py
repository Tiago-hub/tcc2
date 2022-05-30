#!/usr/bin/env python3

import os, os
import csv

root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_folder = os.path.join(root,"data")
file = os.path.join(data_folder,"walk1.csv")
with open(file, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
