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

# def get_max_val(attr, file_name):
#     max_val = 0
#     with open(file_name) as file_obj:
#         reader = csv.DictReader(file_obj, delimiter=',')
#         str_lst = [line[attr] for line in reader]
#         for i in range(0, len(str_lst)):
#             if str_lst[i] == "NA":
#                 str_lst[i] = "0"
#         max_val = max([float(strval) for strval in str_lst])
#     return max_val

def file_to_data(file_name):
    with open(file_name) as file_obj:
        reader = csv.DictReader(file_obj, delimiter=',')
        lot_frontage_max = get_max_val("LotFrontage", file_name)
        print("lot_fr_max=", lot_frontage_max)
        i = 0
        for line in reader:
            #print(line)
            inarr = unitary_coding(["20", "30", "40", "45", "50", "60", "70", "75", "80", "85", "90", "120", "150", "160", "180", "190"], line["MSSubClass"])
            inarr = np.hstack((inarr, unitary_coding(["A", "C", "FV", "I", "RH", "RL", "RP", "RM"], line["MSZoning"])))
            print(line["LotFrontage"])
            #print("value=", line["MSSubClass"], ", code=", ms_sub_class)
    return [0, 0]