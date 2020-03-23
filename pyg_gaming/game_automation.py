#!/usr/bin/env python3

import pyautogui as control
import time as t


# get Screen Size 
def gss():
      w , h = control.size()
      print(w , h)

# Forward (W)
def goForward():
      t.sleep(1)
      w =1
      for w in range(3):
            w = 5
            while w < 7:
                  t.sleep(1)
                  control.keyDown('w')
                  message = "The Key \"W\" is Automated"
                  print("Log:", message)
                  break
            
# Left (A)
def goLeft():
      t.sleep(1)
      w =1
      for w in range(3):
            w = 5
            while w < 7:
                  t.sleep(1)
                  control.keyDown('a')
                  control.moveRel(123, 0, 0.43)
                  #control.moveRel(-123, 0, 0.43)
                  message = "The Key \"A\" is Automated"
                  print("Log:", message)
                  break
            
# Right (D)
def goRight():
      t.sleep(1)
      w =1
      for w in range(3):
            w = 5
            while w < 7:
                  t.sleep(1)
                  control.keyDown('d')
                  control.moveRel(-123, 0, 0.43)
                  #control.moveRel(123, 0, 0.43)
                  message = "The Key \"D\" is Automated"
                  print("Log:", message)
                  break
            
# Backward (S)
def backWard():
      t.sleep(1)
      w =1
      for w in range(3):
            w = 5
            while w < 7:
                  t.sleep(1)
                  control.keyDown('s')
                  message = "The Key \"S\" is Automated"
                  print("Log:", message)
                  break
      
            
# Jump (spaceBar)
def jump():
      t.sleep(1)
      w =1
      for w in range(3):
            w = 5
            while w < 7:
                  t.sleep(1)
                  control.keyDown('space')
                  message = "The Key \"Space Bar\" is Automated"
                  print("Log:", message)
                  break

# Execution
def run():
      goForward()
      goLeft()
      goRight()
      #backWard()
      goForward()
      jump()


run()
