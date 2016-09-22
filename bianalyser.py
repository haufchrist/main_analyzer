def bianalyser(bidelayzero, bidirectory, intervallwidth, maxphotons, stackingthreshold):
    import os
    import time
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy.optimize as optimization
    from scipy.special import erf

    directory = bidirectory

    datfiles = []

    ntp = 25
    MaxDelay =  5000
    MinDelay = -5000

    resultdirectory = directory + 'reduced_' + str(intervallwidth) + '_' + str(maxphotons) + '_' + str(stackingthreshold)+ '_' + str(bidelayzero)+'\\'

    for file in os.listdir(resultdirectory):
        if file.endswith('.dat'):
            datfiles.append(file)
            
    data = []
    delays = []
    dIoverI = []
    derr = []       ## Uncertainty of average delay
    Ierr = []       ## Uncertainty of average dIoverI
    nap = []        ## Number of averaged points
    SNR = []        ## Signal to Noise ratio
    overallerror = 0
    michcrit = 0


    for i in range(0, len(datfiles)):
        
        filename = (resultdirectory + datfiles[i])
        spitfilename = os.path.splitext( os.path.basename(filename))
        filenameparts = spitfilename[0].split('_')


        with open(filename, 'r') as f:
            for line in f: 
                data.append([float(x) for x in line.split('\t')])
                

    sorteddata = sorted(data, key=lambda data: data[1])


    intervalmin = 0
    intervalmax = 0
    
    for i in range (0, len(sorteddata)):
        if (sorteddata[i][1]) < MinDelay:
            intervalmin = i
        if (sorteddata[i][1]) < MaxDelay:
            intervalmax = i

    numberofusedstacks = intervalmax - intervalmin
    stacksperdelaypoint=int((numberofusedstacks-(numberofusedstacks%ntp))/ntp)

    for i in range (0, ntp):

        stackcounter = 0
        bineddelays=[]
        bineddIoverI =[]
        
        for j in range(0, stacksperdelaypoint):
            stackcounter=intervalmin+(i*stacksperdelaypoint)+j
            bineddelays.append(sorteddata[stackcounter][1])
            bineddIoverI.append(sorteddata[stackcounter][6])
                    
        delays.append(np.mean(bineddelays))
        derr.append( (np.std(bineddelays))  /  (np.sqrt((len(bineddelays))))  )
        dIoverI.append(np.mean(bineddIoverI))
        Ierr.append(  (np.std(bineddIoverI))  /  (np.sqrt((len(bineddIoverI))))  )
        nap.append(len(bineddIoverI))
        SNR.append(np.absolute((np.mean(bineddIoverI))/(  (np.std(bineddIoverI))  /  (np.sqrt((len(bineddIoverI)))))))

    overallerror = 100 * np.mean(Ierr)
    michcrit = np.std(dIoverI) / np.mean(Ierr)
    timereso = (MaxDelay - MinDelay)/ntp


    dIoverI_before = []
    delays_before = []

    for i in range (0, ntp):
        if delays[i] < 0:
            delays_before.append(delays[i])
            dIoverI_before.append(dIoverI[i])


    resultsfilename = resultdirectory + filenameparts[0] + '_' + filenameparts[1] + '_' + str(ntp) + '_transient.res'
    with open(resultsfilename, 'w') as f:    
        for i in range (0, ntp):
           f.write("{0:03d}\t {1:+07.2f}\t {2:05.2f}\t {3:+02.6f}\t {4:+02.6f}\t {5:05d}\n".format(i, delays[i], derr[i], dIoverI[i], Ierr[i], nap[i] ))


    init = np.array([7.0, 0.0 , 110.0, -7.0, 0.001])
    minidelays = []

    for i in range (0, MaxDelay-MinDelay):
        minidelays.append(MinDelay+i)

    npdelays = np.asarray(delays)
    npdIoverI = np.asarray(dIoverI)
    npminidelays = np.asarray(minidelays)
    fittedtzero = 0
        
    def mfitFunct(x, S, x0, w, bg ,a):
        return ( S*(erf(-(x-x0)/w)) + bg + (0.5*(np.sign(x-x0) + 1)) * a * (x-x0))/100

    fitParams = optimization.curve_fit(mfitFunct, npdelays, npdIoverI, init)

    fittedtzero = int(bidelayzero - fitParams[0][1])

    plt.figure()

    ax1 = plt.subplot2grid((4,4), (0,0), colspan = 4, rowspan=3)
    plt.xlim(min(delays)*1.05, max(delays)*1.05)
    plt.ylabel(r'$\Delta I$' + ' / ' + r'$I$', fontsize = 14)
    plt.title('Transient with ' + str(ntp) + ' points; ' + ' Time resolution = ' + str(round(timereso , 1)) + ' fs' + '\n' + 
              r'$\overline{Err}$' + ' = ' + str(round(overallerror , 4)) + ' %;  ' +
     r'$\overline{\Delta I / I}$' + ' (t<0) = '+ str(round((np.mean(dIoverI_before)*100), 4)) + ' %; MichCrit = ' + str(round(michcrit,3)) + '; Fitted ' + r'$t_0$'+ ' = ' + str(int(fittedtzero)) , fontsize = 12)
    plt.errorbar(delays, dIoverI, xerr = derr, yerr = Ierr, fmt='o' )
    plt.plot(npminidelays, mfitFunct(npminidelays, fitParams[0][0], fitParams[0][1], fitParams[0][2], fitParams[0][3], fitParams[0][4]))
    plt.grid(True)


    ax2 = plt.subplot2grid((4,4), (3,0), colspan = 4, rowspan=1,sharex=ax1)
    plt.xlabel('Delay [fs]', fontsize = 14)
    plt.ylabel(r'$SNR$', fontsize = 14)
    plt.scatter(delays, SNR, c= SNR, s=50)
    plt.locator_params(axis='y',nbins=4)
    plt.xlim(min(delays)*1.05, max(delays)*1.05)
    plt.grid(True)

    plt.tight_layout()
    figurename = resultdirectory + filenameparts[0] + '_' + filenameparts[1] + '_' + str(ntp) + '_transient.pdf'
    plt.savefig(figurename)
    plt.show()

    return fittedtzero
