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
