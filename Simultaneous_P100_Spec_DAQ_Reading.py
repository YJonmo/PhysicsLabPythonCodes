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




# ########## A function for reading the spectrometer intensities ########### '''
def Spec_Read_Process(No_Spec_Sample):
    for Spec_Index_Process in range(No_Spec_Sample):
        #Time_Label = time.time()
        Current_Spec_Record[:], Spec_Time[Spec_Index_Process]  = Spec1.readIntensity(True, True)
        #Spec_Time[Spec_Index_Process] = (time.time() )
        Spec_Is_Read.value = 1
        #Spec_Index_Process = Spec_Index_Process + 1
        print "spectrometer Index is %i" % Spec_Index_Process
        #print (Current_Spec_Record[0] - Time_Label)

    '''
    for I in range(No_Spec_Sample):
        #Time_Label = time.time()
        Current_Spec_Record[:] = Spec1.readIntensity(True, True)
        Spec_Is_Read.value = 1
        #print (Current_Spec_Record[0] - Time_Label)
    '''


# ######## A function for reading the DAQ analogue inpute on AINX ########
def DAQ_Read_Process(No_DAC_Sample,):
    while DAQ_Index[0] < No_DAC_Sample:
        #Time_Label = time.time()
        DAQ_Signal[DAQ_Index[0]], DAQ_Time[DAQ_Index[0]] = DAQ1.readPort('AIN1')
        #DAQ_Time[DAQ_Index[0]] = (time.time() )
        DAQ_Index[0] = DAQ_Index[0] + 1
    DAQ_Is_Read.value = 1

# ######## A function for reading the Power meter ########
def Power_Read_Process(No_Power_Sample):
    while Power_Index[0] < No_Power_Sample:
        #Time_Label = time.time()
        Power_Signal[Power_Index[0]], Power_Time[Power_Index[0]] = Power_meter.readPower()
        #Power_Time[Power_Index[0]] = (time.time() )
        Power_Index[0] = Power_Index[0] + 1
    Power_Is_Read.value = 1


