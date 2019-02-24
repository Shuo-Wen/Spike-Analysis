import numpy as np
def find_spike_threshold(x,stdmin):
	if 'stdmin' not in locals():
		stdmin = 5
	thr = stdmin * np.median(abs(x))/0.6745;
	return thr
