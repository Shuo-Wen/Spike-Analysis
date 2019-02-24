def extract_extracellular_spikes(data, stdmin, time=None, tpre=None, tpost=None, tdead=None, detection_mode=None):
	import numpy as np
	import math
	from scipy import interpolate
	from find_spike_threshold import find_spike_threshold

################################# Necessary function############################################
	def indices(a, func):
		return [i for (i, val) in enumerate(a) if func(val)]
		#### Interpolates with cubic splines to improve alignment.
	def int_spikes(spikes,w_pre,w_post,detection_mode,int_factor):
		ls=w_pre + w_post
		nspk = spikes.shape[0]
		s=np.arange(1,spikes.shape[1]+1)
		ints=np.linspace(1 / int_factor,spikes.shape[1], 1/int_factor)
		intspikes=np.zeros((1,len(ints)),dtype=float)
		spikes1=np.zeros((nspk,ls),dtype=float)
		absIntspikes = abs(intspikes)

		if 'pos' == detection_mode:
			for i in range(nspk):
				tck = interpolate.splrep(s, spikes[i,:], s=0)
				intspikes = interpolate.splev(ints, tck, der=0)
				maxi,iaux = intspikes[w_pre*int_factor:w_pre*int_factor+8].max(0),intspike[w_pre*int_factor:w_pre*int_factor+8].argmax(0)
				iaux = iaux + w_pre*int_factor-1
				spikes1[i,w_pre:0:-1] = intspikes[iaux:iaux-w_pre*int_factor+int_factor:-int_factor]
				spikes1[i,w_pre+1:ls] = intspikes[iaux+int_factor:iaux + w_post*int_factor:int_factor]

		if 'neg' == detection_mode:
			for i in range(nspk):
				tck = interpolate.splrep(s, spikes[i,:], s=0)
				intspikes = interpolate.splev(ints, tck, der=0)
				maxi,iaux = intspikes[w_pre*int_factor:w_pre*int_factor+8].min(0),intspike[w_pre*int_factor:w_pre*int_factor+8].argmin(0)
				iaux = iaux + w_pre*int_factor-1
				spikes1[i,w_pre:0:-1] = intspikes[iaux:iaux-w_pre*int_factor+int_factor:-int_factor]
				spikes1[i,w_pre+1:ls] = intspikes[iaux+int_factor:iaux + w_post*int_factor:int_factor]

		if 'both' == detection_mode:
			for i in range(nspk):
				tck = interpolate.splrep(s, spikes[i,:], s=0)
				intspikes = interpolate.splev(ints, tck, der=0)
				maxi,iaux = absIntspikes[w_pre*int_factor:w_pre*int_factor+8].max(0),absIntspikes[w_pre*int_factor:w_pre*int_factor+8].argmax(0)
				iaux = iaux + w_pre*int_factor - 1
				spikes1[i,w_pre:0:-1] = intspikes[iaux:iaux-w_pre*int_factor+int_factor:-int_factor]
				spikes1[i,w_pre+1:ls] = intspikes[iaux+int_factor:iaux + w_post*int_factor:int_factor]
#################################################################################################################
	#Setting
	if time is None:
		dt = 1 / 30000
		time  = np.arange(0,data.shape[1]*dt)
	elif len(time)>1:
		dt = time[1]-time[0]
	else:
		dt = time
		time  = np.arange(0,data.shape[1]*dt)
	if tpre is None:
		tpre = 1
	if tpost is None:
		tpost = 1.5
	if tdead is None:
		tdead = 1.5
	if detection_mode is None:
		detection_mode = 'neg'

	interpolation = 'y'
	int_factor = 2
	N = data.shape[0]

	spk     = np.zeros((N,1),dtype=float)
	spk_w   = np.zeros((N,1),dtype=float)

	spk_idx     = np.zeros((N,1),dtype=float)
	threshold     = np.zeros((N,1),dtype=float)

	ref = math.ceil(tdead/1000/dt)
	w_pre = math.ceil(tpre/1000/dt)
	w_post = math.ceil(tpost/1000/dt)

	count = 0
	I=0
	timeList=[]
	#Locate spike time
	for ii in range(N):
		thr = find_spike_threshold(data[ii,:],stdmin)
		threshold[ii] = thr

		if 'pos' == detection_mode:
			dd = data
		elif 'neg' == detection_mode:
			dd = -data
		elif 'both' == detection_mode:
			dd = abs(data)
		nspk = 0;
		#xaux = find(dd(ii,w_pre+2:end-w_post-2) > thr) + w_pre+1 in python we cannot add a number directly
		xaux = np.asarray(np.nonzero(dd[ii,w_pre+2:-(w_post+3)]) > thr, np.float32)
		#Generate an arry with the same size as xaux, all elements are "w_pre+1"

		xaux = np.add(xaux,np.full((xaux.shape[0],xaux.shape[1]), w_pre+1))
		xaux0 = 0
		if not len(xaux):
			continue
		# Addition Bea 29/11/2018
		index = np.zeros((1,len(xaux)),int)
		for i in range(len(xaux)):
			if xaux[0][i] >= xaux0 + ref:
				a = dd[i,xaux[0][i]:(xaux[i]+floor(ref/2)-1)]
				maxi,iaux = a.max(0),a.argmax(0)
				index[0,nspk] = iaux + xaux[0][i] -1
				xaux0 = index[nspk]
				nspk = nspk + 1

		# ###############SPIKE STORING (with or without interpolation)
		ls = w_pre + w_post
		spikes = np.zeros((nspk,ls+4),dtype=float)
		xf = data[ii,:]
		xf = np.hstack((xf,np.zeros((1,w_post)[0],dtype=float)))

		for i in range(nspk):
			if max(abs(xf[index[i]-w_pre:index[i]+w_post])) < thr*50:
				spikes[i,:] = xf[index[i]-w_pre-1:index[i]+w_post + 2]

				#rases indexes that were artifacts###################
		aux=np.where(spikes[:,w_pre] == 0)

		for i in range(len(aux)):
			spikes = np.delete(spikes,(aux[i]),axis=0)
		index = np.delete(index,aux)

		if 'n' == interpolation:
			for i in range(spike.shape[1]):
				np.delete(spike[i],np.s_[-2:])
				np.delete(spikes[i],np.s_[0:2])

		elif 'y' == interpolation:
				#Does interpolation
				spikes=int_spikes(spikes,w_pre,w_post,detection_mode,int_factor)
		if count < len(index):
			index[count]=I
			timeList.append(time[I])
			count+=1
		spk[ii] = np.asarray(timeList, dtype=np.float32)
		spk_w[ii] = spikes
		spk_idx[ii] = index
		#for loop ends here
	print(type(tpre))
	print(type(tpost))
	print(type(dt))
	print(type(time))
	t_spk_w = np.linspace(-tpre-dt, tpost)

	if N < 2:
		spk=spk[0]
		spk_w=spk_w[0]
		spk_idx=spk_idx[0]

		return spk,spk_w,t_spk_w,spk_idx,threshold
