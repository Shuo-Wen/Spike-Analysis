import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import os
import scipy
from scipy import signal
import pandas as pd
import sys

from find_spike_threshold import find_spike_threshold
from filter_data import filter_data
from extract_extracellular_spikes import extract_extracellular_spikes
from FastRMS import FastRMS
from getAbove import getAbove
###################################################################Get the input preference from Users###################################################################

ichan = int(input("Set the channle you want to test!"))

def get_bool(prompt):
    while True:
        try:
           return {"true":True,"false":False}[input(prompt).lower()]
        except KeyError:
           print("Invalid input please enter True or False!")

#Default Setting
print("If the default setting?")
ifDefault = get_bool("Enter True or False") #Import a new dataset
if ifDefault:
    ImportNewData, LoadData, SaveCleanWS ,RestoreUncertainChannels, RasterPlot, InvertData, CleanSpkMap = [1,0, 0, 0, 1, 0 ,0]
else:
    ImportNewData = get_bool("'Import New Data, filter, extract spikes and save the workspace?(answer true or false only):") #Import a new dataset
    LoadData = get_bool("'Load pre-processed data?")  # .bin data loaded in mV and corrected for gain
    SaveCleanWS = get_bool("Saveworkspace of cleaned data?")  #Save the workspace of the cleaned data
    RestoreUncertainChannels = ("Restore uncertain channels indexes?")  #Put to zero the indexes of the additional channels to remove
    RasterPlot=get_bool("Raster Plot?");                 #Plot the rasterplot
    #Remove the bad channel default set as True
    InvertData=get_bool("Invert Data?");                 # Invert the data
    CleanSpkMap=get_bool("Clean Spike Map Data?");                # Remove bad channels identified after the spike map plot


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
        fileName = os.path.basename(Full_Path)
        nsamples  = os.path.getsize(Full_Path)/float(nchannels*dt.itemsize)
        d = np.memmap(Full_Path,mode = 'r+',dtype = dt ,shape = (int(nsamples),int(nchannels)))
        data = d.T
        #filtered data should copy from data
        fdata = data
        print('Data Imported. Starting to filter ...')
        time = np.arange(0,len(fdata[ichan,:])/30000,1/30000)

        # check a test channel of the data
        plt.plot(data[ichan,:])
        thresh = np.zeros((nchannels,1),dtype=float)

        #Data Filtering
        for i in range(nchannels):
                fdata[i,:] = filter_data(data[i,:],500,8000,30000)
                thresh[i] = find_spike_threshold(fdata[i,:],6)

        print('Data filtered!!');
        print('Now plot the filtered data')
        plt.plot(time,fdata[ichan,:])
        plt.xlabel('Time(sec)')
        plt.ylabel('Voltage(mv)')
        print("Notice that you have to close the window to continue the code!")
        plt.show()


        # Extract extracellular spikes
        print('Starting Extracellular spikes extraction ...')
        spk,spk_w,t_spk_w,spk_idx,threshold=extract_extracellular_spikes(fdata, 6, None, 1, 1, 2, 'neg')
        ###Save the work space File
        df = pd.DataFrame(fdata)
        df.to_csv(os.path.splitext(Full_Path)[0]+"_filtered.csv")

if (LoadData):
    sys.modules[__name__].__dict__.clear()
    Full_Path2 = [path,fileOld];
    print('Data Loaded.');

###################################################################Removal of bad channels###################################################################
RemoveBadCh=1

if (RemoveBadCh):
        # Conversion of spikes indexes in seconds
        spk_idx_T = Samples_to_seconds(data,fs)
#12/11
        print('Starting to remove the bad channels ...')
        limit=10000

        numberOfSamples=1000

        problem = np.zeros(fdata.shape[0],1)

        uncertain=np.zeros(fdata,shape[0],1)

        rms=np.zeros(fdata.shape[0],fdata.shape[1])

        above=np.zeros(fdata.shape[0],fdata.shape[1])

        doubt=np.zeros(fdata.shape[0],fdata.shape[1])

        slope_limit=1e-08

        for i in range(spk_idx.shape[0]):
                if not len(spk_idx[i,:]):
                    rms[i,:] = FastRMS(fdata[i,:],numberOfSamples)
                    above[i,:], doubt[i,:] = getAbove(rms[i,:],slope_limit)
                    problem[i] = isNotValid(above[i,:],limit)
                    uncertain[i] = isNotValid(doubt[i,:],limit)

        spk_idx_clean=copy(spk_idx)
        spk_w_clean=copy(spk_w)

        for i in range(spk_idx_clean.shape[0]):
            if problem[i] == 1:
                spk_idx_clean[i]=[]
                spk_w_clean[i]=[]

        # Save to a variable the list of removed channels auto
        ChRemAuto=problem.nonzero()[0]
        print('Bad channels removed.')
        # find the indexes of the non-zero elements of uncertain vector
        ChToCheck=uncertain.nonzero()[0]
