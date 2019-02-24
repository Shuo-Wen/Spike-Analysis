import numpy as np
from scipy import signal

def isNotValid(above,limit):
    global time
    if len(time)==0 or time.shape[1] != above.shape[1]:
        time=linspace(1,above.shape[1],above.shape[1]))

    tmp=np.zeros((1,1),float)

    if not len(above)==0 and above[0,0] == 1:
        above=np.hsatck((tmp,above))
        time=linspace(1,above.shape[1] + 1,above.shape[1])
        problem=max(scipy.signal.square(above,time,'Polarity','Positive')) >=limit
        #There's no pulsewidth in python
    else:
        above=double(above)
        problem=max(pulsewidth(above,time,'Polarity','Positive')) >= limit

    if len(problem)==0:
        problem=0

    return problem