if __name__ == "__main__":

    PhotoDiod_Port = "AIN1"
    #Spectrometer_Trigger_Port = "DAC0"

    Spec1 = SBO.open()
    Integration_Time = 2                                        # Integration time in ms
    Spec1.setTriggerMode(0)                                      # It is set for free running mode
    Spec1.setIntegrationTime(Integration_Time*1000)              # Integration time is in microseconds when using the library

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
    No_Power_Sample = int(round(No_DAC_Sample/3))
    No_Spec_Sample = int(round(No_DAC_Sample/(.4*Integration_Time)))

    Current_Spec_Record = Array('d', np.zeros(shape=( len(Spec1.Handle.wavelengths()) ,1), dtype = float ))
    #Spec_Index = Array('i', np.zeros(shape=( 1 ,1), dtype = int ))
    Full_Spec_Records = np.zeros(shape=(len(Spec1.Handle.wavelengths()), No_Spec_Sample ), dtype = float )
    Spec_Time   = Array('d', np.zeros(shape=( No_Spec_Sample ,1), dtype = float ))
    Spec_Index = 0
    Spec_Index2 = Array('i', np.zeros(shape=( 1 ,1), dtype = int ))

    DAQ_Signal = Array('d', np.zeros(shape=( No_DAC_Sample ,1), dtype = float ))
    DAQ_Time   = Array('d', np.zeros(shape=( No_DAC_Sample ,1), dtype = float ))
    DAQ_Index = Array('i', np.zeros(shape=( 1 ,1), dtype = int ))


    Power_Signal = Array('d', np.zeros(shape=( No_Power_Sample ,1), dtype = float ))
    Power_Time   = Array('d', np.zeros(shape=( No_Power_Sample ,1), dtype = float ))
    Power_Index = Array('i', np.zeros(shape=( 1 ,1), dtype = int ))

    # ########### The file containing the records (HDF5 format)###########'''


    Pros_DAQ = Process(target=DAQ_Read_Process, args=(No_DAC_Sample,))
    Pros_DAQ.start()
    Pros_Power = Process(target=Power_Read_Process, args=(No_Power_Sample,))
    Pros_Power.start()
    Pros_Spec = Process(target=Spec_Read_Process, args=(No_Spec_Sample,))
    Pros_Spec.start()


    while((Spec_Index < No_Spec_Sample)):
        if  Spec_Is_Read.value == 1:
            Spec_Is_Read.value = 0
            Full_Spec_Records[1:, Spec_Index] = Current_Spec_Record[1:]
            #Full_Spec_Records[0, Spec_Index] = (Current_Spec_Record[0])*1000000000000
            #Full_Spec_Records[0, Spec_Index] = time.time()
            #print ('time %f' % Full_Spec_Records[0, Spec_Index])
            #Spec_Time[Spec_Index] = Current_Spec_time
            Spec_Index = Spec_Index + 1
            #print ('dsds' , Spec_Index)
    print('Spectrometer is done')
    while True:
        if ((DAQ_Is_Read.value == 1) & (Power_Is_Read.value == 1)):
            break


    DAQ1.close()
    Spec1.close()

    # ######### Plotting the spectrumeter and the photodiod recordings ########
    plt.figure()

    #DAQ_Time = DAQ_Time[0:DAQ_Index] - DAQ_Time[0]
    #DAQ_Signal = DAQ_Signal[0:DAQ_Index]
    plt.subplot(1,3,1)
    #DAQ_Index = DAQ_Index = np.int32(DAQ_Index[0])
    #DAQ_Time = np.asarray((DAQ_Time[0:DAQ_Index]) - np.asarray(DAQ_Time[0]), dtype=np.float64)
    DAQ_Signal = np.asarray(DAQ_Signal[0:DAQ_Index[0]])
    plt.plot(DAQ_Time[0:DAQ_Index[0]], DAQ_Signal[0:DAQ_Index[0]], label = "Photo Diode")
    plt.title('Photo diode')
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (v)')

    plt.subplot(1,3,2)
    # Power_Index = DAQ_Index = np.int32(DAQ_Index[0])
    # Power_Time = np.asarray(Power_Time[0:Power_Index]) - np.asarray(Power_Time[0])
    Power_Signal = np.asarray(Power_Signal[0:Power_Index[0]])
    plt.plot(Power_Time[0:Power_Index[0]], Power_Signal[0:Power_Index[0]], label = "Power meter")
    plt.title('Power meter')
    plt.xlabel('Time (s)')
    plt.ylabel('Pwor (w)')

    plt.subplot(1,3,3)
    plt.plot(Spec1.readWavelength()[1:],Full_Spec_Records[1:]);
    plt.title('Specrometer recordings')
    plt.xlabel('Wavelength (nano meter)')
    plt.ylabel('Intensity')
    plt.show()

    ################################Closing the devices#############################

    plt.figure()
    plt.plot(DAQ_Time, (DAQ_Signal[0:DAQ_Index[0]]-np.mean(DAQ_Signal))/float( np.max(np.abs(DAQ_Signal))))
    plt.plot(Power_Time, (Power_Signal[0:Power_Index[0]]-np.mean(Power_Signal))/float( np.max(np.abs(Power_Signal))))
    plt.title("Normalized Power and DAQ signals")
    plt.xlabel("Unix time")
    plt.legend(['DAQ', 'P100'])
    plt.show()


    #################### Estimate the latencies of the devices ###################################
    plt.figure()

    DAQ_Latency = DAQ_Time[0:DAQ_Index[0]]
    DAQ_Latency[0] = 0
    for I in range(1,DAQ_Index[0]):
        DAQ_Latency[I] = DAQ_Time[I] - DAQ_Time[I-1]
    plt.subplot(1,3,1)
    plt.plot(DAQ_Latency)
    plt.ylabel("Time (s)")
    plt.title("DAQ latencies")

    Power_Latency = Power_Time[0:Power_Index[0]]
    Power_Latency[0] = 0
    for I in range(1,Power_Index[0]):
        Power_Latency[I] = Power_Time[I] - Power_Time[I-1]
    plt.subplot(1,3,2)
    plt.plot(Power_Latency)
    plt.title("P100 latencies")
    plt.ylabel("Time (s)")

    plt.subplot(1,3,3)
    Spec_Latency = Spec_Time[0:Spec_Index]
    Spec_Latency[0] = 0
    for I in range(1,Spec_Index):
        Spec_Latency[I] = Spec_Time[I] - Spec_Time[I-1]
    plt.plot(Spec_Latency)
    plt.ylabel("Time (s)")
    plt.title("Spectrometer integration durations")
    plt.show()