# NeuronsAnalysis_v12_2018.m:121
        print('Check the following uncertain channels:')
        print('ChToCheck')
        chCheck=989
        rms=FastRMS(fdata[chCheck,:],numberOfSamples)
        above2, doubt2 = getAbove(rms, slope_limit)
        if len(doubt2)>1:
            uncertain2 = isNotValid(doubt2,limit)
            plt.figure()
            plt.subplot(2,1,1)
            plt.plot(fdata[chCheck,:])
            plt.title('Ch:'+str(chCheck)+' Raw Data')
            plt.plot(rms)
            plt.title(sprintf('Ch: %.f RMS',chCheck))
            plt.subplot(2,1,2)
            plt.plot(doubt2)
            plt.title(sprintf('Ch: %.f Doubt',chCheck))
            plt.ylim((0,2))
        else:
            print('doubt2 variable empty!')

        if len(above2) > 1:
            uncertain2=isNotValid(above2,limit)
            plt.figure()
            plt.subplot(2,1,1)
            plt.plot(fdata[chCheck,:])
            plt.title('Ch:'+str(chCheck)+'Raw Data')
            plt.plot(rms)
            plt.title('Ch:'+ str(chCheck)+'RMS')
            plt.subplot(2,1,2)
            plt.plot(above2)
            plt.title('Ch: '+str(chCheck)+' Above')
            plt.ylim((0,2))
            plt.show()
        else:
            print('above2 variable empty!')
            # Remove additional channels after manual check
        if (RestoreUncertainChannels):
            Excl_idx=[]
            Incl_idx=[]

        else:
            Excl_idx=[]
            Incl_idx=[]
       ############################# confused why empty #############
        for k in range(Excl_idx.shape[1]):
            tmp_idx = Excl_idx[k]
            spk_idx_clean[tmp_idx,:] = np.zero((1,1),float)
            spk_w_clean[tmp_idx,:]= np.zero((1,1),float)

            # Auto removed channels not be be removed
        for k in range(Incl_idx.shape[1]):
            tmp_idx=Incl_idx[k]
            spk_idx_clean[tmp_idx,:] = np.zero((1,1),float)
            spk_w_clean[tmp_idx,:] = np.zero((1,1),float)

######################## save workspace of cleaned data (why save again?why txt? what kind of file should be saved?)
if (SaveCleanWS):
        # Save the workspace in a  csv file
        print('Saving the clean WS to file ...')
        saveName='WS2msNegINV_CLEAN_'+os.path.splitext(fileName)
        df1 = pd.DataFrame(fdata)
        #if you wanna save to different file, just add the file path before"saveName"
        df.to_csv(saveName+".csv")
        print('Cleaned WS saved to csv.')

        filename_noExt=os.path.splitext(fileName)
        saveNameTXT='RemovedCH_Man_'+ filename_noExt + '.txt'
        np.savetxt(saveNameTXT,fdata)
        #saveNameTXT2=concat(['RemovedCH_Auto_',filename_noExt,'.txt'])
        #save(saveNameTXT2,'ChRemAuto','-ascii')
        #fprintf('%s\n','Cleaned WS saved to .mat and removed extra channels saved to .txt.')

##################################################################### Plot of a single channel with the averaged waveforms
## Convert the spike time index from samples to seconds
ichan = 100
plt.figure()
plt.subplot(1,4,3)
plt.plot(time.T,fdata[ichan,:]*1e3)

plt.xlabel('Time, (s)')
plt.ylabel('Voltage, (\muV)')
plt.xlim((0,time[-1]))

plt.plot(spk[ichan],fdata[ichan,spk_idx[ichan]])
plt.plot([0,time[-1],[-threshold[ichan],-threshold[ichan]]])

plt.subplot(1,4,4)
t_spk_w_T = Samples_to_seconds(t_spk_w,fs)

if not len(spk_idx[ichan])==0:
    plt.plot(t_spk_w,spk_w[ichan].T,'k0',linewidth=0.5)
    plt.plot(t_spk_w,np.nanmean(spk_w[ichan]),'r+',linewidth=2)
    plt.ylabel('Voltage, (\muV)')
plt.show()

##################################################################### Raster Plot####################################
if (RasterPlot):
    Raster(spk_idx,fs,time,spk_idx.shape[0],10,'r','Raster Plot: '+fileName)
    Raster(spk_idx_clean,fs,time,spk_idx_clean.shape[0],10,'b','Raster Plot (clean): '+fileName)

######################################################################################################################

    SpikeMap(spk_w_clean,5,1,'b',20)
    title(concat([sprintf('ch %.f,',ichan),fileName]),'Interpreter','none')

if (CleanSpkMap):
    # clean in case bad channels are detected
    spk_w_clean_aftSpMap = spk_w_clean
    spk_idx_clean_aftSpMap = spk_idx_clean
    Excl=concat([301])
# NeuronsAnalysis_v12_2018.m:266
    for k in arange(1,size(Excl,2),1).reshape(-1):
        tmp_idx=Excl(k)
# NeuronsAnalysis_v12_2018.m:269
        spk_w_clean_aftSpMap[tmp_idx,arange()]=cellarray([[]])
# NeuronsAnalysis_v12_2018.m:270
        spk_idx_clean_aftSpMap[tmp_idx,arange()]=cellarray([[]])
# NeuronsAnalysis_v12_2018.m:271
    saveNameTXT3=concat(['RemovedCH_AftSpMap_',filename_noExt,'.txt'])
# NeuronsAnalysis_v12_2018.m:274
    save(saveNameTXT3,'Excl','-ascii')
    fprintf('%s\n','Removed extra channels after spike map saved to .txt.')
    # plot again spike map after cleaning
# SpikeMap(InputData, SpykeWidth, waveforms, color,g)
    SpikeMap(spk_w_clean_aftSpMap,10,0,'b',20)
    # if (ImportNewData)
    clear('title')
    title(concat([sprintf('ch %.f,',ichan),fileName]),'Interpreter','none')
