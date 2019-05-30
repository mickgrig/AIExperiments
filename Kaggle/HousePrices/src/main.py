from datamaker import file_to_data
import numpy as np

[TrainIn, TrainOut] = file_to_data("../data/train.csv")

print("input shape = ", TrainIn.shape)
print("output shape = ", TrainOut.shape)


