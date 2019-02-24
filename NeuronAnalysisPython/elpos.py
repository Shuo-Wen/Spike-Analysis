import numpy as np
def elpos(debug):
# Parameter Settings
    well_pitch=20
    nchans=1024
    nchans_per_well=256
    nchans_per_side=sqrt(nchans_per_well)

    x=np.zeros((nchans,1),float)
    y=np.zeros((nchans,1),float)

    # Well 1
    w=1
# elpos.m:16
    xw[2]=0
# elpos.m:17
    yw[2]=0
# elpos.m:18
    x[dot((w - 1),nchans_per_well) + (arange(1,nchans_per_well))]=xw(1) + mod((arange(1,nchans_per_well)) - 1,nchans_per_side) + 1
# elpos.m:19
    y[dot((w - 1),nchans_per_well) + (arange(1,nchans_per_well))]=yw(1) + fix(((arange(1,nchans_per_well)) - 1) / nchans_per_side) + 1
# elpos.m:20
    # Well 2
    w=2
# elpos.m:23
    xw[w]=0
# elpos.m:24
    yw[w]=well_pitch
# elpos.m:25
    x[dot((w - 1),nchans_per_well) + (arange(1,nchans_per_well))]=xw(w) + mod((arange(1,nchans_per_well)) - 1,nchans_per_side) + 1
# elpos.m:26
    y[dot((w - 1),nchans_per_well) + (arange(1,nchans_per_well))]=yw(w) + fix(((arange(1,nchans_per_well)) - 1) / nchans_per_side) + 1
# elpos.m:27
    # # Well 3
    w=3
# elpos.m:30
    xw[w]=well_pitch
# elpos.m:31
    yw[w]=0
# elpos.m:32
    x[dot((w - 1),nchans_per_well) + (arange(1,nchans_per_well))]=xw(w) + nchans_per_side - mod((arange(1,nchans_per_well)) - 1,nchans_per_side) + 1
# elpos.m:33
    y[dot((w - 1),nchans_per_well) + (arange(1,nchans_per_well))]=yw(w) + fix(((arange(1,nchans_per_well)) - 1) / nchans_per_side) + 1
# elpos.m:34
    # # Well 3
    w=4
# elpos.m:37
    xw[w]=well_pitch
# elpos.m:38
    yw[w]=well_pitch
# elpos.m:39
    x[dot((w - 1),nchans_per_well) + (arange(1,nchans_per_well))]=xw(w) + nchans_per_side - mod((arange(1,nchans_per_well)) - 1,nchans_per_side) + 1
# elpos.m:40
    y[dot((w - 1),nchans_per_well) + (arange(1,nchans_per_well))]=yw(w) + fix(((arange(1,nchans_per_well)) - 1) / nchans_per_side) + 1
# elpos.m:41
    pitch=15
# elpos.m:43
    elx=dot(pitch,x)
# elpos.m:44
    ely=dot(pitch,y)
# elpos.m:45
    max_xy=max(elx) + pitch
# elpos.m:46
    ## Comment if not in debugging mode
    for i in arange(1,dot(w,nchans_per_well)).reshape(-1):
        el(i).x = copy(dot(pitch,x(i)))
# elpos.m:50
        el(i).y = copy(dot(pitch,y(i)))
# elpos.m:51

    max_xy=max(concat([ravel(el).x])) + pitch
# elpos.m:53

    ##
    if (debug):
        figure
        for i in arange(1,dot(w,nchans_per_well)).reshape(-1):
            #text(el.x(i), max_xy-ely(i), sprintf('#d',i)); # Actual Data script
            text(el(i).x,max_xy - el(i).y,sprintf('%d',i))
            hold('on')
        xlim(concat([0,max_xy]))
        ylim(concat([0,max_xy]))
