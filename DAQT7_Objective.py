'''
Please refer to this website in for installation and prerequisites of the LabJack device python library:
https://labjack.com/support/software/examples/ljm/python
To use this class and its functions, folowing syntax is recommended:
import DAQT7_Objective as DAQ
Assuming that your device name is DeviceName then here are some sample commands:
DeviceName = DAQ.open()
This command puts 4.2 volts on DAC1 port (digital to analogue conversion): DeviceName.writePort('DAC1', 4.2)
This command reads the analogue values from AIN0 port (analogue to digital conversion): ReadVoltage = DeviceName.readPort('AIN0')
This command writes a digital value (3.3v) to a digital port (FIO0) port: DeviceName.writePort('FIO0', 1)
This command reads the digital value (zero or one) from a digital port (FIO0) port: State = DeviceName.readPort('FIO0'). State: 0 or 1
*The analogue ports are DACs and AINs. The DACs are read and writable. The AINs are only readable and they are only used for measuring an external voltages (0 to 10v) connected to the port. The FIOs are digital ports and their state are read and writable and they can have only 0 or 3.3 v values (equivalent to 0 and 1 digits).
To close the device: DeviceName.close()
print
In order to change the setup of the DAQT7, you need to access to the detailed attributes of the labjack library. The detailed attributes can be accessed:
DeviceName.Handle.Attribute, where the Attribute is one of the following:
eReadNames
eStreamRead
eStreamStart
eStreamStop
eWriteAddress
eWriteAddressArray
eWriteAddressString
eWriteAddresses
eWriteName
eWriteNameArray
eWriteNameString
eWriteNames
errorToString
errorcodes
float32ToByteArray
getHandleInfo
handle
int32ToByteArray
ipToNumber
listAll
listAllExtended
listAllS
ljm
loadConfigurationFile
loadConstants
loadConstantsFromFile
loadConstantsFromString
log
lookupConstantName
lookupConstantValue
macToNumber
mbfbComm
nameToAddress
namesToAddresses
numberToIP
numberToMAC
open
openAll
openS
readLibraryConfigS
readLibraryConfigStringS
readRaw
resetLog
streamBurst
sys
tcVoltsToTemp
uint16ToByteArray
uint32ToByteArray
updateValues
writeLibraryConfigS
writeLibraryConfigStringS
writeRaw

Changing the setup for Labjack device is described in the device manual.

@author: Yaqub Jonmohamadi
June 24, 2016
'''


from labjack import ljm
import time
import numpy as np

class open:
    '''
    Initialization and detection of the LabJack device
    '''
    def __init__(self):
        self.Handle = ljm
        self.Handle.handle = self.Handle.open(self.Handle.constants.dtANY, self.Handle.constants.ctANY, "ANY")
        info = self.Handle.getHandleInfo(self.Handle.handle)
        print("Opened a LabJack with Device type: %i, Connection type: %i,\n" \
        "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" % \
        (info[0], info[1], info[2], self.Handle.numberToIP(info[3]), info[4], info[5]))

        ''' Setup and call eWriteNames to configure AINs on the LabJack.'''
        numFrames = 3
        names = ["AIN_ALL_NEGATIVE_CH", "AIN_ALL_RANGE", "AIN_ALL_RESOLUTION_INDEX"]
        aValues = [199, 10, 1]
        self.Handle.eWriteNames(self.Handle.handle, numFrames, names, aValues)



    def getDetails(self):
        info = self.Handle.getHandleInfo(self.Handle.handle)

        return "Device type: %i, Connection type: %i,\n" \
            "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" % \
            (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5])


    def writePort(self, Port, Volt):      # DAC is one of the DAC ports (e.g., 'DAC0') and Volt is an integer from 0 to 5 volt (e.g., can be used for clossing or openning Shutter: 0=close, 5=open)
        '''
        Writing values to the ports
        * AIN ports are not writable
        '''
        self.Handle.eWriteName(self.Handle.handle, Port, Volt)
        return


    def readPort(self, Port):
        '''
        Reading analogue inpute values (0 to 10 v) in the AIN ports.
        To change the range of input voltage or speed of conversion, below lines should be changed in the initialization:
        numFrames = 3
        names = [")AIN0_NEGATIVE_CH"), ")AIN0_RANGE"), ")AIN0_RESOLUTION_INDEX")]
        aValues = [199, 2, 1]
        self.Handle.handle.eWriteNames(self.Handle.handle, numFrames, names, aValues)
        '''
        return np.float(self.Handle.eReadNames(self.Handle.handle,1 , [Port])[0]), time.time()



    def close(self):
        ''' Closing the device '''
        self.Handle.close(self.Handle.handle)
