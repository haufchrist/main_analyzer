from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import sys
import datetime
import time
import threading
import matplotlib.pyplot as plt

import bireducer
import bianalyser
import mainreducer
import mainanalyser
import fluxanalyser
import voltagesanalyser
import expdetails


class Application(tk.Frame):


    def OpenFolder(self):
        try:
            self.basedirectory = 'E:\\projects\\LiB3O5\\singlecrystaldata\\'
            self.directory = filedialog.askdirectory(initialdir=self.basedirectory) + '/'
            self.dirparts = self.directory.split('/')
            self.date=int(self.dirparts[-3])
            messagebox.showwarning('Info', str(self.directory) + '\nhas been selected as sample directory' )
        except Exception as ex1:
            messagebox.showwarning('Error', 'Please choose a valid sample directory!' )
            


    def expdetails(self):
        try:
            (self.t0_BBOtt, self.t0_Bi111) =  expdetails.expdetails(self.basedirectory, self.date)
        except Exception as ex2:
            messagebox.showwarning('Error', 'Please choose a valid sample directory!' )


    def voltages(self,*args):
        try:
            self.maxphotons = int(self.maxphotons_Entry.get())
            voltagesanalyser.voltagesanalyser(self.intervallwidth, self.maxphotons, self.directory, self.delaysperscan, self.pointsperdelay, self.voltoffset, self.voldifference)
        except Exception as ex3:
            messagebox.showwarning('Error', 'Please choose a valid sample directory!' )

            
    def reducer(self, *args):
        try:
            messagebox.showwarning('Info', 'From now up to ' + str(self.maxphotons) + ' photon events will be considered during data reduction!\n' +
                                   'From now T0 =  ' + str(self.t0_BBOtt) + ' fs will be considered during data reduction!\n')
            self.stackingthreshold = int(self.stackingthreshold_Entry.get())
            mainreducer.mainreducer(self.delaysperscan, self.pointsperdelay, self.intervallwidth, self.maxphotons, self.stackingthreshold, self.t0_BBOtt, self.directory, self.voltoffset, self.voldifference)
        except Exception as ex4:
            print(ex4)
            
    def analyser(self, *args):
        try:
            self.ntp = int(self.ntp_Entry.get())
            self.MaxDelay = int(self.MaxDelay_Entry.get())
            self.MinDelay = int(self.MinDelay_Entry.get())
            self.offset = float(self.offset_Entry.get())
            mainanalyser.mainanalyser(self.intervallwidth, self.maxphotons, self.stackingthreshold,  self.t0_BBOtt, self.directory, self.ntp, self.MaxDelay, self.MinDelay, self.offset)
        except Exception as ex5:
            print(ex5)
            
            
    def QuitHandler(self):
        if messagebox.askokcancel("Quit?", "Are you sure you want to quit?"):
            root.quit()



    def __init__(self, master=None):

        self.delaysperscan = 50
        self.pointsperdelay = 5000

        self.voltoffset = 0.106
        self.voldifference = 0.0330

        self.intervallwidth = 7000


        self.maxphotons = 17
        self.stackingthreshold = 20
        self.ntp = 40
        self.MaxDelay =  20000
        self.MinDelay = -11000
        self.offset = 0
        
   
        tk.Frame.__init__(self, master)

        ##Data selection##
        self.FolderButton = ttk.Button(master , text="Data selection", command=self.OpenFolder, takefocus = False)
        self.FolderButton.grid(row=0, column=0, sticky='nsew', ipady=25)

        ##Experimental Details##
        self.ExpButton = ttk.Button(master , text="Exp Details", command=self.expdetails, takefocus = False)
        self.ExpButton.grid(row=0, column=1, sticky='nsew', ipady=25)
   
        ##Check Voltages##
        self.VoltagesButton = ttk.Button(master , text="Check Voltages", command=self.voltages, takefocus = False)
        self.VoltagesButton.grid(row=0, column=2, sticky='nsew', ipady=25)

        self.label1 = ttk.Label(master,font='Helvetica 12',text='Max Photons')
        self.label1.grid(row=1,column=2,padx=25,pady=25)

        self.maxphotons_Entry = ttk.Entry(master,width=10,justify=tk.CENTER)
        self.maxphotons_Entry.insert(0,str(self.maxphotons))
        self.maxphotons_Entry.grid(row=2,column=2,ipady=5,pady=2)
        self.maxphotons_Entry.bind('<Return>',self.voltages)

        ##Reduce Data##
        self.ReducerButton = ttk.Button(master , text="Reduce Data", command=self.reducer, takefocus = False)
        self.ReducerButton.grid(row=0, column=3, sticky='nsew', ipady=25)

        self.label2 = ttk.Label(master,font='Helvetica 12',text='Stacking Threshold')
        self.label2.grid(row=1,column=3,padx=25,pady=25)

        self.stackingthreshold_Entry = ttk.Entry(master,width=10,justify=tk.CENTER)
        self.stackingthreshold_Entry.insert(0,str(self.stackingthreshold))
        self.stackingthreshold_Entry.grid(row=2,column=3,ipady=5,pady=2)
        self.stackingthreshold_Entry.bind('<Return>',self.reducer)


        ##Analyse Data##
        self.AnalyserButton = ttk.Button(master , text=" Analyse Data ", command=self.analyser, takefocus = False)
        self.AnalyserButton.grid(row=0, column=4, columnspan = 4, sticky='nsew', ipady=25)

        self.label3= ttk.Label(master,font='Helvetica 12',text='Number of Points')
        self.label3.grid(row=1,column=4,padx=25,pady=25)
        
        self.ntp_Entry = ttk.Entry(master,width=10,justify=tk.CENTER)
        self.ntp_Entry.insert(0,str(self.ntp))
        self.ntp_Entry.grid(row=2,column=4,ipady=5,pady=2)
        self.ntp_Entry.bind('<Return>',self.analyser)


        self.label4= ttk.Label(master,font='Helvetica 12',text='Offset')
        self.label4.grid(row=1,column=5,padx=25,pady=25)
        
        self.offset_Entry = ttk.Entry(master,width=10,justify=tk.CENTER)
        self.offset_Entry.insert(0,str(self.offset))
        self.offset_Entry.grid(row=2,column=5,ipady=5,pady=2)
        self.offset_Entry.bind('<Return>',self.analyser)


        self.label6= ttk.Label(master,font='Helvetica 12',text='Minimum Delay')
        self.label6.grid(row=1,column=6,padx=25,pady=25)
        
        self.MinDelay_Entry = ttk.Entry(master,width=10,justify=tk.CENTER)
        self.MinDelay_Entry.insert(0,str(self.MinDelay))
        self.MinDelay_Entry.grid(row=2,column=6,ipady=5,pady=2)
        self.MinDelay_Entry.bind('<Return>',self.analyser)
        

        self.label5= ttk.Label(master,font='Helvetica 12',text='Maximum Delay')
        self.label5.grid(row=1,column=7,padx=25,pady=25)
        
        self.MaxDelay_Entry = ttk.Entry(master,width=10,justify=tk.CENTER)
        self.MaxDelay_Entry.insert(0,str(self.MaxDelay))
        self.MaxDelay_Entry.grid(row=2,column=7,ipady=5,pady=2)
        self.MaxDelay_Entry.bind('<Return>',self.analyser)

        

        master.protocol('WM_DELETE_WINDOW', self.QuitHandler)
        master.resizable(width=False, height=False)
        master.title('Haufys Signalyser')

        



root = tk.Tk()
app = Application(master=root)
app.mainloop()
