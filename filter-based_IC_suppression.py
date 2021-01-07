# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 18:04:47 2020

@author: dsikerid
"""
import sys
import csv
from cuckoopy import CuckooFilter
from collections import Mapping, Container
from sys import getsizeof
import math
from random import randrange
from cuckoo.filter import CuckooFilter
 
def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size



mozilla_ICs=[]
error_rate = 10**(-3)


# Read Mozilla Intermediate Certificate List
with open('PublicAllIntermediateCertsWithPEMReport.csv', 'r', encoding="utf8") as file:
    reader = csv.reader(file)
    for row in reader:
        mozilla_ICs.append(row[23])
mozilla_ICs.pop(0)

#Construct cuckoo filter
capacity = 398
bucket_size = 2
# Setting the bucket size is optional, the bigger the bucket,
# the more number of items a filter can hold, and the longer
# the fingerprint needs to be to stay at the same error rate
cuckoo = CuckooFilter(capacity=capacity, error_rate=error_rate, bucket_size=bucket_size)

# The fingerprint length is computed using the following formula:
fingerprint_size = int(math.ceil(math.log(1.0 / error_rate, 2) + math.log(2 * bucket_size, 2)))

certs_number = 700
for i in range(1, certs_number):
    item = mozilla_ICs[i]
    cuckoo.insert(item)

    # if cuckoo.contains(item):
    #     print('{} has been added'.format(item))

    # cuckoo.delete(item)

    # if not cuckoo.contains(item):
    #     print('{} has been removed'.format(item)())
upper_space_cost=float((math.ceil(math.log(1.0 / error_rate, 2) + math.log(2 * bucket_size, 2)))/cuckoo.load_factor())

total_filter_size = upper_space_cost * certs_number*0.000125
print('total_filter_size = ',total_filter_size)
print('Load_factor = ',cuckoo.load_factor())
print('--------------------')
