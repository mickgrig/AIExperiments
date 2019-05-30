import csv
from keras.utils import np_utils
import numpy as np
import jellyfish as jf

open('logout.txt', 'w').close() #clear log-file

def unitary_coding(valdct, attribute):
    attr_name = attribute[0]
    attr_range = attribute[1]
    value = valdct[attr_name]
    val_idx = -1
    if value in attr_range:
        val_idx = attr_range.index(value)
    else:
        levdist = len(value) #maximum levenstein distance
        for i in range(0, len(attr_range)):
            curlevdist = jf.levenshtein_distance(value, attr_range[i])
            if curlevdist < levdist:
                levdist = curlevdist
                val_idx = i
        if val_idx >= 0:
            with open("logout.txt", "a") as logf:
                msg = "WARNING. Id = " + valdct["Id"] + ", attr_name = '" + attr_name + "', attr_val = '"\
                    + value + "' among [" + ",".join(attr_range) + "] didn't find exact attribute. Chosen nearest = '"\
                    + attr_range[val_idx]
                msg += "(leven_dist=" + str(levdist) + ")"
                msg += "'\n\n"
                logf.write(msg)

    if val_idx != -1: #parsing attribute successful
        coded_out = np_utils.to_categorical(val_idx, num_classes=len(attr_range))
    else: #bad case = attribute didn't parsed
        with open("logout.txt", "a") as logf:
            msg = "ERROR. Id = " + valdct["Id"] + ", attr_name = '" + attr_name + "', attr_val = '" \
                  + value + "' among [" + ",".join(attr_range) + "] didn't find any similar attribute."
            msg += "'\n\n"
            logf.write(msg)
        coded_out = np.zeros(len(attr_range))
    return coded_out

