def fluxanalyser(intervallwidth, maxphotons, stackingthreshold, delayzero, sampledirectory, ntp, MaxDelay, MinDelay, offset):
    
    import os
    import time
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy.optimize as optimization
    from scipy.special import erf

    datfiles = []


    resultdirectory = sampledirectory + 'reduced_' + str(intervallwidth) + '_' + str(maxphotons) + '_' + str(stackingthreshold)+ '_' + str(delayzero)+'\\'

    for file in os.listdir(resultdirectory):
        if file.endswith('.dat'):
            datfiles.append(file)


    data = []
    photons = []
    photonsperdelay = []
    delays = []

    for i in range(0, len(datfiles)):
        
        filename = (resultdirectory + datfiles[i])
        spitfilename = os.path.splitext( os.path.basename(filename))
        filenameparts = spitfilename[0].split('_')


        with open(filename, 'r') as f:
            for line in f: 
                data.append([float(x) for x in line.split('\t')])
    sorteddata = sorted(data, key=lambda data: data[0])

    delay = sorteddata[i][1]
    photons = 0

    for i in range(0, len(sorteddata)):
        if(sorteddata[i][1] == delay):
            photons = photons +( sorteddata[i][4] + sorteddata[i][5])
        else:
            photonsperdelay.append(photons)
            delays.append(delay)
            photons=0
            delay=sorteddata[i][1]
            photons = photons +( sorteddata[i][4] + sorteddata[i][5])
            
    photonsperdelay.append(photons)
    delays.append(delay)
    maximum=max(delays)
    minimum=min(delays)

    analyticsdirectory = sampledirectory + 'Analytics' +'\\'
    if not os.path.exists(analyticsdirectory):
        os.makedirs(analyticsdirectory)  

    plt.plot(photonsperdelay)
    plt.title('Number of detected Photons per Delay Point' + '\n' + 'over the course of the measurement')
    plt.xlabel('Serial Number of Delay point')
    plt.ylabel('# Photons per Delay point ')
    figurename = analyticsdirectory + 'Flux_per_delay.pdf'
    plt.savefig(figurename)
    plt.show()

                
    plt.hist(delays, 50)
    plt.xlabel('Delay time')
    plt.title('Histogram of the Delay times')
    figurename = analyticsdirectory + 'Delay_histogram.pdf'
    plt.savefig(figurename)
    plt.show()

    return(maximum, minimum)
    
            

        
        
        
