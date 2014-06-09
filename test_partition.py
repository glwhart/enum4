#!/usr/local/bin/python3
from msgenum3 import *

colors = [3,3,3,3,2]
cycles = [1,1,1,1,1,1,1,1,2,2,2]
if sum(colors) != sum(cycles):
    print("argh")

print(partition_cycles_into_color_vector(colors,cycles))
