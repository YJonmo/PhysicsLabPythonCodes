

from labjack import ljm
import time

def help(self):
    print ("Please refer to this website in for installation and prerequisites of the LabJack device python library:")
    print ("https://labjack.com/support/software/examples/ljm/python")
    print ("To use this class and its functions, folowing syntax is recommended:")
    print ("import DAQT7_Objective as DAQ")
    print ("To see the help for this library use DAQ.help()")
    print ("Assuming that your device name is DeviceName then here are some sample commands:")
    print ("DeviceName = DAQ.open()")
    print ("This command puts 4.2 volts on DAC1 port (digital to analogue conversion): DeviceName.Port_Write('DAC1', 4.2)")
    print ("This command reads the analogue values from AIN0 port (analogue to digital conversion): ReadVoltage = DeviceName.Port_Read('AIN0')")
    print ("This command writes a digital value (3.3v) to a digital port (FIO0) port: DeviceName.Port_Write('FIO0', 1)")
    print ("This command reads the digital value (zero or one) from a digital port (FIO0) port: State = DeviceName.Port_Read('FIO0'). State: 0 or 1 ")
    print ("*The analogue ports are DACs and AINs. The DACs are read and writable. The AINs are only readable and they are only used for measuring an external voltages (0 to 10v) connected to the port. The FIOs are digital ports and their state are read and writable and they can have only 0 or 3.3 v values (equivalent to 0 and 1 digits).")
    #print ("To change the range of input voltage or speed of conversion for AINs, following attributes should be changed in the intialization:")
    #print ("numFrames = 3")
    #print ("names = [\")AIN0_NEGATIVE_CH\"), \")AIN0_RANGE\"), \")AIN0_RESOLUTION_INDEX\")]")
    #print ("aValues = [199, 2, 1]")
    #print ("self.Handle.eWriteNames(self.Handle.handle, numFrames, names, aValues)")

    print ("To close the device: DeviceName.close()")
    print
    print ("In order to change the setup of the DAQT7, you need to access to the detailed attributes of the labjack library. The detailed attributes can be accessed:")
    print ("DeviceName.Handle.Attribute, where the Attribute is one of the following:")
    print ( "	eReadNames		\n" \
            "	eStreamRead		\n" \
            "	eStreamStart		\n" \
            "	eStreamStop		\n" \
            "	eWriteAddress		\n" \
            "	eWriteAddressArray		\n" \
            "	eWriteAddressString		\n" \
            "	eWriteAddresses		\n" \
            "	eWriteName		\n" \
            "	eWriteNameArray		\n" \
            "	eWriteNameString		\n" \
            "	eWriteNames		\n" \
            "	errorToString		\n" \
            "	errorcodes		\n" \
            "	float32ToByteArray		\n" \
            "	getHandleInfo		\n" \
            "	handle		\n" \
            "	int32ToByteArray		\n" \
            "	ipToNumber		\n" \
            "	listAll		\n" \
            "	listAllExtended		\n" \
            "	listAllS		\n" \
            "	ljm		\n" \
            "	loadConfigurationFile		\n" \
            "	loadConstants		\n" \
            "	loadConstantsFromFile		\n" \
            "	loadConstantsFromString		\n" \
            "	\log		\n" \
            "	lookupConstantName		\n" \
            "	lookupConstantValue		\n" \
            "	macToNumber		\n" \
            "	mbfbComm		\n" \
            "	nameToAddress		\n" \
            "	namesToAddresses		\n" \
            "	numberToIP		\n" \
            "	numberToMAC		\n" \
            "	\open		\n" \
            "	openAll		\n" \
            "	openS		\n" \
            "	readLibraryConfigS		\n" \
            "	readLibraryConfigStringS		\n" \
            "	readRaw		\n" \
            "	resetLog		\n" \
            "	streamBurst		\n" \
            "	sys		\n" \
            "	tcVoltsToTemp		\n" \
            "	uint16ToByteArray		\n" \
            "	uint32ToByteArray		\n" \
            "	updateValues		\n" \
            "	writeLibraryConfigS		\n" \
            "	writeLibraryConfigStringS		\n" \
            "	writeRaw		\n" )


    '''
    #attrs = dir(self.Handle.handle)
    dirr = dir(self.Handle)
    for item in dirr:
        print (item)
    '''

    print ("Changing the setup for Labjack device is available in the device manual.")
    #attrs =  [attr for attr in dir(self.Handle.handle) if not  attr.startswith('_')]
    #for I in range(len(attrs)):
    #print (dir(self.Handle.handle))


class open:
    '''
    Initialization and detection of the LabJack device
    '''
    def __init__(self):
        # Open first found LabJack
        self.Handle = ljm
        self.Handle.handle = self.Handle.open(self.Handle.constants.dtANY, self.Handle.constants.ctANY, "ANY")
        #self.handle = self.Handle.openS("ANY", "ANY", "ANY")
        info = self.Handle.getHandleInfo(self.Handle.handle)
        print("Opened a LabJack with Device type: %i, Connection type: %i,\n" \
        "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" % \
        (info[0], info[1], info[2], self.Handle.numberToIP(info[3]), info[4], info[5]))

        ''' Setup and call eWriteNames to configure AINs on the LabJack.'''
        numFrames = 3
        names = ["AIN0_NEGATIVE_CH", "AIN0_RANGE", "AIN0_RESOLUTION_INDEX"]
        aValues = [199, 2, 1]
        self.Handle.eWriteNames(self.Handle.handle, numFrames, names, aValues)
        #return self.handle, Info



    def getDetails(self):
        info = self.Handle.getHandleInfo(self.Handle.handle)

        return "Device type: %i, Connection type: %i,\n" \
            "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" % \
            (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5])

    '''
    Writing values to the ports
    * AIN ports are not writable
    '''
    def portWrite(self, Port, Volt):      # DAC is one of the DAC ports (e.g., 'DAC0') and Volt is an integer from 0 to 5 volt (e.g., can be used for clossing or openning Shutter: 0=close, 5=open)

        self.Handle.eWriteName(self.Handle.handle, Port, Volt)
        return


    '''
    Reading analogue inpute values (0 to 10 v) in the AIN ports.
    To change the range of input voltage or speed of conversion, below lines should be changed in the initialization:
    numFrames = 3
    names = [")AIN0_NEGATIVE_CH"), ")AIN0_RANGE"), ")AIN0_RESOLUTION_INDEX")]
    aValues = [199, 2, 1]
    self.Handle.handle.eWriteNames(self.Handle.handle, numFrames, names, aValues)
    '''
    # This function returns the analogue value recorde on one of the AIN ports (e.g., 'AIN0') and the unix time when the value is read
    def portRead(self, Port):
        return self.Handle.eReadNames(self.Handle.handle,1 , [Port])[0]


    '''
    Closing the device
    '''
    def close(self):
        self.Handle.close(self.Handle.handle)

