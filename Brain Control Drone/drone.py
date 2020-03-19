from pymultiwii import MultiWii
import time
import numpy as np
import math
from matplotlib import pyplot

init = 1.0
forward = 2.0
stop = 6.0
fly_up = 3.0
go_left = 5.0
go_right = 4.0

class PID:

    def __init__(self, KP, KI, KD):

        self.K = {'TS': 0, 'SAT': 0, 'KE': 0, 'KU': 0, 'KP': 0, 'KI': 0, 'KD': 0, 'KN': 0, 'B_0': 0, 'B_1': 0, 'C_1': 0,
                  'D_0': 0, 'D_1': 0}
        self.i_delay = [0, 0]
        self.d_delay = [0, 0]
        self.s_delay = 0
        self.s_flag = 0
        self.K['TS'] = 0.02
        self.K['SAT'] = 1.0
        self.K['KE'] = 1/20.0
        self.K['KU'] = 500
        self.K['KP'] = KP
        self.K['KI'] = KI
        self.K['KD'] = KD
        self.K['KN'] = 30.0
        self.PIDCoefCalc()
        self.PIDDelayInit()

    def PIDDelayInit(self):

        self.i_delay[0] = 0
        self.i_delay[1] = 0
        self.d_delay[0] = 0
        self.d_delay[1] = 0
        self.s_delay = 0.0

    def PIDCoefCalc(self):

        if self.K['KI'] is not 0:
            self.K['B_0'] = self.K['TS'] * self.K['KI'] * 0.5
            self.K['B_1'] = self.K['B_0']
        else:
            self.K['B_0'] = self.K['B_1'] = 0

        if self.K['KP'] != 0 or self.K['KD'] != 0:
            self.K['C_1'] = -((self.K['TS'] * self.K['KN'] - 2.0) / (self.K['TS'] * self. K['KN'] + 2.0))
            self.K['D_0'] = (self.K['KP'] + ((2.0 * self.K['KD'] * self.K['KN']) / (self.K['KN'] * self.K['TS'] + 2.0)))
            self.K['D_1'] = ((((self.K['KN'] * self.K['TS'] - 2.0) * self.K['KP']) - (2.0 * self.K['KD'] * self.K['KN'])) / (self.K['KN'] * self.K['TS']+2.0))
        else:
            self.K['C_1'] = self.K['D_0'] = self.K['D_1'] = 0.0

    def PIDisSaturated(self):

        return not self.s_flag   #1 not saturated 0 saturated

    def calcPID(self, error_in):

        input_buffer = error_in
        f_error = input_buffer * self.K['KE']

        self.s_delay = 0

        if self.K['KI'] is not 0:
            if self.s_flag:
                self.i_delay[1] = f_error + self.i_delay[0]
            else:
                self.i_delay[1] = self.i_delay[0]
            self.s_delay = self.s_delay + (self.K['B_0'] * self.i_delay[1]) + (self.K['B_1'] * self.i_delay[0])
            self.i_delay[0] = self.i_delay[1]

        if self.K['KP'] is not 0 or self.K['KI'] is not 0:
            self.d_delay[1] = f_error + self.K['C_1'] * self.d_delay[0]
            self.s_delay = self.s_delay + self.K['D_0'] * self.d_delay[1] + self.K['D_1'] * self.d_delay[0]
            self.d_delay[0] = self.d_delay[1]

        output_buffer = self.s_delay
        if output_buffer > self.K['SAT']:
            output = self.K['SAT'] * self.K['KU']
            self.s_flag = 0

        elif output_buffer < -(self.K['SAT']):
            output = -(self.K['SAT'] * self.K['KU'])
            self.s_flag = 0

        else:
            output = output_buffer * self.K['KU']
            self.s_flag = 1

        return output


drone = MultiWii()
input("press any key to continue")
try:
    f = open("decision.txt", mode='w')
    f.write(str(init+0.1))
    print("detected")
except Exception as e:
    print(e)
finally:
    f.close()

try:
    drone.open("/dev/rfcomm0")
    time.sleep(2)
    drone.arm()
    time.sleep(0.5)
    drone.sendCMD(8, MultiWii.SET_RAW_RC, [1500, 1500, 1500, 1000], '4h')
    print("arm")
except Exception as error:
    print(error)

# pyplot.ion()
# fig = pyplot.figure()
# imu_fig = fig.add_subplot(121)
# pyplot.xticks([1, 2],  ['roll', 'pitch'])
# rect1 = imu_fig.bar([1, 2], [-90, 90])
#
# imu_fig = fig.add_subplot(122)
# pyplot.xticks([1, 2, 3, 4],  ['roll', 'pitch', 'yaw', 'throttle'])
# rect2 = imu_fig.bar([1, 2, 3, 4], [1000, 2000, 1000, 1000])

