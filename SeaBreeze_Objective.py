import time
import seabreeze.spectrometers as sb
import time

def help():
    print ("Please refer to this website in for installation and prerequisites of the OceanOptice spectrometers python library:")
    print ("https://github.com/ap--/python-seabreeze")
    print ("To use this class and its functions, following syntax is recommended:")
    print ("import SeaBreeze_Objective as SBO")
    print ("DeviceName = SBO.open()")
    print ("To see the help for this library use DeviceName.help()")
    print ("To clear the spectrometer use DeviceName.clear()")
    print ("To reset the spectrometer use DeviceName.reset()")
    print ("To close the spectrometer use DeviceName.close()")
    print ("To get the detailed information about connected spectrometer use DeviceName.readDetails()")
    print ("To read the intensities the recommended format is Intensities = DeviceName.readIntensity(True, True). The True values refer to Correct_dark_counts and Correct_nonlinearity")
    print ("The first element of Intensities (Intensities[0]) is the moment when the intensities are read (in unix time format)")
    print ("To read the wavelengthes the recommended format is Wavelengthes = DeviceName.readWavelenght()")


    print ("To chose an integration time use DeviceName.setIntegrationTime(IntegrationTime), where IntegrationTime is in microseconds and is from minimum integration time to maximum integration time")
    print ("To chose an integration time use DeviceName.setTriggerMode(TriggerValue), where TriggerValue is the TriggerValue is a value between 0 to 4 depending on the spectrometer. Read below information to chose a value for triggering:")
    print ("for HR2000+, USB2000+and Flame-S:")
    print ("Trigger Value = 0 ==> Normal (Free running) Mode")
    print ("Trigger Value = 1 ==> Software Trigger Mode")
    print ("Trigger Value = 2 ==> External Hardware Level Trigger Mode")
    print ("Trigger Value = 3 ==> External Synchronization Trigger Mode")
    print ("Trigger Value = 4 ==> External Hardware Edge Trigger Mode")
    print

    print ("for HR4000, USB4000 and Flame-T Set Trigger Mode")

    print ("Trigger Value = 0 ==> Normal (Free running) Mode")
    print ("Trigger Value = 1 ==> Software Trigger Mode")
    print ("Trigger Value = 2 ==> External Hardware Level Trigger Mode")
    print ("Trigger Value = 3 ==> Normal (Shutter) Mode")
    print ("Trigger Value = 4 ==> External Hardware Edge Trigger Mode")


    print ("for Maya2000Pro and Maya - LSL, QE65000, QE65 Pro, and QE Pro")

    print ("Trigger Value = 0 ==> Normal (Free running) Mode")
    print ("Trigger Value = 1 ==> External Hardware Level Trigger Mode")
    print ("Trigger Value = 2 ==> External Synchronous Trigger Mode*")
    print ("Trigger Value = 3 ==> External Hardware Edge Trigger Mode")
    print ("*Not yet implemented on the QE Pro")

    print ("For NIRQuest")

    print ("Trigger Value = 0 ==> Normal (Free running) Mode")
    print ("Trigger Value = 3 ==> External Hardware Edge Trigger Mode")

    print ("To access to all the callable attributes of the spectrometer use DeviceName.Handle.Attribute, where the Attribute could be one of the followings:")
    print ("close \n" \
    "continuous_strobe_set_enable\n" \
    "continuous_strobe_set_period_micros\n" \
    "eeprom_read_slot\n" \
    "from_serial_number\n" \
    "integration_time_micros\n" \
    "intensities\n" \
    "irrad_calibration\n" \
    "irrad_calibration_collection_area\n" \
    "lamp_set_enable\n" \
    "light_sources\n" \
    "minimum_integration_time_micros\n" \
    "model\n" \
    "pixels\n" \
    "serial_number\n" \
    "shutter_set_open\n" \
    "spectrum\n" \
    "stray_light_coeffs\n" \
    "tec_get_temperature_C\n" \
    "tec_set_enable\n" \
    "tec_set_temperature_C\n" \
    "trigger_mode\n" \
    "wavelengths\n")



''' ************** Detection of the OceanOptics spectrumeter **************** '''
class open:
    def __init__(self):
        if len(sb.list_devices()) == 0:
            print ("No spectrometer is detected!")
            return
        else:
            devices = sb.list_devices()
            self.Handle = sb.Spectrometer(devices[0])
            #spec = self.Handle
            print (devices)
            print ('Serial number:%s' % self.Handle.serial_number)
            print ('Model:%s' % self.Handle.model)
            print ('minimum_integration_time_micros: %s microseconds' % self.Handle.minimum_integration_time_micros)
        self.clear()


    def readDetails(self):
        attrs = vars(self.Handle)
        #for item in attrs.items():
        #    print item
        return attrs

    ''' This function resets the spectrometer. To make a hardware reset unplug it from the computer and then plug in again. '''
    def reset(self):
        devices = sb.list_devices()
        if len(sb.list_devices()) == 0:
            print ("No spectrometer is detected!")
            return
        else:
            self.Handle.close()
            #del self
            #del spec
            self.Handle = sb.Spectrometer(devices[0])
            #spec = self.Handle
        self.clear()


        ''' Setting the integration time (microseconds) '''
    def setIntegrationTime(self, Integration_time):
        self.Handle.integration_time_micros(Integration_time)
        time.sleep(0.01)


        ''' Setting the triggering mode (e.g., free running or external trigger) '''
    def setTriggerMode(self, Trigger_mode):
        self.Handle.trigger_mode(Trigger_mode)
        time.sleep(0.01)


        ''' Reading the intensities.
        Important! the first element in the Intensities array is the unix time for when the reading is finished.
        '''
    def readIntensity(self, Correct_dark_counts, Correct_nonlinearity):
        Intensities = self.Handle.intensities(correct_dark_counts=Correct_dark_counts, correct_nonlinearity=Correct_nonlinearity)
        #Intensities[0] = time.time()
        #Intensities[0] = int(round(time.time() * 1000))
        return Intensities, time.time()


        ''' Reading the wavelengthes of the spectrometer '''
    def readWavelength(self):
        return self.Handle.wavelengths()


    def clear(self):
        for I in range(3):
            self.Handle.trigger_mode(0)            #Flushing the stuff down and make the spectrometer ready for the next steps!
            time.sleep(0.01)
            self.Handle.integration_time_micros(10000)
            time.sleep(0.01)
            self.Handle.intensities(correct_dark_counts=True, correct_nonlinearity=True)
            time.sleep(0.01)


    ''' Closing the device '''
    def close(self):
        self.Handle.close()
