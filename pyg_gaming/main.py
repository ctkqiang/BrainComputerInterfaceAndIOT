#!/usr/bin/env python3
######################################
# STAR LABS BIOSCIENCE PRIVATE LIMITED  
# BRAINTECH PRIVATE LIMITED             
# JOHN MELODY MELISSA                    
######################################     
# This is a copyrighted script.         
# All rights reserved © 2019 BRAINTECH.
######################################
import numpy as np
import os
import pyautogui as control
from pynput.mouse import Button, Controller as MouseController
import time
#from PIL import ImageGrab
#import cv2
from control import eeg_W, eeg_A, eeg_S, eeg_D, eeg_RC, eeg_LC, space
from control import * 
import random
#from directkeys import ReleaseKey, PressKey, W, A, S, D
#from directkeys import * 
#import tkinter as GUI
#from tkinter import *
#from tkinter.ttk import *

# MAIN  FUNC() DECLARATION:
"""def processed_img(original_image):
    # [0, 255, 255] | [0]
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    return processed_img
"""
#random.random()
def main():
    for i in list(range(3))[::-1]:
        print(i+1)
        time.sleep(1)
    
    #delay =  time.sleep(1)

  #  last_time = time.time()
    while(True):
   #     screen =  np.array(ImageGrab.grab(bbox=(0, 40, 1600, 940))) #0, 0, width, height
    #    new_screen = processed_img(screen)
        #printscreen_numpy = np.array(printscreen_pil.getdata(),dtype="uint8")  #\
        #.reshape((printscreen_pil.size[1],printscreen_pil.size[0],3))

        # [W] [A] [S] [D] declaration:
        def forward():
            # if "matlab.mat" == "matlab1.mat":  # <<<< MATLAB FILES HERE
            eeg_W()
            return
        forward()
    
        def backward():
            # if "matlab.mat" == "matlab1.mat":  # <<<< MATLAB FILES HERE
            eeg_S()
            return
        backward()

        def left():
            # if "matlab.mat" == "matlab1.mat":  # <<<< MATLAB FILES HERE
            eeg_A()
            
        left()

        def right():
            # if "matlab.mat" == "matlab1.mat":  # <<<< MATLAB FILES HERE
            eeg_D()
            
        right()

        def look():
            eeg_RC()
        look()
        
        def shoot():
            eeg_LC()
        shoot()
        
        def jump():
            space()
        jump()
        

        # ["#" comment Line -- {50,51,52,53,54}]:
       # loop = "Loop took {} seconds".format(time.time()-last_time)
       # print(loop)
        #last_time = time.time()
        #cv2.imshow("window", new_screen) # new screen undefined.
        #cv2.imshow("window", cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))#cv2.cvtColor(printscreen_numpy, cv2.COLOR_BGR2RGB))
    #    if cv2.waitKey(25) & 0xFF == ord('q'):
    #        cv2.destroyAllWindows()
    #        break
# Function SCREENGRABBING:
main()