start = time.time()
data = [1500, 1500, 1500, 1000]
fly_up_f = 0
roll = 0
pitch = 0
start_imu = time.time()
roll_pid = PID(2.0, 0.0, 0.4)
pitch_pid = PID(2.0, 0.0, 0.4)
out1 = 0
out2 = 0
landing = 0
start_countdown = time.time()

while True:
    try:

        # try:
        #     drone.getData(MultiWii.RAW_IMU)
        # except Exception as error:
        #     pass

        drone.rawIMU['gx'] = drone.rawIMU['gx'] / 65.5
        drone.rawIMU['gy'] = drone.rawIMU['gy'] / 65.5
        drone.rawIMU['gz'] = drone.rawIMU['gz'] / 65.5

        drone.rawIMU['ax'] = drone.rawIMU['ax'] / 4096.0
        drone.rawIMU['ay'] = drone.rawIMU['ay'] / 4096.0
        drone.rawIMU['az'] = drone.rawIMU['az'] / 4096.0

        roll_angle = math.atan2(-drone.rawIMU['ay'], drone.rawIMU['az']) * 180 / math.pi
        pitch_angle = math.atan2(drone.rawIMU['ax'], math.sqrt(drone.rawIMU['ay'] * drone.rawIMU['ay']
                                                               + drone.rawIMU['az'] * drone.rawIMU[
                                                                   'az'])) * 180 / math.pi
        dt = float(time.time()) - start_imu
        roll = 0.98 * (roll + drone.rawIMU['gx'] * dt) + 0.02 * roll_angle
        pitch = 0.98 * (pitch + drone.rawIMU['gy'] * dt) + 0.02 * pitch_angle

        start_imu = time.time()

        if (time.time() - start) > 0.02:

            # if roll-0 > 3.0 or roll-0 < -3.0:
            #     roll_error = roll - 0
            # else:
            #     roll_error = 0
            #     roll_pid.PIDDelayInit()
            #
            # if pitch-0 > 3.0 or pitch-0 < -3.0:
            #     pitch_error = pitch - 0
            # else:
            #     pitch_error = 0
            #     pitch_pid.PIDDelayInit()

            roll_out = roll_pid.calcPID(roll-0)
            pitch_out = pitch_pid.calcPID(pitch-0)

            # roll_out = 0
            # pitch_out = 0

            buf = [roll, pitch]
            buf2 = [roll_out, pitch_out]

            # for rect, h in zip(rect1, buf):
            #
            #     rect.set_height(h)
            #
            # for rect, h in zip(rect2, data):
            #
            #     rect.set_height(h)
            #
            # pyplot.draw()
            # pyplot.pause(0.0001)
            try:
                decision = np.loadtxt("decision.txt")
            except Exception as error:
                print(error)
            if decision > fly_up and fly_up_f is 0:
                data = [1500, 1500, 1500, 1800]
                fly_up_f = 1
                if landing is 0:
                    throttle = 1645+25
                elif landing is 1:
                    throttle = 1685+25
                elif landing is 2:
                    throttle = 1670+25
                print("fly_up")

            if fly_up_f > 0:
                if decision > stop:
                    if throttle > 1100:
                        print("stop")
                        if landing is 0:
                            throttle -= 4
                        elif landing is 1:
                            throttle -= 4
                        else:
                            throttle -= 4
                        # print("slowing down")
                        data = [1560, 1522, 1500, int(throttle)]
                    else:
                        fly_up_f = 0
                        landing += 1
                        data = [1500, 1522, 1500, 1000]
                        try:
                            f = open("decision.txt", mode='w')
                            f.write(str(init + 0.1))
                            print("detected")
                        except Exception as e:
                            print(e)
                        finally:
                            f.close()

                elif decision > go_left:
                    # if 1300 + roll_out < 1000:
                    #     final = 1000
                    # else:
                    #     final = int(1200 + roll_out)

                    data = [1650, 1550, 1500, 1820]
                    print("go_left")

                elif decision > go_right:
                    data = [1350, 1525, 1500, 1840]
                    print("go_right")

                else:
                    data = [int(1500 - pitch_out), int(1505 + roll_out), 1500, 1800]  #roll pitch yaw throttle
                    print("fly_up")

            try:
                drone.sendCMD(8, MultiWii.SET_RAW_RC, data, '4h')
            except Exception as error:
                print(error)
                pass

            start = time.time()

    except KeyboardInterrupt as error:
        drone.disarm()
        time.sleep(0.5)
        while True:
            pass