import time, struct, serial #pyserial library
from pymultiwii import MultiWii
import array as arr
import numpy as np
from matplotlib import pyplot
from scipy import signal
from scipy import integrate
from mne.time_frequency import psd_array_multitaper
from scipy.signal import butter, lfilter
import threading

class uart:

    def __init__(self, serport):

        self.ser = serial.Serial()
        self.ser.port = serport
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.baudrate = 115200
        self.ser.timeout = 0
        self.write = False
        self.info = []
        self.ii = 0
        self.plot = False
        self.initialize = False
        self.plot_time = 0

        self.ch1 = arr.array('h')
        self.ch2 = arr.array('h')

        self.ch1load = []

        self.data = {'CH1': 0, 'CH2': 0, 'CH3': 0, 'CH4': 0, 'CH5': 0, 'CH6': 0}
        self.packet_count = 0

        try:
            self.ser.open()
        except Exception as error:
            print(error)

    def get_data(self, pri=False):

        aa = 0
        try:
            if self.ser.in_waiting:
                header = struct.unpack('B', self.ser.read())
                if header[0] == 0xa5:
                    header2 = struct.unpack('B', self.ser.read())
                    if header2[0] == 0x5a:
                        aa = 1
                        temp = self.ser.read(2)
                        self.info = struct.unpack('2B', temp)
                        temp2 = self.ser.read(12)
                        data = struct.unpack('>6h', temp2)  # MSB first
                        self.data['CH1'] = data[0]
                        self.data['CH2'] = data[1]
                        self.data['CH3'] = data[2]
                        self.data['CH4'] = data[3]
                        self.data['CH5'] = data[4]
                        self.data['CH6'] = data[5]

                        self.ch1.append(self.data['CH1'])
                        self.ch2.append(self.data['CH2'])

                        print(self.info[1])

                        self.ser.flushInput()
                        self.ser.flushOutput()

                        if pri:
                            print('CH1 = {} CH2 = {}'.format(self.data['CH1'], self.data['CH2']))

                        if self.info[1] == 0xFF or self.info[1] == 127 or self.info[1] == 63 or self.info[1] == 191:
                            if self.initialize:
                                self.write = True
                                self.plot = True
                                self.write_file(self.ch1, "data.txt")
                                self.write_file(self.ch2, "data2.txt")
                                del self.ch1
                                del self.ch2
                                self.ch1 = arr.array('h')
                                self.ch2 = arr.array('h')
                            else:
                                self.initialize = True

                    else:
                        pass
                else:
                    pass
            else:
                pass
        except Exception as error:
            if aa:
                print(error)

    def write_file(self, data, filename):

        try:
            f = open(filename, mode="w")
            for i in range(0, 255):
                f.write(str(data[i]))
                f.write('\n')
        except Exception as e:
            print(e)
        finally:
            f.close()

if __name__ == '__main__':

    app = uart("/dev/ttyUSB0")
    # app.load_data()
    # app.plot_data()
    while True:
        app.get_data(False)

        pass