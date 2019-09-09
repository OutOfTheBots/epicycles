import numpy as np
import cv2
from math import sin, cos, pi


#load x and y points on path and parse into 2d data array
data = []
text_file = open('logo_text.txt','r')
for line in text_file:
	comma_pos = line.find(",")
	data.append([int(line[:comma_pos]), int(line[comma_pos + 1:len(line)-1])])
text_file.close()


#create numpy array of complex number datatype and load data
points_list = np.zeros((len(data)),dtype=complex)
for point in range(len(data)):
	points_list.real[point] = data[point][0] 
	points_list.imag[point] = data[point][1]


#calulate needed sin waves using numpy fft
sine_waves = np.fft.fft(points_list)

#break down the complex number output into sine wave componets
epicycles = []
for freq in range(len(sine_waves)):
	amp = np.abs(sine_waves[freq])/len(sine_waves)
	phase = np.angle(sine_waves[freq])
	epicycles.append((amp, phase, freq))

#sort sinewaves by ampatude this isn't needed but looks better
epicycles.sort(reverse=True)



#setup for main loop------------------------------------------

#create video write for output file
out = cv2.VideoWriter('Fourier19.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 60, (1280, 720))

#create array to hold back ground image
back_ground = np.zeros((720,1280,3), np.uint8)

#this is used to translate 0,0 to center of image rather than corner
move_x = 600
move_y = 450

#initize startup varibales
last_x = 0
last_y = 0


#Main loop------------------------------------------

#do 1 full rotation (2 * pi) stepping on each point
for theta in np.arange(0, 2 * pi, 2*pi/len(epicycles)) :	
	
	#take a copy of back ground to draw on
	img = back_ground.copy()	
	
	#start poition at 0,0
	x = 0
	y = 0
	
	#go through every sinwave and draw the clock hands and circles
	for freq in range(len(epicycles)):
		prev_x = x 
		prev_y = y
		
		#each next epicycles position adds ontop of previous position
		x += epicycles[freq][0] * cos(epicycles[freq][2] * theta + epicycles[freq][1])
		y += epicycles[freq][0] * sin(epicycles[freq][2] * theta  + epicycles[freq][1])
		cv2.circle(img,(int(prev_x) + move_x, int(prev_y) + move_y), int(epicycles[freq][0]), (120, 120, 120), 1)
		cv2.line(img,(int(prev_x) + move_x, int(prev_y) + move_y), (int(x) + move_x, int(y) + move_y),(255,255,255),1)	
	
	#proving it is not the very first time i.e nto at position 0 then draw on the back ground
	if last_x != 0: cv2.line(back_ground, (int(x) + move_x, int(y) + move_y),(last_x, last_y),(255,0,0),3)
	last_x = int(x) + move_x
	last_y = int(y) + move_y

	#display the image to screen and write it to file
	cv2.imshow("Fourer", img)
	out.write(img)
	
	#check if q has been pressed for exit
	if cv2.waitKey(1) == ord("q"): break	

#close file and finish
out.release()	
	





