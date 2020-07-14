# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 17:53:42 2020

@author: dsikerid
"""
from fastavro import reader
import csv

head = True
count = 0
f = csv.writer(open("a.csv", "w+"))
with open('a.avro', 'rb') as fo:
    reader_avro = reader(fo)
    for emp in reader_avro:
        if head == True:
            header = emp.keys()
            f.writerow(header)
            head = False
        count += 1
        f.writerow(emp.values())
print(count)
