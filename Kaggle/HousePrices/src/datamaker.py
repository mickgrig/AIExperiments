import csv
from keras.utils import np_utils
import numpy as np

def unitary_coding(possible_val_lst, value):
    val_idx = -1
    if value in possible_val_lst:
        val_idx = possible_val_lst.index(value)
    else:
        for i in range(0, len(possible_val_lst)):
            if possible_val_lst[i] in value: #list element is the part of value
                val_idx = i
                break
    coded_out = np_utils.to_categorical(val_idx, num_classes=len(possible_val_lst))
    if val_idx == -1:
        raise "Fatal error! Unrecognized symbol!"
    return coded_out

all_attributes = \
    [
        ("MSSubClass", ["20", "30", "40", "45", "50", "60", "70", "75", "80", "85", "90", "120", "150", "160", "180", "190"]), #16
        ("MSZoning", ["A", "C", "FV", "I", "RH", "RL", "RP", "RM"]), #8 = 24
        ("LotFrontage", []), #2 = 26
        ("LotArea", []), #2 = 28
        ("Street", ["Grvl", "Pave"]), #2 = 30
        ("Alley", ["Grvl", "Pave", "NA"]), #3 = 33
        ("LotShape", ["Reg", "IR1", "IR2", "IR3"]) #4 = 37
    ]

def float_coding(valdct, attr, maxvals_dct):
    retarr = np.zeros(2)
    if valdct[attr] == "NA":
        retarr[0] = 1
    else:
        retarr[1] = float(valdct[attr]) / maxvals_dct[attr]
    return retarr

def make_base_dictlst(file_name):
    dctlst = []
    with open(file_name) as file_obj:
        reader = csv.DictReader(file_obj, delimiter=',')
        for line in reader:
            linedct = dict()
            for attr_descr in all_attributes:
                attr_name = attr_descr[0]
                linedct[attr_name] = line[attr_name]
            dctlst.append(linedct)
    return dctlst

def make_max_dict(dctlst):
    maxvals_dct = dict()
    for attr_descr in all_attributes:
        attr_range = attr_descr[1]
        if len(attr_range) == 0: #this is number attribute
            attr_name = attr_descr[0]
            max_val = 0
            for valdct in dctlst:
                strval = valdct[attr_name]
                if strval != "NA": #possible unknown value
                    fltval = float(strval)
                    if fltval < 0:
                        raise "Unexpected negative number!"
                    max_val = max(max_val, fltval)
            maxvals_dct[attr_name] = max_val
    return maxvals_dct

def file_to_data(file_name):
    dctlst = make_base_dictlst(file_name) #read file and make working dictionary
    maxvals_dct = make_max_dict(dctlst) #make max values dictionary for number attributes

    for valdct in dctlst: #for each input example
        inarr = np.ndarray(0)
        for attribute in all_attributes:
            attr_name = attribute[0]
            attr_range = attribute[1]
            if len(attr_range) == 0: #number attribute
                inarr = np.hstack((inarr, float_coding(valdct, attr_name, maxvals_dct)))
            else: #quality attribute
                inarr = np.hstack((inarr, unitary_coding(attr_range, valdct[attr_name])))
        print(len(inarr))
        break
    return [0, 0]