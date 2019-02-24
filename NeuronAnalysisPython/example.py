import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import os
import scipy
from scipy import signal
import pandas as pd 

import find_spike_threshold
#########################FUNCTION Definition##########################################
def filter_data(x,fmin,fmax,srate):
	from scipy import signal
	if 'fmin' not in locals():
		fmin = 500
	if 'fmax' not in locals():
		fmax = 8000
	if 'srate' not in locals():
		srate = 30000
	
	Wp = [700*2/srate, 8000*2/srate]
	Ws = [500*2/srate, 10000*2/srate]
	N, Wn = signal.buttord(Wp,Ws,3,20,True)
	b, a = signal.butter(N, Wn, 'band', analog = True)
	xf = signal.filtfilt(b,a,x,method='gust')
	return xf
	
###################################################################Get the input preference from Users###################################################################

TestChan = int(input("Set the channle you want to test!"))

def get_bool(prompt):
    while True:
        try:
           return {"true":True,"false":False}[input(prompt).lower()]
        except KeyError:
           print("Invalid input please enter True or False!")

ImportNewData = get_bool("'Be filtered?(answer true or false only):")
LoadData = get_bool("Extract spikes and save the workspace?")
ichan = TestChan;

###################################################################Variables Definition   ###################################################################
fs=30000;
nchannels = 1024
dt = np.dtype(np.float32)

################################################################### Import the Data ###################################################################
if(ImportNewData):
	root = tk.Tk()
	root.withdraw()
	root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("BIN files","*.bin"),("all files","*.*")))
	print ('Your file path is:'+root.filename)
	Full_Path = root.filename
	nsamples  = os.path.getsize(Full_Path)/float(nchannels*dt.itemsize)
	d = np.memmap(Full_Path,mode = 'r+',dtype = dt ,shape = (int(nsamples),int(nchannels)))
	data = d.T
	
	#filtered data should copy from data
	fdata = data
	print('Data Imported. Starting to filter ...')
	time = np.arange(0,1/30000,1/30000*(len(data)-1))
	
	# check a test channel of the data
	plt.plot(data[ichan,:])
	thresh = np.zeros((nchannels,1),dtype=float)
	
	#Data Filtering
	for i in range(nchannels):
		fdata[i,:] = filter_data(data[i,:],500,8000,30000)
		thresh[i] = find_spike_threshold(fdata[i,:])
		
	print('Data filtered!!');
	print('Now plot the filtered data')
	plt.plot(time.T,fdata[ichan,:]*1e3,[0,time[1,end]],[0,0]-thresh(ichan)*1e3)
	plt.xlabel('Time(sec)')
	plt.ylabel('Voltage(mv)')
	plt.show()
	
	# Extract extracellular spikes
	print('Starting Extracellular spikes extraction ...')
	
	###Save the work space File
	df = pd.DataFrame(fdata)
	df.to_csv(Full_Path+"_filtered.csv")
	