all_attributes = \
    [
        ("MSSubClass", ["20", "30", "40", "45", "50", "60", "70", "75", "80", "85", "90", "120", "150", "160", "180", "190"]), #16
        ("MSZoning", ["A", "C", "FV", "I", "RH", "RL", "RP", "RM"]), #8 = 24
        ("LotFrontage", []), #2 = 26
        ("LotArea", []), #2 = 28
        ("Street", ["Grvl", "Pave"]), #2 = 30
        ("Alley", ["Grvl", "Pave", "NA"]), #3 = 33
        ("LotShape", ["Reg", "IR1", "IR2", "IR3"]), #4 = 37
        ("LandContour", ["Lvl", "Bnk", "HLS", "Low"]), #4 = 41
        ("Utilities", ["AllPub", "NoSewr", "NoSeWa", "ELO"]), #4 = 45
        ("LotConfig", ["Inside", "Corner", "CulDSac", "FR2", "FR3"]), #5 = 50
        ("LandSlope", ["Gtl", "Mod", "Sev"]), #3 = 53
        ("Neighborhood", ["Blmngtn", "Blueste", "BrDale", "BrkSide", "ClearCr", "CollgCr", "Crawfor", "Edwards", "Gilbert",
                          "IDOTRR", "MeadowV", "Mitchel", "Names", "NoRidge", "NPkVill", "NridgHt", "NWAmes", "OldTown",
                          "SWISU", "Sawyer", "SawyerW", "Somerst", "StoneBr", "Timber", "Veenker"]), #25 = 78
        ("Condition1", ["Artery", "Feedr", "Norm", "RRNn", "RRAn", "PosN", "PosA", "RRNe", "RRAe"]), #9 = 87
        ("Condition2", ["Artery", "Feedr", "Norm", "RRNn", "RRAn", "PosN", "PosA", "RRNe", "RRAe"]), #9 = 96
        ("BldgType", ["1Fam", "2FmCon", "Duplx", "TwnhsE", "TwnhsI"]), #5 = 101
        ("HouseStyle", ["1Story", "1.5Fin", "1.5Unf", "2Story", "2.5Fin", "2.5Unf", "SFoyer", "SLvl"]), #8 = 109
        ("OverallQual", []), #2 = 111
        ("OverallCond", []), #2 = 113
        ("YearBuilt", []), #2 = 115
        ("YearRemodAdd", []), #2 = 117
        ("RoofStyle", ["Flat", "Gable", "Gambrel", "Hip", "Mansard", "Shed"]), #6 = 123
        ("RoofMatl", ["ClyTile", "CompShg", "Membran", "Metal", "Roll", "Tar&Grv", "WdShake", "WdShngl"]), #8 = 131

        #может быть  Wd Shng or WdShing !

        ("Exterior1st", ["AsbShng", "AsphShn", "BrkComm", "BrkFace", "CBlock", "CemntBd", "HdBoard", "ImStucc",
                         "MetalSd", "Other", "Plywood", "PreCast", "Stone", "Stucco", "VinylSd", "Wd Sdng", "WdShing"]), #17 = 148
        ("Exterior2nd", ["AsbShng", "AsphShn", "BrkComm", "BrkFace", "CBlock", "CemntBd", "HdBoard", "ImStucc",
                         "MetalSd", "Other", "Plywood", "PreCast", "Stone", "Stucco", "VinylSd", "Wd Sdng", "WdShing"]), # 17 = 165
        ("MasVnrType", ["BrkCmn", "BrkFace", "CBlock", "None", "Stone"]), #5 = 170
        ("MasVnrArea", []), #2 = 172
        ("ExterQual", ["Ex", "Gd", "TA", "Fa", "Po"]), #5 = 177
        ("ExterCond", ["Ex", "Gd", "TA", "Fa", "Po"]), #5 = 182
        ("Foundation", ["BrkTil", "CBlock", "PConc", "Slab", "Stone", "Wood"]), #6 = 188
        ("BsmtQual", ["Ex", "Gd", "TA", "Fa", "Po", "NA"]), #6 = 194
        ("BsmtCond", ["Ex", "Gd", "TA", "Fa", "Po", "NA"]), #6 = 200
        ("BsmtExposure", ["Gd", "Av", "Mn", "No", "NA"]), #5 = 205
        ("BsmtFinType1", ["GLQ", "ALQ", "BLQ", "Rec", "LwQ", "Unf", "NA"]), #7 = 212
        ("BsmtFinSF1", []), #2 = 214
        ("BsmtFinType2", ["GLQ", "ALQ", "BLQ", "Rec", "LwQ", "Unf", "NA"]), #7 = 221
        ("BsmtFinSF2", []), #2 = 223
        ("BsmtUnfSF", []), #2 = 225
        ("TotalBsmtSF", []), #2 = 227
        ("Heating", ["Floor", "GasA", "GasW", "Grav", "OthW", "Wall"]), #6 = 233
        ("HeatingQC", ["Ex", "Gd", "TA", "Fa", "Po"]), #5 = 238
        ("CentralAir", ["N", "Y"]), #2 = 240
        ("Electrical", ["SBrkr", "FuseA", "FuseF", "FuseP", "Mix"]), #5 = 245
        ("1stFlrSF", []), #2 = 247
        ("2ndFlrSF", []), #2 = 249
        ("LowQualFinSF", []), #2 = 251
        ("GrLivArea", []), #2 = 253
        ("BsmtFullBath", []), #2 = 255
        ("BsmtHalfBath", []), #2 = 257
        ("FullBath", []), #2 = 259
        ("HalfBath", []), #2 = 261
        ("BedroomAbvGr", []), #2 = 263 (incorrect decription key)
        ("KitchenAbvGr", []), #2 = 265  (incorrect decription key)
        ("KitchenQual", ["Ex", "Gd", "TA", "Fa", "Po"]), #5 = 270
        ("TotRmsAbvGrd", []), #2 = 272
        ("Functional", ["Typ", "Min1", "Min2", "Mod", "Maj1", "Maj2", "Sev", "Sal"]), #8 = 280
        ("Fireplaces", []), #2 = 282
        ("FireplaceQu", ["Ex", "Gd", "TA", "Po", "NA"]), #5 = 287
        ("GarageType", ["2Types", "Attchd", "Basment", "BuiltIn", "CarPort", "Detchd", "NA"]), #7 = 294
        ("GarageYrBlt", []), #2 = 296
        ("GarageFinish", ["Fin", "RFn", "Unf", "NA"]), #4 = 300
        ("GarageCars", []), #2 = 302
        ("GarageArea", []), #2 = 304
        ("GarageQual", ["Ex", "Gd", "TA", "Fa", "Po", "NA"]), #6 = 310
        ("GarageCond", ["Ex", "Gd", "TA", "Fa", "Po", "NA"]), #6 = 316
        ("PavedDrive", ["Y", "P", "N"]), #3 = 319
        ("WoodDeckSF", []), #2 = 321
        ("OpenPorchSF", []), #2 = 323
        ("EnclosedPorch", []), #2 = 325
        ("3SsnPorch", []), #2 = 327
        ("ScreenPorch", []), #2 = 329
        ("PoolArea", []), #2 = 331
        ("PoolQC", ["Ex", "Gd", "TA", "Fa", "NA"]), #5 = 336
        ("Fence", ["GdPrv", "MnPrv", "GdWo", "MnWw", "NA"]), #5 = 341
        ("MiscFeature", ["Elev", "Gar2", "Othr", "Shed", "TenC", "NA"]), #6 = 347
        ("MiscVal", []), #2 = 349
        ("MoSold", []), #2 = 351
        ("YrSold", []), #2 = 353
        ("SaleType", ["WD", "CWD", "VWD", "New", "COD", "Con", "ConLw", "ConLI", "ConLD", "Oth"]), #10 = 363
        ("SaleCondition", ["Normal", "Abnorml", "AdjLand", "Alloca", "Family", "Partial"]), #6 = 369
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
            linedct["Id"] = line["Id"] #separatly
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
    #print(jf.levenshtein_distance('berne', 'born'))

    dctlst = make_base_dictlst(file_name) #read file and make working dictionary
    maxvals_dct = make_max_dict(dctlst) #make max values dictionary for number attributes
    rawlst = []
    for valdct in dctlst: #for each input example
        inrow = np.ndarray(0)
        for attribute in all_attributes:
            attr_name = attribute[0]
            attr_range = attribute[1]
            if len(attr_range) == 0: #number attribute
                inrow = np.hstack((inrow, float_coding(valdct, attr_name, maxvals_dct)))
            else: #quality attribute
                inrow = np.hstack((inrow, unitary_coding(valdct, attribute)))
        rawlst.append(inrow)
    print("rawlist size = ", len(rawlst))
    #inmtx = np.ndarray(rawlst)
    inmtx = np.zeros(2)
    return inmtx