import csv
from keras.utils import np_utils
import numpy as np

# MSZoning: Identifies the general zoning classification of the sale.
#
# A Agriculture
# C Commercial
# FV Floating Village Residential
# I Industrial
# RH Residential High Density
# RL Residential Low Density
# RP Residential Low Density Park
# RM Residential Medium Density

def unitary_coding(estimation_lst, value):
    val_idx = -1
    if value in estimation_lst:
        val_idx = estimation_lst.index(value)
    else:
        for i in range(0, len(estimation_lst)):
            if estimation_lst[i] in value: #list element is the part of value
                val_idx = i
                break
    coded_out = np_utils.to_categorical(val_idx, num_classes=len(estimation_lst))
    if val_idx == -1:
        raise "Fatal error! Unrecognized symbol!"
    return coded_out

def to_float(strval):
    if strval == "NA":
        return 0
    else:
        return float(strval)

def get_max_val(attr, dctlst):
    max_val = 0
    str_lst = [valdct[attr] for valdct in dctlst]
    for i in range(0, len(str_lst)):
        if str_lst[i] == "NA":
            str_lst[i] = "0"
    max_val = max([to_float(strval) for strval in str_lst])
    return max_val

def file_to_data(file_name):
    with open(file_name) as file_obj:

        #lot_frontage_max = get_max_val("LotFrontage", file_name)
        #print("lot_fr_max=", lot_frontage_max)
        i = 0
        reader = csv.DictReader(file_obj, delimiter=',')
        dctlst = []
        for line in reader:
            linedct = dict()
            linedct["Id"] = line["Id"]
            linedct["MSSubClass"] = line["MSSubClass"]
            linedct["MSZoning"] = line["MSZoning"]
            linedct["LotFrontage"] = line["LotFrontage"]
            dctlst.append(linedct)
            #print(line)
            #print(line["LotFrontage"])
            #print("value=", line["MSSubClass"], ", code=", ms_sub_class)
        for valdct in dctlst:
            inarr = unitary_coding(["20", "30", "40", "45", "50", "60", "70", "75", "80", "85", "90", "120", "150", "160", "180", "190"], valdct["MSSubClass"])
            inarr = np.hstack((inarr, unitary_coding(["A", "C", "FV", "I", "RH", "RL", "RP", "RM"], valdct["MSZoning"])))
            inarr = np.hstack((inarr,[to_float(valdct["LotFrontage"]) / get_max_val("LotFrontage", dctlst)]))
    return [0, 0]