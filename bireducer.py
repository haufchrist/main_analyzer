def bireducer(delaysperscan, pointsperdelay, intervallwidth, maxphotons, stackingthreshold, bidelayzero, bidirectory, voltoffset, voldifference):

    import os
    import time
    import numpy as np
    import re

    directory = bidirectory
    
    ## Create boundaries ##

    boundaries=[]

    for bb in range (0, maxphotons+1):
        boundaries.append([(voltoffset+(bb*voldifference)) - (intervallwidth/(2*245031)),
                           (voltoffset+(bb*voldifference)) + (intervallwidth/(2*245031))])

            
    ##Import datfiles from specified directory while ignoring subdirectories,
    ## then the list of files is sorted numericaly ##
            
    datfilesimp = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    datfiles = sorted(datfilesimp, key=lambda x: (int(re.sub('\D','',x)),x))


    ## Evaluate all datfiles in a loop ##

    for h in range(0, len(datfiles)):


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


        ## Calculate the mean Chopper-Voltage over the all 50 Delay-Points of the Scanfile ##
                
        mean = 0
        
        for i in range(0, delaysperscan):
                for j in range(pointsperdelay+1, 2*pointsperdelay+1):
                        mean = mean + data[i][j]/(delaysperscan*pointsperdelay)


        ## Evaluate one Delay-Point after the other in a loop over all 50 Delay-Points ##

        stackinfo = []

        for i in range(0, delaysperscan):
            pcounts = 0
            ucounts = 0
            deltaIoverI = 0
            pumped = []
            unpumped = []
            photons = []
            delay=((data[i][0]-bidelayzero) * -1)

            ## Re-Zero the Potons-Array ##
            
            for l in range(0, pointsperdelay+1):
                photons.append(0)


            ## Check if voltage is within one of the Intervall set by the boundaries ##
            ## and update the Photonnumber per Shot in the Potons-Array accordingly ##
            
            for j in range(1, pointsperdelay+1):
                for k in range(0, maxphotons+1):
                    if boundaries[k][0] < data[i][j] <boundaries[k][1]:
                        photons[j-1] = k

                
                ## Check if the Chopper-Voltage is above or below the mean value and ##
                ## sort the photon number into the pumped or unpumped colum accordingly ##
                
                if data[i][j+pointsperdelay] > mean:
                    pumped.append(photons[j-1])
                        
                elif data[i][j+pointsperdelay] < mean:
                    unpumped.append(photons[j-1])

            ## For each Stack go through the entire Stack and sum up##
            ## as long as number of pumped and unpumped Photons < threshold
            ## to calculate the total number of pumped and unpumped Photons ##
            ## and then deltaIoverI and the error for each substackstack##
            
            pcounts = 0
            ucounts = 0
            deltaIoverI = 0
            stacksize = 0
            stacknumber = 1
            ll = 0
            if len(pumped) != len(unpumped):
                print('!!!Error!!! Unequal Number of pumped and unpumped Shots in Scan '
                      + str(h) + ', Delaypoint' + str(i) )


            for  ll in range(0, len(pumped)):
                
                if ((pcounts < stackingthreshold) or (ucounts < stackingthreshold)):
                    pcounts = pcounts + pumped[ll]
                    ucounts = ucounts + unpumped[ll]
                    ll = ll + 1
                    stacksize = stacksize +1
                    
                    
                else:
                    deltaIoverI = round((2*(pcounts - ucounts))/(pcounts + ucounts),5)
                    #deltaIoverI = round(((pcounts - ucounts))/(ucounts),5)
                    stackinfo.append([scannumber, delay, i+1, stacknumber , pcounts, ucounts, deltaIoverI, stacksize])
                    pcounts = 0
                    ucounts = 0
                    deltaIoverI = 0
                    stacksize = 0
                    stacknumber = stacknumber + 1

                    
        resultdirectory = directory + 'reduced_' + str(intervallwidth) + '_' + str(maxphotons) + '_' + str(stackingthreshold)+ '_' + str(bidelayzero)+'\\'
        if not os.path.exists(resultdirectory):
            os.makedirs(resultdirectory)
        
        resultsfilename = resultdirectory + filenameparts[0] + '_' + filenameparts[1] + '_' + filenameparts[2] + '_' + filenameparts[4] + '_reduced.dat'
        with open(resultsfilename, 'w') as f:
                for line in stackinfo:
                    f.write("{0:03d}\t {1:+07.2f}\t  {2:03d}\t {3:03d}\t {4:5d}\t {5:5d}\t {6:+06.5f}\t {7:5d}\n".format(*line)  )                                 
        f.close()
        end = time.clock()
        print('Bismuth: Scan ' + filenameparts[4] + '\tprocessed in ' + str(round((end-start),3)) + ' Seconds;', str(len(datfiles)-h-1)  + ' files remaining')
    logfilename = directory + 'Bismuth_Reduction_Info.log'
    with open(logfilename, 'w') as f:
            f.write(str(intervallwidth) + '\t')
            f.write(str(maxphotons) + '\t')
            f.write(str(stackingthreshold) + '\t')
            f.write(str(bidelayzero) + '\t')
    f.close()
    print('Bismuth-Logfile has been writen \n')          
                

                
