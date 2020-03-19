import time, struct, serial #pyserial library
from pymultiwii import MultiWii
import array as arr
import numpy as np
from matplotlib import pyplot
from scipy import signal
from scipy import integrate
from mne.time_frequency import psd_array_multitaper
from scipy.signal import butter, lfilter, find_peaks
from skfuzzy import control as ctrl
import skfuzzy as fuzz

init = 1.0
forward = 2.0
stop = 6.0
fly_up = 3.0
go_left = 5.0
go_right = 4.0


class filter:

    def __init__(self):

        self.sf = 255
        self.write_decision(init)
        self.stop_f = 0

        self.eeg_bands = {'Delta': (2, 4), 'Theta': (4, 8), 'Alpha': (8, 12), 'Beta': (12, 30), 'Gamma': (30, 45)}
        self.band_name = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']

        # self.eeg_bands = {'Delta': (4,6), 'Theta': (6, 8), 'Alpha': (8, 10), 'Beta': (10, 12), 'Gamma': (12, 14)}
        # self.band_name = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']

        self.ch1_bandpower = [0.1, 0.1, 0.1, 0.1, 1.0]
        self.ch2_bandpower = [0.1, 0.1, 0.1, 0.1, 1.0]

        self.ch1_bandamp = [1000, 2000, 2000, 2000, 4000]
        self.ch2_bandamp = [1000, 2000, 2000, 2000, 4000]
        self.fft_vals = np.array([])
        self.fft_freq = np.array([])

        self.ch1_power_x = np.arange(len(self.band_name))
        self.ch2_power_x = np.arange(len(self.band_name))

        self.ch1_plot = np.array([])
        self.ch1_x_ax = np.array([])
        self.ch2_plot = np.array([])
        self.ch2_x_ax = np.array([])
        self.ch1_detrend = np.array([])
        self.ch2_detrend = np.array([])
        self.ch1_filt = np.array([])
        self.ch2_filt = np.array([])

        self.ch1_plot_delta = np.array([])
        self.ch1_plot_theta = np.array([])
        self.ch1_plot_alpha = np.array([])
        self.ch1_plot_beta = np.array([])
        self.ch1_plot_gamma = np.array([])

        self.ch2_plot_delta = np.array([])
        self.ch2_plot_theta = np.array([])
        self.ch2_plot_alpha = np.array([])
        self.ch2_plot_beta = np.array([])
        self.ch2_plot_gamma = np.array([])

        self.ch1_beta_peak = np.array([])
        self.ch1_beta_peak_x = np.array([])

        self.ch2_beta_peak = np.array([])
        self.ch2_beta_peak_x = np.array([])

        self.ch1_theta_peak = np.array([])
        self.ch1_theta_peak_x = np.array([])

        self.ch2_theta_peak = np.array([])
        self.ch2_theta_peak_x = np.array([])

        self.plot_time = 0

        self.ch1_beta_count = 0
        self.ch2_beta_count = 0

        self.ch1_theta_count = 0
        self.ch2_theta_count = 0

        self.forward_f = 0
        self.forward_f2 = 0

        self.stop_f = 0
        self.stop_f2 = 0

        self.c1_theta = ctrl.Antecedent(np.arange(0, 7, 1), 'ch1_theta')
        self.c2_theta = ctrl.Antecedent(np.arange(0, 7, 1), 'ch2_theta')
        self.c1_beta = ctrl.Antecedent(np.arange(0, 10, 1), 'ch1_beta')
        self.c2_beta = ctrl.Antecedent(np.arange(0, 10, 1), 'ch2_beta')
        self.result1 = ctrl.Consequent(np.arange(0, 1, 0.1), 'blink_one_eye')
        self.result2 = ctrl.Consequent(np.arange(0, 1, 0.1), 'blink_two_eye')
        self.result3 = ctrl.Consequent(np.arange(0, 1, 0.1), 'raise_eyebrow')
        self.result4 = ctrl.Consequent(np.arange(0, 1, 0.1), 'look left')

        # self.c1_theta.automf(3)
        # self.c2_theta.automf(3)
        # self.c1_beta.automf(3)
        # self.c2_beta.automf(3)

        self.c1_theta['poor'] = fuzz.trimf(self.c1_theta.universe, [0, 0, 3])
        self.c1_theta['average'] = fuzz.trimf(self.c1_theta.universe, [0, 3, 5])
        self.c1_theta['good'] = fuzz.trimf(self.c1_theta.universe, [3, 7, 7])

        self.c2_theta['poor'] = fuzz.trimf(self.c2_theta.universe, [0, 0, 3])
        self.c2_theta['average'] = fuzz.trimf(self.c2_theta.universe, [0, 3, 5])
        self.c2_theta['good'] = fuzz.trimf(self.c2_theta.universe, [3, 7, 7])

        self.c1_beta['poor'] = fuzz.trimf(self.c1_beta.universe, [0, 0, 3])
        self.c1_beta['average'] = fuzz.trimf(self.c1_beta.universe, [0, 3, 8])
        self.c1_beta['good'] = fuzz.trimf(self.c1_beta.universe, [8, 10, 10])

        self.c2_beta['poor'] = fuzz.trimf(self.c2_beta.universe, [0, 0, 3])
        self.c2_beta['average'] = fuzz.trimf(self.c2_beta.universe, [0, 3, 8])
        self.c2_beta['good'] = fuzz.trimf(self.c2_beta.universe, [8, 10, 10])

        self.result1.automf(3)
        self.result2.automf(3)
        self.result3.automf(3)
        self.result4.automf(3)

        self.rule1 = ctrl.Rule((self.c2_beta['good'] | self.c2_theta['good']) & self.c1_theta['poor'] & self.c1_beta['poor'], self.result1['good'])
        self.rule2 = ctrl.Rule(self.c2_beta['poor'] | self.c2_theta['poor'], self.result1['poor'])
        self.rule3 = ctrl.Rule(self.c2_beta['average'] & self.c2_theta['average'], self.result1['poor'])
        self.rule4 = ctrl.Rule((self.c2_beta['good'] | self.c2_theta['good']) & self.c1_theta['good'], self.result1['poor'])

        self.rule5 = ctrl.Rule((self.c1_theta['good'] | self.c2_theta['good']), self.result2['good'])
        self.rule6 = ctrl.Rule(self.c1_theta['poor'] | self.c2_theta['poor'], self.result2['poor'])
        self.rule7 = ctrl.Rule(self.c1_theta['average'] | self.c2_theta['average'], self.result2['average'])
        self.rule8 = ctrl.Rule(self.c1_theta['average'] & self.c2_theta['average'], self.result2['good'])

        self.rule9 = ctrl.Rule((self.c2_beta['average'] & self.c1_beta['average']), self.result3['good'])
        self.rule10 = ctrl.Rule(self.c2_beta['average'] | self.c1_beta['average'], self.result3['average'])
        self.rule11 = ctrl.Rule((self.c2_beta['good'] | self.c1_beta['good']), self.result3['good'])
        self.rule12 = ctrl.Rule(self.c2_beta['poor'] | self.c1_beta['poor'], self.result3['poor'])

        self.rule13 = ctrl.Rule(self.c1_theta['average'] & self.c2_theta['average'], self.result4['good'])
        self.rule14 = ctrl.Rule(self.c1_theta['good'] | self.c2_theta['good'], self.result4['poor'])
        self.rule15 = ctrl.Rule(self.c1_theta['poor'] & self.c2_theta['poor'], self.result4['poor'])

        # self.rule13 = ctrl.Rule((self.c2_beta['good'] | self.c1_beta['good']), self.result3['average'])

        # self.rule5 = ctrl.Rule(self.c1_beta['good'] & self.c2_beta['good'] & self.c1_theta['poor'] & self.c2_theta['poor'], self.result3['good'])
        # self.rule6 = ctrl.Rule(self.c1_beta['poor'] & self.c2_beta['poor'], self.result2['poor'])
        # self.rule7 = ctrl.Rule(self.c1_beta['poor'] & self.c2_beta['poor'] & self.c1_theta['poor'] & self.c2_theta['poor'], self.result3['good'])

        self.drone_control = ctrl.ControlSystem([self.rule1, self.rule2, self.rule3, self.rule4, self.rule5, self.rule6,
                                                 self.rule7, self.rule8, self.rule9, self.rule10, self.rule11, self.rule12,
                                                 self.rule13, self.rule14, self.rule15])
        self.drone = ctrl.ControlSystemSimulation(self.drone_control)

        pyplot.ion()
        self.fig = pyplot.figure()

        self.ch1_fig = self.fig.add_subplot(221)
        self.ch1_beta_peak_line, = self.ch1_fig.plot(self.ch1_beta_peak_x, self.ch1_beta_peak, c='r', marker='x')
        self.ch1_theta_peak_line, = self.ch1_fig.plot(self.ch1_theta_peak_x, self.ch2_theta_peak, c='r', marker='o')
        # self.ch1_line, = self.ch1_fig.plot(self.ch1_x'_ax, self.ch1_plot)
        # self.ch1_delta_line, = self.ch1_fig.plot(self.ch1_x_ax, self.ch1_plot_delta, color="red")
        self.ch1_theta_line, = self.ch1_fig.plot(self.ch1_x_ax, self.ch1_plot_theta, color='green')
        self.ch1_alpha_line, = self.ch1_fig.plot(self.ch1_x_ax, self.ch1_plot_alpha, color='yellow')
        self.ch1_beta_line, = self.ch1_fig.plot(self.ch1_x_ax, self.ch1_plot_beta, color='purple')
        self.ch1_gamma_line, = self.ch1_fig.plot(self.ch1_x_ax, self.ch1_plot_gamma, color='orange')
        pyplot.title("CH1 Raw Data")
        pyplot.legend(['beta_p', 'theta_p', 'theta', 'alpha', 'beta', 'gamma'], loc='upper left')

        self.ch2_fig = self.fig.add_subplot(222)
        self.ch2_beta_peak_line, = self.ch2_fig.plot(self.ch2_x_ax, self.ch2_beta_peak, c='r', marker='x')
        self.ch2_theta_peak_line, = self.ch2_fig.plot(self.ch2_x_ax, self.ch2_theta_peak, c='r', marker='o')
        # self.ch2_line, = self.ch2_fig.plot(self.ch2_x_ax, self.ch2_plot)
        self.ch2_theta_line, = self.ch2_fig.plot(self.ch2_x_ax, self.ch2_plot_theta, color='green')
        self.ch2_alpha_line, = self.ch2_fig.plot(self.ch2_x_ax, self.ch2_plot_alpha, color='yellow')
        self.ch2_beta_line, = self.ch2_fig.plot(self.ch2_x_ax, self.ch2_plot_beta, color='purple')
        self.ch2_gamma_line, = self.ch2_fig.plot(self.ch2_x_ax, self.ch2_plot_gamma, color='orange')
        pyplot.legend(['beta_p', 'theta_p', 'theta', 'alpha', 'beta', 'gamma'], loc='upper left')
        pyplot.title("CH2 Raw Data")

        # self.ch1_d_fig = self.fig.add_subplot(323)
        # pyplot.title("CH1 Power Spectral")
        # self.ch2_d_fig = self.fig.add_subplot(324)
        # pyplot.title("CH2 Power Spectral")

        self.ch1_bar_fig = self.fig.add_subplot(223)
        pyplot.title("CH1 BandPower")
        pyplot.xticks(self.ch1_power_x, self.band_name)

        # self.ch2_bar_fig = self.fig.add_subplot(224)
        # pyplot.title("CH2 BandPower")
        # pyplot.xticks(self.ch1_power_x, self.band_name)
        #
        # self.ch1_bar2_fig = self.fig.add_subplot(425)
        # pyplot.title("CH1 BandAmplitude")
        # pyplot.xticks(self.ch1_power_x, self.band_name)
        #
        # self.ch2_bar2_fig = self.fig.add_subplot(426)
        # pyplot.title("CH2 BandAmplitude")
        # pyplot.xticks(self.ch1_power_x, self.band_name)

        # self.ch1_d_line, = self.ch1_d_fig.plot(self.ch1_x_ax, self.ch1_detrend)
        # self.ch2_d_line, = self.ch2_d_fig.plot(self.ch2_x_ax, self.ch2_detrend)
        #
        self.ch1_rect = self.ch1_bar_fig.bar(self.ch1_power_x, self.ch1_bandpower)
        # self.ch2_rect = self.ch2_bar_fig.bar(self.ch2_power_x, self.ch2_bandpower)
        #
        # self.ch1_rect2 = self.ch1_bar2_fig.bar(self.ch1_power_x, self.ch1_bandamp)
        # self.ch2_rect2 = self.ch2_bar2_fig.bar(self.ch2_power_x, self.ch2_bandamp)


        pyplot.show()


    def receive_data(self):

        ch1 = self.load_data("data.txt")
        ch2 = self.load_data("data2.txt")

        self.plot_time += 0.25
        self.ch1_plot = np.append(self.ch1_plot, ch1)
        self.ch2_plot = np.append(self.ch2_plot, ch2)

        if len(self.ch1_plot) > 1281:
            self.ch1_plot = self.ch1_plot[-1281:]
        if len(self.ch2_plot) > 1281:
            self.ch2_plot = self.ch2_plot[-1281:]

        # self.ch1_plot = self.detrend(self.ch1_plot)
        # self.ch2_plot = self.detrend(self.ch2_plot)

        # freq, psd = self.multitaper_diagram(self.ch1_plot, "CH1", plot=True)
        #
        # i = 0
        # for band in self.eeg_bands:
        #
        #     self.ch1_bandpower[i] = self.bandpower(freq, psd, self.eeg_bands[band][0], self.eeg_bands[band][1])
        #
        #     if i is 0:
        #         self.ch1_bandamp[i] = self.band_amplitude(self.ch1_plot, self.eeg_bands[band][0], self.eeg_bands[band][1], first=True)
        #     else:
        #         self.ch1_bandamp[i] = self.band_amplitude(self.ch1_plot, self.eeg_bands[band][0], self.eeg_bands[band][1])
        #     i += 1
        #
        # freq, psd = self.multitaper_diagram(self.ch2_plot, "CH2", plot=True)
        #
        # i = 0
        # for band in self.eeg_bands:
        #     self.ch2_bandpower[i] = self.bandpower(freq, psd, self.eeg_bands[band][0], self.eeg_bands[band][1])
        #
        #     if i is 0:
        #         self.ch2_bandamp[i] = self.band_amplitude(self.ch2_plot, self.eeg_bands[band][0], self.eeg_bands[band][1], first=True)
        #     else:
        #         self.ch2_bandamp[i] = self.band_amplitude(self.ch2_plot, self.eeg_bands[band][0], self.eeg_bands[band][1])
        #
        #     i += 1

        # self.ch1_plot_delta = self.butter_bandpass_filter(self.ch1_plot, 0.5, 4, self.sf, order=3)
        self.ch1_plot_theta = self.butter_bandpass_filter(self.ch1_plot, 4, 8, self.sf, order=4)
        self.ch1_plot_alpha = self.butter_bandpass_filter(self.ch1_plot, 8, 12, self.sf, order=4)
        self.ch1_plot_beta = self.butter_bandpass_filter(self.ch1_plot, 12, 30, self.sf, order=4)
        self.ch1_plot_gamma = self.butter_bandpass_filter(self.ch1_plot, 30, 45, self.sf, order=4)

        self.ch2_plot_theta = self.butter_bandpass_filter(self.ch2_plot, 4, 8, self.sf, order=4)
        self.ch2_plot_alpha = self.butter_bandpass_filter(self.ch2_plot, 8, 12, self.sf, order=4)
        self.ch2_plot_beta = self.butter_bandpass_filter(self.ch2_plot, 12, 30, self.sf, order=4)
        self.ch2_plot_gamma = self.butter_bandpass_filter(self.ch2_plot, 30, 45, self.sf, order=4)

        self.ch1_beta_peak_x = find_peaks(self.ch1_plot_beta, height=[18, 50])[0]
        self.ch2_beta_peak_x = find_peaks(self.ch2_plot_beta, height=[10, 50])[0]

        self.ch1_theta_peak_x = find_peaks(self.ch1_plot_theta, height=20)[0]
        self.ch2_theta_peak_x = find_peaks(self.ch2_plot_theta, height=20)[0]

        self.plot_raw()
        # pyplot.draw()
        # pyplot.pause(0.0001)
        self.plot()

    def plot(self):

        self.ch1_bandpower = [self.drone.output['blink_one_eye'], self.drone.output['blink_two_eye'], self.drone.output['raise_eyebrow'],
                                self.drone.output['look left']]
        for rect, h in zip(self.ch1_rect, self.ch1_bandpower):

            rect.set_height(h)

        # for rect, h in zip(self.ch2_rect, self.ch2_bandpower):
        #
        #     rect.set_height(h)
        #
        # for rect, h in zip(self.ch1_rect2, self.ch1_bandamp):
        #
        #     rect.set_height(h)
        #
        # for rect, h in zip(self.ch2_rect2, self.ch2_bandamp):
        #
        #     rect.set_height(h)

        pyplot.draw()
        pyplot.pause(0.0001)

    def plot_raw(self):

        if self.plot_time > 5:
            self.ch1_x_ax = np.arange(1281)/256+(self.plot_time-5)
        else:
            self.ch1_x_ax = np.arange(self.ch1_plot.size)/256

        # ch1_min = [min(self.ch1_plot_theta), min(self.ch1_plot_delta), min(self.ch1_plot_alpha),
        #                                                             min(self.ch1_plot_gamma), min(self.ch1_plot_beta)]
        # ch1_max = [max(self.ch1_plot_theta), max(self.ch1_plot_delta), max(self.ch1_plot_alpha),
        #                                                             max(self.ch1_plot_gamma), max(self.ch1_plot_beta)]

        # self.ch1_line.set_data(self.ch1_x_ax, self.ch1_plot)
        self.ch1_fig.set_ylim(-80, 80)
        self.ch1_fig.set_xlim(left=self.ch1_x_ax[0], right=self.ch1_x_ax[-1])
        self.ch1_alpha_line.set_data(self.ch1_x_ax, self.ch1_plot_alpha)
        # self.ch1_delta_line.set_data(self.ch1_x_ax, self.ch1_plot_delta)
        self.ch1_theta_line.set_data(self.ch1_x_ax, self.ch1_plot_theta)
        self.ch1_beta_line.set_data(self.ch1_x_ax, self.ch1_plot_beta)
        self.ch1_gamma_line.set_data(self.ch1_x_ax, self.ch1_plot_gamma)

        if self.plot_time > 5:
            self.ch2_x_ax = np.arange(1281)/256+(self.plot_time-5)
        else:
            self.ch2_x_ax = np.arange(self.ch2_plot.size)/256

        # self.ch2_line.set_data(self.ch2_x_ax, self.ch2_plot)
        self.ch2_fig.set_ylim(-80, 80)
        self.ch2_fig.set_xlim(left=self.ch2_x_ax[0], right=self.ch2_x_ax[-1])
        self.ch2_alpha_line.set_data(self.ch2_x_ax, self.ch2_plot_alpha)
        # self.ch1_delta_line.set_data(self.ch1_x_ax, self.ch1_plot_delta)
        self.ch2_theta_line.set_data(self.ch2_x_ax, self.ch2_plot_theta)
        self.ch2_beta_line.set_data(self.ch2_x_ax, self.ch2_plot_beta)
        self.ch2_gamma_line.set_data(self.ch2_x_ax, self.ch2_plot_gamma)

        self.detect_peak()
        self.decision_making()
        self.ch1_beta_peak_line.set_data(self.ch1_x_ax, self.ch1_beta_peak)
        self.ch1_theta_peak_line.set_data(self.ch1_x_ax, self.ch1_theta_peak)
        self.ch2_beta_peak_line.set_data(self.ch2_x_ax, self.ch2_beta_peak)
        self.ch2_theta_peak_line.set_data(self.ch2_x_ax, self.ch2_theta_peak)


    def detrend(self, data):

        return signal.detrend(data, type='constant')

    def butter_bandpass_filter(self, data, lowcut, highcut, fs, order=2):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        y = lfilter(b, a, data)
        return y

    def multitaper_diagram(self, data, channel, plot=False):

        psd, freq = psd_array_multitaper(data, self.sf, adaptive=True, normalization='full', verbose=0)
        if plot:
            if channel is "CH1":
                self.ch1_d_line.set_data(freq, psd)
                self.ch1_d_fig.set_xlim(left=min(freq), right=max(freq))
                self.ch1_d_fig.set_ylim(min(psd), max(psd))
                pyplot.draw()
                pyplot.pause(0.0001)
            if channel is "CH2":
                self.ch2_d_line.set_data(freq, psd)
                self.ch2_d_fig.set_xlim(left=min(freq), right=max(freq))
                self.ch2_d_fig.set_ylim(min(psd), max(psd))
                pyplot.draw()
                pyplot.pause(0.0001)
        return freq, psd

    def bandpower(self, freq, psd, low, high):

        freq_res = freq[1]-freq[0]
        idx_delta = np.logical_and(freq >= low, freq <= high)
        band_interest = np.logical_and(freq >= self.eeg_bands['Delta'][0], freq <= self.eeg_bands['Gamma'][1])
        bandpower = integrate.simps(psd[idx_delta], dx=freq_res)  # from y_axis range of interest to find bandpower(area under graph)
        total_power = integrate.simps(psd[band_interest], dx=freq_res)  # total area under graph
        relative_power = bandpower / total_power

        return relative_power

    def band_amplitude(self, data, low, high, first=False):

        if first:
            self.fft_vals = np.absolute(np.fft.rfft(data))
            self.fft_freq = np.fft.rfftfreq(len(data), 1.0/self.sf)

        eeg_band_fft = dict()

        freq_ix = np.where((self.fft_freq >= low) & (self.fft_freq <= high))[0]
        eeg_band_fft = np.max(self.fft_vals[freq_ix])

        return eeg_band_fft

    def load_data(self, filename):

        try:
            data = np.loadtxt(filename)
            return data
        except Exception as e:
            pass

    def detect_peak(self):
        self.ch1_beta_count = 0
        self.ch1_beta_peak = np.zeros(len(self.ch1_x_ax))
        for i in self.ch1_beta_peak_x:
            if i > 900:  # 800
                self.ch1_beta_peak[i] = self.ch1_plot_beta[i]
                self.ch1_beta_count += 1

        self.ch2_beta_count = 0
        self.ch2_beta_peak = np.zeros(len(self.ch2_x_ax))
        for i in self.ch2_beta_peak_x:
            if i > 900:
                self.ch2_beta_peak[i] = self.ch2_plot_beta[i]
                self.ch2_beta_count += 1

        self.ch1_theta_count = 0
        self.ch1_theta_peak = np.zeros(len(self.ch1_x_ax))
        for i in self.ch1_theta_peak_x:
            if i > 900:
                self.ch1_theta_peak[i] = self.ch1_plot_theta[i]
                self.ch1_theta_count += 1

        self.ch2_theta_count = 0
        self.ch2_theta_peak = np.zeros(len(self.ch2_x_ax))
        for i in self.ch2_theta_peak_x:
            if i > 900:
                self.ch2_theta_peak[i] = self.ch2_plot_theta[i]
                self.ch2_theta_count += 1

    def decision_making(self):

        # if self.ch1_theta_count + self.ch2_theta_count > 7 and self.ch1_theta_count is not 0 and self.forward_f is 0:        # blink two eye 7
        #     self.write_decision(forward)
        #     self.forward_f = 1
        #     print("forward")
        # elif self.forward_f is 1 and self.ch1_theta_count + self.ch2_theta_count > 12 and self.ch1_theta_count is not 0:
        #     self.write_decision(forward)
        #     self.forward_f2 = 1
        #     print("forward")
        # elif self.ch1_beta_count > 8:               # eyebrow                                         # 6
        #     print("stop")
        #     self.write_decision(stop)
        #
        # elif self.ch2_beta_count + self.ch2_theta_count > 5 or self.forward_f2 is 1:               #blink one eye 10
        #     print("fly up")
        #     self.forward_f = 0
        #     self.forward_f2 = 0
        #     self.write_decision(fly_up)
        self.drone.input['ch1_theta'] = self.ch1_theta_count
        self.drone.input['ch2_theta'] = self.ch2_theta_count
        self.drone.input['ch1_beta'] = self.ch1_beta_count
        self.drone.input['ch2_beta'] = self.ch2_beta_count
        try:
            self.drone.compute()
        except Exception as e:
            #print(e)
            pass

        # print([self.drone.output['blink_one_eye'], self.drone.output['blink_two_eye'], self.drone.output['raise_eyebrow']])

        if self.drone.output['blink_one_eye'] > 0.6:
            print("blink one eye - go_left")
            self.write_decision(go_left)

        elif self.drone.output['blink_two_eye'] > 0.55:
            print("blink two eye - go_right")
            self.write_decision(go_right)

        elif self.drone.output['raise_eyebrow'] > 0.55:
            self.stop_f += 1
            if self.stop_f > 2 and self.forward_f is 1:
                self.write_decision(stop)
                self.forward_f = 0
                print("raise eyebrow - stop")

        elif self.drone.output['look left'] > 0.70:
            print("look left - fly up")
            self.write_decision(fly_up)
            self.forward_f = 1

        elif self.forward_f is 1:
            print("fly up")
            self.write_decision(fly_up)

        # else:
        #     self.stop_f = 0

        # if self.stop_f > 1:


    def write_decision(self, value):

        try:
            f = open("decision.txt", mode='w')
            f.write(str(value+0.1))
        except Exception as e:
            print(e)
        finally:
            f.close()

if __name__ == '__main__':

    filt = filter()
    while True:
        filt.receive_data()
        time.sleep(0.25)

        pass