#!/usr/bin/env python3
######################################
# STAR LABS BIOSCIENCE PRIVATE LIMITED  
# BRAINTECH PRIVATE LIMITED             
# JOHN MELODY MELISSA                    
######################################     
# This is a copyrighted script.         
# All rights reserved © 2019 BRAINTECH.
######################################
import pyautogui
import os
import time
# import cv2
# Move FORWARD:
def eeg_W():
        time.sleep(1)
        w = 1
        for w in range(10):
            w = 5
            while w < 10: 
                time.sleep(1)
                pyautogui.keyDown('w')  # Previously control.press("w")
               # pyautogui.hotkey("shift") 
                key = " \"Up Arrow\" :: "
                direction = "FORWARD"
                print(key + "is pressed" + "." + " The $SUBJECT is moving " + direction)
                break
eeg_W()

# Move LEFT:
def eeg_A():
        time.sleep(1)
        a = 1
        for a in range(5):
            a = 5
            while a < 10: 
                time.sleep(1) 
                pyautogui.keyDown("a")
                pyautogui.moveRel(-123, 0, 0.34)
                pyautogui.moveRel(123, 0, 0.34)
                pyautogui.keyUp("a")
                key = " \"Left Arrow\" :: "
                direction = "LEFT"
                print(key + "is pressed" + "." + " The $SUBJECT is moving " + direction)
                break
eeg_A()


# Move Backward:
def eeg_S():
        for s in range(5):
                s = 5
                while s < 10:
                        time.sleep(1)
                        pyautogui.keyDown("s")
                        key = " \"Down Arrow\" ::"
                        pyautogui.keyUp("s")
                        direction = "BACKWARD"
                        print(key + "is pressed" + "." + " The $SUBJECT is moving " + direction)
                        break
eeg_S()

# Move Right:
def eeg_D():
        for d in range(5):
                d = 5
                while d < 10:
                        time.sleep(1) 
                        pyautogui.keyDown("d")
                        pyautogui.moveRel(123, 0, 0.34)
                        pyautogui.moveRel(-123, 0, 0.34)
                        pyautogui.keyUp("d")
                        key = " \"Right Arrow\" ::"
                        direction = "RIGHT"
                        print(key + "is pressed" + "." + " The $SUBJECT is moving " + direction)
                        break
eeg_D()

# Right click:
def eeg_RC():
        for d in range(2):
                d = 2
                while d < 5: 
                        pyautogui.click(button="right")
                        key = " \"Right Click\" ::"
                        action = "Look"
                        print(key + "is clicked" + "." + " The $SUBJECT is $action+ " + action)
                        break
eeg_RC()

# Left click:
def eeg_LC():
        for d in range(5):
                d = 2
                while d < 10: 
                        pyautogui.click(button="left")
                        pyautogui.mouseDown()
                        key = " \"Left Click\" ::"
                        action = "Look"
                        print(key + "is clicked" + "." + " The $SUBJECT is $action+ " + action)
                        break
eeg_RC()

def space():
         for d in range(5):
                d = 2
                while d < 10: 
                        pyautogui.keyDown("space")
                        pyautogui.moveRel(123, 0, 0.34)
                        pyautogui.moveRel(-123, 0, 0.34)
                        time.sleep(2)
                        pyautogui.keyUp("space")
                        break
space()