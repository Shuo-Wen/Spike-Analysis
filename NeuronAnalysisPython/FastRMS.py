def FastRMS(data,numberOfSamples):
    global appoggio
    if len(appoggio)==0 or appoggio.shape[1] != data.shape[1]:
        appoggio=np.zeros((1,data.shape[1]),float)

    RMS=appoggio

    for i in range(data.shape[1] - numberOfSamples):
        RMS[i] = np.sqrt(np.mean(data[i:i + numberOfSamples]**2))

    return RMS
