import numpy as np
from itertools import chain

# Get the largest absolute value in an np array
def getAbsLargestVal(arr):
    return np.max(np.abs(arr))

# Flatten a 2d np array into 1d array
def flatten2dList(arr, dataType=int):
    return np.fromiter(chain.from_iterable(arr), dataType)