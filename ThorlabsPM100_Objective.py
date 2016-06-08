from ThorlabsPM100 import ThorlabsPM100, USBTMC
import os


def help():
    print ("Please refer to this website in for installation and prerequisites of the Thorlabs PM100 power meter python library:")
    print ("https://pypi.python.org/pypi/ThorlabsPM100")
    print ("To use this class and its functions, folowing syntax is recommended:")
    print ("import ThorlabsPM100 as P100")
    print ("To see the help for this library use P100.help()")
    print ("Assuming that your device name is DeviceName then here are some sample commands:")
    print ("DeviceName = P100.open()")
    print ("To read power Power = DevieceName.readPower()")

    print ("To close the device: DeviceName.close()")

    print ("In order to change the setup of the power meter, you need to access to its attributes. The detailed attributes can be accessed:")
    print ("DeviceName.Attribute, where the Attribute is one of the following:")
    print ( "	DeviceName.abort  \n" \
            "   DeviceName.getconfigure  \n" \
            "   DeviceName.sense  \n" \
            "   DeviceName.calibration  \n" \
            "   DeviceName.initiate      \n" \
            "   DeviceName.status    \n" \
            "   DeviceName.configure     \n" \
            "   DeviceName.input         \n" \
            "   DeviceName.system \n" \
            "   DeviceName.display \n" \
            "   DeviceName.measure \n" \
            "   DeviceName.fetch \n" \
            "   DeviceName.read  \n" )
    print (" Each of the attributes can have their own attributes, example to change the brightness of the dispace use DeviceName.display.brightness = 0.8 ")


class open:
    '''
    Initialization and detection of the Thorlab device
    '''
    def __init__(self):
        # Open first found LabJack
        try:
            USBTMC(device="/dev/usbtmc0")
            inst = USBTMC(device="/dev/usbtmc0")
            self.Handle = ThorlabsPM100(inst=inst)
        except OSError, er0:
            print ('er0:%s' % er0)
            if er0.errno == 13:				#Permission denied: '/dev/usbtmc0'
                os.system('sudo chmod 777 /dev/usbtmc0')
                inst = USBTMC(device="/dev/usbtmc0")
                self.Handle = ThorlabsPM100(inst=inst)
            elif er0.errno == 2:			#No such a [Errno 2] No such file or directory: '/dev/usbtmc0'
                try:
                    USBTMC(device="/dev/usbtmc1")
                    inst = USBTMC(device="/dev/usbtmc1")
                    self.Handle = ThorlabsPM100(inst=inst)
                except OSError, er1:
                    print ('er1:%s' % er1)
                    if er1.errno == 13:		#Permission denied: '/dev/usbtmc1'
                        os.system('sudo chmod 777 /dev/usbtmc1')
                        inst = USBTMC(device="/dev/usbtmc1")
                        self.Handle = ThorlabsPM100(inst=inst)
                    elif er1.errno == 2:	#No such a [Errno 2] No such file or directory: '/dev/usbtmc1'
                        try:
                            USBTMC(device="/dev/usbtmc2")
                            inst = USBTMC(device="/dev/usbtmc2")
                            self.Handle = ThorlabsPM100(inst=inst)
                        except OSError, er2:
                            print ('er2:%s' % er2)
                            if er2.errno == 13:		#Permission denied: '/dev/usbtmc2'
                                os.system('sudo chmod 777 /dev/usbtmc2')
                                inst = USBTMC(device="/dev/usbtmc2")
                                self.Handle = ThorlabsPM100(inst=inst)
                            elif er2.errno == 2:	#No such a [Errno 2] No such file or directory: '/dev/usbtmc2'
                                print ("Power meter is not connected!")
                                return

            '''
            def assignPort(self, Port):
                print ('here')
                inst = USBTMC(device=Port)
                self.Handle = ThorlabsPM100(inst=inst)
                self.Handle.system.beeper.immediate()
            '''
        #print(dir(self))
        print ("A Thorlabs PM100 device is opened.")

    # This function returns the analogue value recorde on one of the AIN ports (e.g., 'AIN0')

    def readPower(self):
        return self.Handle.read

