import matplotlib.pyplot as plt
import numpy as np

def Raster(data,fs,xlim,ylim = None,MarkerSize = None,col = None,titleString=None):

    #Raster Raster plot of matrix data.
#   Raster(data,fs,xlim,ylim,MarkerSize,color,title) plots the rastergram of the
#   matrix 'data' with x axes limit 'xlim' and y axes limts 'ylim'. The
#   marker will have a size of 'MarkerSize' and a color 'color'.
#   data = data matrix (time stamps matrix).
#   fs = sampling frequency for time conversion.
#   ylim = limits of y axes.
#   MarkerSize = size of the marker.
#   col = color of the markers.
#   titleSTring = title of the plot.
#   [time] = x axis of raster plot.
#   [ChID] = raster plot data (events per channel in time).

    if ylim is None:
        ylimitplot=data.shape[0]
    else:
        ylimitplot = ylimit

    if MarkerSize is None:
        marker=[]
    else:
        marker=MarkerSize

    if col is None:
        colPlot=[]
    else:
        colPlot = col

    if titleString is None:
        titleStr = []
    else:
        titleStr = titleString
##Check!!
#find the number of non zero elements
#numEvents =len(np.nonzero(spk_idx)[0])
    isEm = []
    for i in range(len(spk_idx)):
        if spk_idx[i].size==0:
            isEm.append(1)
    	else:
    		isEm.append(0)
    numEvents =len(np.nonzero(isEm)[0])
    N=data.shape[0]

    SpkTime = np.zeros((numEvents,1),dtype=float)
    ChID = np.zeros((numEvents,1),dtype=float)
    kk = 0

    for i in range(N):
    	szCell = len(data[i])
    	for j in range(szCell):
    		SpkTime[k] = spk_idx[i][j]
    		ChID[k]=i
    		k+=1

    time = SpkTime/fs

    #Plot of the rasterplot
    plt.figure()
    #Set the size of the square
    plt.scatter(time, ChID,c=color, marker=marker)

    plt.ylabel('Channel #')
    plt.xlabel('Time (samples)')
    plt.title('Raster Plot: '+titleString)
    plt.ylim((1,1024));
    plt.show()

    return time,ChID
