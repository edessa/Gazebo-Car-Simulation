import pygame
import ach
import hubo_ach as ha
import sys
import time
from ctypes import *
import numpy as np
import diff_drive
import socket
import cv2.cv as cv
import cv2
import numpy as np
import math

dd = diff_drive
ref = dd.H_REF()
tim = dd.H_TIME()

ROBOT_DIFF_DRIVE_CHAN   = 'robot-diff-drive'
ROBOT_CHAN_VIEW   = 'robot-vid-chan'
ROBOT_TIME_CHAN  = 'robot-time'
# CV setup 
cv.NamedWindow("wctrl", cv.CV_WINDOW_AUTOSIZE)
#capture = cv.CaptureFromCAM(0)
#capture = cv2.VideoCapture(0)

newx = 320
newy = 240

nx = 640
ny = 480

r = ach.Channel(ROBOT_DIFF_DRIVE_CHAN)
r.flush()
v = ach.Channel(ROBOT_CHAN_VIEW)
v.flush()
t = ach.Channel(ROBOT_TIME_CHAN)
t.flush()

i=0
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
 
pygame.init()
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Current position
x_coord = 10
y_coord = 10
maximum = 32767.0


ref.ref[0] = 0
ref.ref[1] = 0

# Count the joysticks the computer has
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    # No joysticks!
    print("Error, I didn't find any joysticks.")
else:
    # Use joystick #0 and initialize it
    my_joystick = pygame.joystick.Joystick(0)
    my_joystick.init()
while not done:

    # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
 
    # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
 
    # As long as there is a joystick
    if joystick_count != 0:
 
        # This gets the position of the axis on the game controller
        # It returns a number between -1.0 and +1.0
        jl00 = my_joystick.get_axis(0)
        jl01 = my_joystick.get_axis(1)
        jl10 = my_joystick.get_axis(2)
        jl11 = my_joystick.get_axis(3)
        for i in range(0,16):
          my_joystick.get_button(i)
	
	
	if jl01 > 0:
	  if jl11 > 0:
	    ref.ref[0] = -jl01
  	    ref.ref[1] = -jl11
	if jl01 < 0:
	  if jl11 < 0:
	    ref.ref[0] = -jl01
	    ref.ref[1] = -jl11
	if jl00 > 0:
	  if jl10 > 0:
  	    ref.ref[0] = -jl00
	    ref.ref[1] = jl10
	if jl00 < 0:
	  if jl10 < 0:
	    ref.ref[0] = -jl00
	    ref.ref[1] = jl10
	if jl00 == 0 and jl01 == 0 and jl10 == 0 and jl11 == 0:
	  ref.ref[0] = 0
	  ref.ref[1] = 0

    	print 'Sim Time = ', tim.sim[0]
    
    	# Sets reference to robot
    	r.put(ref);

    	# Sleeps
    	time.sleep(0.1)   

	# Close the connection to the channels
#	r.close()
#	s.close()
 
    # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
 
    clock.tick(60)
 
pygame.quit()
