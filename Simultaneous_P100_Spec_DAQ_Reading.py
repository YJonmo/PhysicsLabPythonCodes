import h5py
import DAQT7_Objective as DAQ
import SeaBreeze_Objective as SBO
import ThorlabsPM100_Objective as P100
import time
import datetime
import numpy as np
from multiprocessing import Process, Pipe, Value, Array
import matplotlib.pyplot as plt
import os.path

time_start =  time.time()



# ####################### Interrupt like delays (s) ####################### '''
# Usage Ex: Px = Process(target=Timer_Multi_Process, args=(Timer_time,))
# Px.start() and in your code constantly check for "Timer_Is_Done"

def Timer_Process(Time_In_Seconds):
    if Timer_Is_Done.value is 1:
        print 'Error: This timer can be run one at a time. Either the previous timer is still running, or Timer_Is_Done bit is reset from previous timer run'
    time.sleep(Time_In_Seconds)
    Timer_Is_Done.value = 1


# ########## A function for reading the spectrometer intensities ########### '''
def Spec_Read_Process():
    print 'Spectrumeter is waiting'
    Intensities = Spec1.Read(True, True, Correct_nonlinearity) # The ' True' and 'True' refers to Spec_handle, Correct_dark_counts respectively
    Spec_Current_Record[:] = Intensities
    Spec_Is_Read.value = 1
    #print "Intensities are read"
    return

# ######## A function for reading the DAQ analogue inpute on AINX ########
def DAQ_Read_Process(Nothing,):
    print ("Started")
    results = DAQ1.portRead(PhotoDiod_Port)
    Current_DAQ_Signal = results[0]
    Current_DAQ_Time = time.time()
    DAQ_Is_Read.value = 1
    return

# ######## A function for reading the Power meter ########
def Power_Read_Process():
    results = DAQ.AIN_Read(DAQ_handle, PhotoDiod_Port)
    Current_Power_Signal[:] = results[0]
    Current_Power_Time[:] = time.time()
    Power_Is_Read.value = 1
    return


if __name__ == "__main__":

    PhotoDiod_Port = "AIN0"
    #Spectrometer_Trigger_Port = "DAC0"

    Spec1 = SBO.open()
    Spec1.setTriggerMode(0)                                      # It is set for free running mode
    Spec1.setIntegrationTime(10000)                             # Integration time is 10ms

    DAQ1 = DAQ.open()

    Power_meter = P100.open()

    Spec_Is_Read = Value('i', 0)
    Spec_Is_Read.value = 0
    DAQ_Is_Read = Value('i', 0)
    DAQ_Is_Read.value = 0
    Power_Is_Read = Value('i', 0)
    Power_Is_Read.value = 0
    Timer_Is_Over = Value('i', 0)
    Timer_Is_Over.value = 0


    No_DAC_Sample = 1000       # Number of samples for Photodiod per iteration of the laser exposer. Every sample takes ~0.6 ms.
    No_Power_Sample = No_DAC_Sample/2
    No_Spec_Sample = No_DAC_Sample/2

    Current_Spec_Record = Array('d', np.zeros(shape=( len(Spec1.Handle.wavelengths()) ,1), dtype = float ))
    Full_Spec_Records = np.zeros(shape=(len(Spec1.Handle.wavelengths()), No_Spec_Sample ), dtype = float )

    DAQ_Signal = np.zeros(No_DAC_Sample)
    DAQ_Time   = np.zeros(No_DAC_Sample)
    Current_DAQ_Signal = Array('d', np.zeros(shape=( 1 ,1), dtype = float ))
    Current_DAQ_Time = Array('d', np.zeros(shape=( 1 ,1), dtype = int ))


    Power_Signal = np.zeros(No_Power_Sample)
    Power_Time   = np.zeros(No_Power_Sample)
    Current_Power_Signal = Array('d', np.zeros(shape=( 1 ,1), dtype = float ))
    Current_Power_Time = Array('d', np.zeros(shape=( 1 ,1), dtype = int ))


    # ########### The file containing the records (HDF5 format)###########'''

    DAQ_Index = 0
    Power_Index = 0
    Spec_Index = 0
    Pros_DAQ = Process(target=DAQ_Read_Process, args=(1,))
    Pros_DAQ.start()
    while DAQ_Index < No_DAC_Sample:
	print DAQ_Index
        if  DAQ_Is_Read.value == 1:
            DAQ_Is_Read.value = 0
            Pros_DAQ = Process(target=DAQ_Read_Process, args=(1,))
            Pros_DAQ.start()
            DAQ_Signal[DAQ_Index] = Current_DAQ_Signal[0]
            DAQ_Time[DAQ_Index]   = Current_DAQ_Time[0]
            DAQ_Index = DAQ_Index + 1
	    print DAQ_Index
	'''
        if  Power_Is_Read.value == 1:
            Power_Is_Read.value = 0
            Pros_Power = Process(target=Power_Read_Process, args=())
            Pros_Power.start()
            Power_Signal[Power_Index] = Current_Power_Signal
            Power_Time[Power_Index]   = Current_Power_time
            Power_Index = Power_Index + 1

        if  Spec_Is_Read.value == 1:
            Spec_Is_Read.value = 0
            Pros_Spec = Process(target=Spec_Read_Process, args=())
            Pros_Spec.start()
            Spec_Full_Records[:, Spec_Index] = Spec_Full_Records
            Spec_Time[Spec_Index]   = Current_Spec_time
            Spec_Index = Spec_Index + 1
	'''



    # ######### Plotting the spectrumeter and the photodiod recordings ########
    plt.figure()

    DAQ_Time2 = DAQ_Time[:] - DAQ_Time[0]
    plt.subplot(1,3,1)
    plt.plot(DAQ_Time2, DAQ_Signal, label = "Photo Diode")
    plt.title('Photo diode')
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (v)')

    plt.subplot(1,3,2)
    Power_Time2 = Power_Time[:] - Power_Time[0]
    plt.plot(Power_Time2, Power_Signal, label = "Power meter")
    plt.title('Power meter')
    plt.xlabel('Time (s)')
    plt.ylabel('Pwor (w)')



    plt.subplot(1,3,3)
    plt.plot(Spec.getWavelength()[1:],Spec_Full_Records[1:])
    plt.title('Specrometer recordings')
    plt.xlabel('Wavelength (nano meter)')
    plt.ylabel('Intensity')
    plt.pause(1)
