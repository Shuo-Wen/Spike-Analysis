
def getAbove(RMS,limit):
    global x

    if len(x)==0 or x.shape[1] != RMS.shape[1]:
        x=linspace(1,RMS.shape[1],RMS.shape[1]).T
# getAbove.m:6

    RMSFit=np.polyfit(x,RMS.T,1)
#
    slope_scalar=RMSFit[0]

    if abs(slope_scalar) > limit:
        above = RMS > RMSFit[x].T
        doubts=0
    else:
        above=0
        doubts = RMS > RMSFit[x].T

    return above,doubts
