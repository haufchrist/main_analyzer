def expdetails(basedirectory, date):
    import os
    import time
    import numpy as np
    import re
    import matplotlib.pyplot as plt
    import scipy.optimize as optimization
    from scipy.special import erf
    from math import pi
    from tkinter import messagebox
    from tkinter import filedialog

    radian=(1/180*pi)
    e0 = 1.60221e-19

    #basedirectory = 'E:\\projects\\LiB3O5\\singlecrystaldata\\'

    expdetailsfilename = basedirectory + 'Experimental_details.txt'

    with open(expdetailsfilename, 'r') as f:
            data = []
            next(f)
            next(f)
            for line in f:
                data.append([float(x) for x in re.split(r'\t+', line)])
                
    
    nodate = 0
    for i in range(0, len(data)):
        
        if(data[i][0]==date):
            nodate = nodate + 1
            t0_BBO        = int(data[i][1])
            t0_Bi111      = int(data[i][2])
            reflection    = data[i][3]
            theta_xray    = data[i][4]
            theta_pump    = data[i][5]
            FWHM_pump     = data[i][6]
            puls_duration = data[i][7]
            puls_energy   = data[i][8]
            photon_energy = data[i][9]
            beta_tpa      = data[i][10]
            n             = data[i][11]
            Vu            = data[i][12]

            
##            print('\n')
##            print('t0_BBO = ' + str(int(t0_BBO)) + ' fs' + '\t'+ 't0_Bi111 = ' + str(int(t0_Bi111)) + ' fs')
##            print('Reflection hkl = (' + str(int(reflection)) + ')' + '\t'+ 'Theta_xray = ' + str(theta_xray) + '°' + '\t'+ 'Theta_pump = ' + str(theta_pump) + '°')
##            print('FWHM_pump = ' + str(FWHM_pump) + ' µm' + '\t'+ 'Tau = ' +  str(puls_duration) + 'fs' + '\t\t'+ 'Puls energy = ' + str(puls_energy) + 'µJ')
##            print('photon_energy = ' + str(photon_energy) + ' eV' + '\t'+ 'TPA: beta = ' + str(beta_tpa) + 'cm/GW'+ '\t'+ 'Refractive index n = ' + str(n) + '\n')
            
            theta_in = 90 -(theta_xray + theta_pump)
            theta_tr = np.arcsin((1/n)*np.sin(theta_in*radian))/radian
            Ti= np.cos(theta_in*radian)/ np.cos(theta_tr*radian)
            Ip = (puls_energy*(1e-6)*Ti)/(FWHM_pump*(1e-6)*FWHM_pump*(1e-6)*puls_duration*(1e-15))            
            alpha_tpa = Ip*beta_tpa*(1e-11)
            n_eh= (Ip * puls_duration*(1e-15) *  alpha_tpa) /(2*photon_energy*e0)
##            print('Peak Intensity = ' + str(round(Ip*(1e-13), 1)) + ' GW/cm2' + '\t' +  'Exitation depth = ' + str(round((1/alpha_tpa)*(1e6),2)) + ' µm' )
##            print('Exitation density = ' + str(round(n_eh*(1e-25), 3)) + '*10^19 e-h+ pairs per pulse and cm3 ' )
            n_ehUC = n_eh * Vu *(1e-30)
##            print(str(round(n_ehUC, 4)) + 'e-h+ pairs per Unit Cell')


            
    if(nodate == 0):
        messagebox.showwarning('Error', '!! This date is not included in the list of experiments !!')

    if(nodate == 1):

        messagebox.showwarning('Info', 'Date: ' + str(date) + '\n\n'
                                + 't0_BBO = ' + str(int(t0_BBO)) + ' fs' + '\t\t'+ 't0_Bi111 = ' + str(int(t0_Bi111)) + ' fs\n\n'
                                + 'Reflection hkl = (' + str(reflection) + ')' + '\t'+ 'Theta_xray = ' + str(theta_xray) + '°\n\n'
                                + 'FWHM_pump =  ' + str(FWHM_pump) + ' µm' + '\t'+ 'Tau = ' +  str(puls_duration) + 'fs\n\n'
                                + 'puls energy = ' + str(puls_energy) + 'µJ ' + '\t\t' + 'photon_energy = ' + str(photon_energy) + ' eV\n\n'
                                + 'TPA: beta = ' + str(beta_tpa) + 'cm/GW'+ '\t'+ 'Refractive index n = ' + str(n) + '\n\n'
                                + 'Ipeak = ' + str(round(Ip*(1e-13), 1)) + ' GW/cm2' + '\t' +  'Exitation depth = ' + str(round((1/alpha_tpa)*(1e6),2)) + ' µm\n\n'
                                + 'Exitation density = ' + str(round(n_eh*(1e-25), 3)) + '*10^19 e-h+ pairs per pulse and cm3\n\n'
                                + str(round(n_ehUC, 4)) + 'e-h+ pairs per Unit Cell')
    
    if(nodate > 1):
        messagebox.showwarning('Error', '!! This date is included in the list of experiments more than once !!')

    return(t0_BBO, t0_Bi111)
