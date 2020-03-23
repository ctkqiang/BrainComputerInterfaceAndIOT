#!/usr/bin/env python 3
# John Melody Me
# The Most Simple one 
import pyautogui as control
import time as t

# Forward (W)
def goForward():
    t.sleep(1)
    w = 1
    for w in range(10):
        w = 5
        while w < 10 :
            t.sleep(1)
            control.keyDown('w')
            control.moveRel(-123, 0, 0.43)
            control.moveRel(123, 0, 0.43)
            message = "The Key \"W\" is Automated."
            print(message)
            break

# Left (A)
def goLeft():
    t.sleep(1)
    w = 1
    for w in range(10):
        w = 5
        while w < 10 :
            t.sleep(1)
            control.keyDown('a')
            control.moveRel(-123, 0, 0.43)
            control.moveRel(123, 0, 0.43)
            message = "The Key \"A\" is Automated."
            print(message)
            break

# Right (D)
def goRight():
    t.sleep(1)
    w = 1
    for w in range(10):
        w = 5
        while w < 10 :
            t.sleep(1)
            control.keyDown('d')
            control.moveRel(-123, 0, 0.43)
            control.moveRel(123, 0, 0.43)
            message = "The Key \"D\" is Automated."
            print(message)
            break
# Backward (S)
def goBack():
    t.sleep(1)
    w = 1
    for w in range(10):
        w = 5
        while w < 10 :
            t.sleep(1)
            control.keyDown('s')
            message = "The Key \"S\" is Automated."
            print(message)
            break

# Jump (SpaceBar)
def Jump():
    t.sleep(1)
    w = 1
    for w in range(10):
        w = 5
        while w < 10 :
            t.sleep(1)
            control.keyDown('space')
            message = "The Key \"S\" is Automated."
            control.keyDown('space')
            print(message)
            break

def Haha():
    goForward()
    goRight()
    goLeft()
    goBack()
    Jump()

# EXECUTION
Haha()
# # while True:
#     Haha()