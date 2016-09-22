def voltagesanalyser(intervallwidth, maxphotons, directory, delaysperscan, pointsperdelay, voltoffset, voldifference):
    import os
    import time
    import numpy as np
    import re
    import matplotlib.pyplot as plt
    import scipy.optimize as optimization
    from scipy.special import erf
   
    ## Create boundaries ##
    plt.ion()
    boundaries=[]

    for bb in range (0, maxphotons+1):
        boundaries.append([(voltoffset+(bb*voldifference)) - (intervallwidth/(2*245031)),
                           (voltoffset+(bb*voldifference)) + (intervallwidth/(2*245031))])

            
    ##Import datfiles from specified directory while ignoring subdirectories,
    ## then the list of files is sorted numericaly ##
            
    datfilesimp = [f for f in os.listdir(directory) if (os.path.isfile(os.path.join(directory, f)))]
    datfiles = sorted(datfilesimp, key=lambda x: (int(re.sub('\D','',x)),x))


    ## Evaluate up to 10 datfiles in a loop ##
    datlen=len(datfiles)
    if(datlen > 10):
        datlen = 10
        
    photons = []
    voltages = []

    #print('\nAnalysing Amptek voltages')

    for h in range(0, datlen):

        ## Extract Information out of Filename of Scanfile##
        filename = (directory + datfiles[h])
        start = time.clock()
        spitfilename = os.path.splitext( os.path.basename(filename))
        filenameparts = spitfilename[0].split('_')       
        scannumber = int(filenameparts[4])


        ## Import one entire Scanfile consiting of 50 Delay-Points ##

        with open(filename, 'r') as f:
            data = []
            for line in f: 
                data.append([float(x) for x in line.split('\t')])


        ## Evaluate one Delay-Point after the other in a loop over all 50 Delay-Points ##


        for i in range(0, delaysperscan):


            ## Check if voltage is within one of the Intervall set by the boundaries ##
            ## and update the Photonnumber per Shot in the Potons-Array accordingly ##
            
            for j in range(1, pointsperdelay+1):
                voltages.append(data[i][j])
                for k in range(0, maxphotons+1):
                    if boundaries[k][0] < data[i][j] <boundaries[k][1]:
                        photons.append(k)
                        
    analyticsdirectory = directory + 'Analytics' +'\\'
    if not os.path.exists(analyticsdirectory):
        os.makedirs(analyticsdirectory)       

    plt.figure(1)
    plt.clf()
    plt.hist(voltages, bins=1024)
    plt.yscale('log', nonposy='clip')

    for i in range(0, maxphotons+1):

        plt.plot((boundaries[i][0], boundaries[i][0]), (0, 1000000), color='b')
        plt.plot((boundaries[i][1], boundaries[i][1]), (0, 1000000), color='r')
    plt.xlabel(r'$U$' + ' (V)')
    plt.title('Histogram of the measured Amptek voltages')    
    figurename = analyticsdirectory + 'Voltages_histogram.pdf'
    plt.savefig(figurename)
    plt.show()
    binsp=[]
                        
    for i in range(0, (maxphotons+1)*4):
        binsp.append((i/4)-0.25)


##    plt.figure(2)
##    plt.clf()
##    plt.hist(photons, binsp)
##    plt.yscale('log', nonposy='clip')
##    plt.xlabel('# Photons per pulse')
##    plt.title('Histogram of the number of Photons per puls ')
##    figurename = analyticsdirectory + 'Photons_histogram.pdf'
##    plt.savefig(figurename)
##    plt.show()
