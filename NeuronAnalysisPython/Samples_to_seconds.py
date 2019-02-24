# Generated with SMOP  0.41
from libsmop import *
import numpy as np


####function
def Samples_to_seconds(data,fs):

    #Samples_to_seconds Convert from # samples to seconds.
#   Converts each row from sample to seconds according to
#   an input sample frequency.
#   data = data to convert (array, matrix or cell array)
#   fs = sampling frequency
#   [data_T] = array/cell according to "data" data converted in seconds.

    N=data.shape[0]
    data_T=np.zeros((data.shape[0],data.shape[1]),float)
        for i in range(N):
            data_T[i,1]=data[i,1] / fs
    return data_T
