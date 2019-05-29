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

all_attributes = ["Id", "MSSubClass", "MSZoning", "LotFrontage", "LotArea", "Street", "Alley"]
number_attributes = ["LotFrontage", "LotArea"]

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
            for attr in all_attributes:
                linedct[attr] = line[attr]
            dctlst.append(linedct)
    return dctlst

def make_max_dict(dctlst):
    maxvals_dct = dict()
    for attrib in number_attributes:
        max_val = 0
        for valdct in dctlst:
            strval = valdct[attrib]
            if strval != "NA": #possible unknown value
                fltval = float(strval)
                if fltval < 0:
                    raise "Unexpected negative number!"
                max_val = max(max_val, fltval)
        maxvals_dct[attrib] = max_val
    return maxvals_dct

def file_to_data(file_name):
    dctlst = make_base_dictlst(file_name)
    maxvals_dct = make_max_dict(dctlst)

    for valdct in dctlst:
        inarr = unitary_coding(["20", "30", "40", "45", "50", "60", "70", "75", "80", "85", "90", "120", "150", "160", "180", "190"], valdct["MSSubClass"]) #16
        inarr = np.hstack((inarr, unitary_coding(["A", "C", "FV", "I", "RH", "RL", "RP", "RM"], valdct["MSZoning"]))) #8 = 24
        inarr = np.hstack((inarr, float_coding(valdct, "LotFrontage", maxvals_dct))) #2 = 26
        inarr = np.hstack((inarr, float_coding(valdct, "LotArea", maxvals_dct)))  #2 = 28
        inarr = np.hstack((inarr, unitary_coding(["Grvl", "Pave"], valdct["Street"])))  #2 = 30
        inarr = np.hstack((inarr, unitary_coding(["Grvl", "Pave", "NA"], valdct["Alley"])))  #3 = 33

        #inarr = np.hstack((inarr, [to_float(valdct["LotArea"]) / get_max_val("LotArea", dctlst)]))
        #inarr = np.hstack((inarr, unitary_coding(["Grvl", "Pave"], valdct["Street"])))

        print(len(inarr))
        break
    return [0, 0]