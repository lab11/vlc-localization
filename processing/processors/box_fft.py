#!/usr/bin/env python2
# vim: sts=4 ts=4 sw=4 noet:

import argparse

from collections import Counter
import math
import numpy
import cv2
import sys,os
import scipy.signal
import pylab

class Light:
	def __init__(self,x,y,lefts,rights,count):
		self.x = x
		self.y = y
		self.left = lefts
		self.right = rights
		self.count = count
class Point:
	def __init__(self,x,y,freq):
		self.x = x
		self.y = y
		self.freq = freq

def box_light_fft(filename):
	image, imblur,thresh,imthresh,contours,heirarchy,cont_im = adjust_image(filename)
	center_im = image.copy()
	#center_im = numpy.rot90(center_im,3)
	centers = []
	radii = []
	#computing groups of lights using minEnclosingCircles
#	centers,radii, number_of_transmitters = find_first_centers(contours,centers,radii)
	rects ,boxs, centers, number_of_transmitters = find_first_transmitters(contours)
	box_im = image.copy()

	for box in boxs:
		cv2.drawContours(box_im,[box],0,(255,255,0),10)
	cv2.imwrite('/home/noah/lab/box.jpg',box_im)
	if number_of_transmitters == 0:
		empty_center = []
		empty_radii = []
		empty_freq = []
		empty_shape = image.shape
		return empty_center,empty_radii,empty_freq,empty_shape,False
        #computing frequencies
	Fs = 1/(1/(47.54e3))#camera.rolling_shutter_r
	T = 1/Fs
	NFFT = 1024     
	gain = 5
	estimated_frequencies = []
	windowed_size = 100

	average_window = 50
	avg_threshold = 2 #what the hell are these
	expanded_trans_list = []
	final_trans_list = []
	new_centers = []
	new_boxes = []
	#expand list of transmitters, breaking blobs of light using center line
	for i in xrange(number_of_transmitters):
		#Find edges of countour blobs
#		print (boxs[i])
		slope1,slope2 = find_slope(boxs,i)
		image_col = image[:,centers[i][1]]
		avg_threshold = []
		top_boundary, bottom_boundary = find_horizontal_bound(image_col,centers,i,average_window,avg_threshold,image)
#		print ("Top Boundary: " + str(top_boundary) + "   Bottom Boundary: " + str(bottom_boundary))
		################
		#Run Check for angle of box
		print (slope1,slope2)
		if abs(slope1) < .5:
			expanded_trans_list, new_centers, new_boxes = side_fft(expanded_trans_list,new_centers,new_boxes, centers,i,top_boundary,bottom_boundary,image,average_window,boxs)
			print ("Sideways box")
			continue
		################
		avg_threshold = 2#can play!
		layers = []
		layers.append(centers[i])
		temp = []
		temp.append((centers[i][0]+top_boundary)/2)
		temp.append(centers[i][1])
		layers.append(temp)
		temp = []
		temp.append((centers[i][0]+bottom_boundary)/2)
		temp.append(centers[i][1])
		layers.append(temp)
		
		temp = []
		temp.append((centers[i][0]-(top_boundary))/5+centers[i][0])
		temp.append(centers[i][1])
		layers.append(temp)
		temp = []
		temp.append(-(centers[i][0]-(top_boundary))/5+centers[i][0])
		temp.append(centers[i][1])
		layers.append(temp)
		
		temp_trans_list = []
		cord = []
		for k in range(len(layers)):
			point = layers[k]
			image_row = image[point[0]]
			left_boundary, right_boundary = find_vertical_bound(image_row,point,i,average_window,avg_threshold,image)
#			print ("Left Boundary: " + str(left_boundary) + "   Right Boundary: " + str(right_boundary))
			j = left_boundary
			span = 100
			freq_list = []
			freq_list = freq_in_row(j,span,image_row,left_boundary,right_boundary,freq_list)
			val = len(expanded_trans_list)
			expanded_trans_list,cord = seperate_transmitters(freq_list,expanded_trans_list,left_boundary,point,i,cord,k)
#			print (freq_list)
		
#		print ("\nCoordinates on line: " + str(cord) + "\n")
		best_diff = 100000
		best_b = 0
		b = []
#		print ("Should i split? " + str(len(cord)))
		if len(cord) >= 3:
			for j in range(boxs[i][0][0] - boxs[i][1][0]):
				b.append((slope2-slope1)*j)
	#			print (slope1*j + b[-1])
			for j in range(boxs[i][0][0] - boxs[i][1][0]):
				est_x = []
				total_error = 0
				for k in range(len(cord)):
					est_x.append(((-(layers[k][0]- boxs[i][1][1])-b[j])/slope1)+boxs[i][1][0])
					total_error = total_error + abs(est_x[k]-cord[k][1])
	#			print (total_error)
				if total_error < best_diff:
					best_diff = total_error
					best_b = j

			bottom_cord = []
			top_cord = []
			x_cord = int(b[best_b]/(slope2-slope1) + boxs[i][1][0])
			y_cord = int(boxs[i][1][1]-slope2*(x_cord-boxs[i][1][0]))
			bottom_cord.append(x_cord)
			bottom_cord.append(y_cord)
			delta_x = x_cord-boxs[i][1][0]
			delta_y = y_cord-boxs[i][1][1]
			top_x = int(boxs[i][2][0]+delta_x)
			top_y = int(boxs[i][2][1]+delta_y)
			top_cord.append(top_x)
			top_cord.append(top_y)
#			print ("\nBest X: " + str(x_cord))
#			print ("Best Y: " + str(y_cord) + "\n")
			box1 = []
			box2 = []
			box1.append(bottom_cord)
			box1.append(boxs[i][1])
			box1.append(boxs[i][2])
			box1.append(top_cord)
			box2.append(boxs[i][0])
			box2.append(bottom_cord)
			box2.append(top_cord)
			box2.append(boxs[i][3])
			new_boxes.append(box1)
			new_boxes.append(box2)
			x = [p[0] for p in box1]
			y = [p[1] for p in box1]
			new_center = (int(sum(y)/4),int(sum(x)/4))
			new_centers.append(new_center)	
			x = [p[0] for p in box2]
			y = [p[1] for p in box2]
			new_center = (int(sum(y)/4),int(sum(x)/4))
			new_centers.append(new_center)
		else:
			new_boxes.append(boxs[i])
			new_centers.append(centers[i])
	print ("New Centers: " + str(new_centers))
#	cenbox_im = image.copy()
	finbox_im = image.copy()
#	for center in range(len(new_centers)):
#		print (new_centers[center])
#		temp = new_centers[center][0]
#		print (new_centers[center][0])
#		new_centers[center][0] = new_centers[center][1]
#		new_centers[center][1] = temp
#		cenbox_im = cv2.circle(cenbox_im,new_centers[center],63,(0,0,255),-1)
#	cv2.imwrite('/home/noah/lab/center_box.jpg',cenbox_im)
	for box in new_boxes:
		box = numpy.array(box)
		cv2.drawContours(finbox_im,[box],0,(255,255,0),10)
	cv2.imwrite('/home/noah/lab/final_box.jpg',finbox_im)
	freqs = []
#	print (str(len(new_centers)) + " and " + str(len(expanded_trans_list)))
	new_trans_list = []
	print ("expanded_trans_list len: " + str(len(expanded_trans_list)) + " new_centers len: " + str(len(new_centers)))
	for i in range(len(new_centers)):#this could be made more accurate
		expanded_trans_list[i].x = new_centers[i][1]
		expanded_trans_list[i].y = new_centers[i][0]
		#these two may need to be shifted could edit based on total width of found boundary
		#can play around with these values	
		print ("FFT Length: " + str(expanded_trans_list[i].right-expanded_trans_list[i].left))
		fft_len = expanded_trans_list[i].right-expanded_trans_list[i].left
		sub = fft_len/3
		add = fft_len/2
		remainder1 = sub%25
		remainder2 = add%25
		sub = sub - remainder1 + 25
		add = add - remainder2 + 25
		print (str(sub) + " " + str(add))
		expanded_trans_list[i].left = new_centers[i][1] - sub
		expanded_trans_list[i].right = new_centers[i][1] + add
	final_trans_list = []
	#Determine Frequencies of all Transmitters
	spot = 0
	print (len(expanded_trans_list))
        for i in xrange(len(expanded_trans_list)):
                image_row = image[expanded_trans_list[i].y]#figure out this line#######################################################################
#                if expanded_trans_list[i].right - expanded_trans_list[i].left > 3*span:
#			y = image_row[expanded_trans_list[i].left + span :expanded_trans_list[i].right - span ]
#                else:
#			y = image_row[expanded_trans_list[i].left:expanded_trans_list[i].right]
		if expanded_trans_list[i].right - expanded_trans_list[i].left > 100:
			y = image_row[expanded_trans_list[i].left + 50:expanded_trans_list[i].right]
		else:
			y = image_row[expanded_trans_list[i].left:expanded_trans_list[i].right]
			continue#should i allow this?
		L = len(y)
		t = numpy.arange(0,L)*T
		Y = numpy.fft.fft(y* gain, NFFT)/float(L)
		f = Fs/2 * numpy.linspace(0,1,NFFT/2.0+1)
		Y_plot = 2*abs(Y[0:NFFT/2.0+1])
		peaks = scipy.signal.argrelmax(Y_plot)[0]
		idx = numpy.argmax(Y_plot[peaks])
		peak_freq = f[peaks[idx]]
		print ("Peak Frequency at: " + str(peak_freq) + " at " + str(expanded_trans_list[i].left) + " to " + str(expanded_trans_list[i].right) + " and y: " + str(expanded_trans_list[i].y))
		flag = False
		#400 is very noise, can i tone this down?
		for j in xrange(len(estimated_frequencies)):
			if estimated_frequencies[j] < peak_freq + 300 and estimated_frequencies[j] > peak_freq - 300:
				print ("Multiple signals with same frequency")
				flag = True
		if flag == False:
			final_trans_list.append(expanded_trans_list[i])
			estimated_frequencies.append(peak_freq)
			spot = spot + 1
#                estimated_frequencies.append(peak_freq)
	print ("Total Number of Transmitters: " + str(len(final_trans_list)))
#	print (estimated_frequencies)
	if len(final_trans_list) < 3:
		empty_center = []
		empty_radii = []
		empty_freq = []
		empty_shape = image.shape
		return empty_center,empty_radii,empty_freq,empty_shape,False
		
	print ("Estimated Frequencies: " + str(estimated_frequencies))
	center_list = []
	radii_list = []
	for i in xrange(len(final_trans_list)):
		point= []
		point.append(final_trans_list[i].y)
		point.append(final_trans_list[i].x)
		center_list.append(point)
		radii_list.append((final_trans_list[i].right - final_trans_list[i].left)/2)

	centers = numpy.array(center_list) 
	radii = numpy.array(radii_list)
	estimated_frequencies = numpy.array(estimated_frequencies)
#	exit(1)
	return (centers,radii,estimated_frequencies, image.shape,True)	

def side_fft(expanded_trans_list, new_centers,new_boxes, centers,i,top_boundary,bottom_boundary,image,average_window,boxs):
	Fs = 1/(1/(47.54e3))#camera.rolling_shutter_r
	T = 1/Fs
	NFFT = 1024     
	gain = 5

	avg_threshold = 2#can play!
	layers = []
	temp = []
	temp.append((centers[i][0]+top_boundary)/2)
	temp.append(centers[i][1])
	layers.append(temp)
	temp = []
	temp.append((centers[i][0]+bottom_boundary)/2)
	temp.append(centers[i][1])
	layers.append(temp)
	temp_trans_list = []
	horz_freqs = []
	for k in range(len(layers)):
		point = layers[k]
		image_row = image[point[0]]
		left_boundary, right_boundary = find_vertical_bound(image_row,point,i,average_window,avg_threshold,image)
		y = image_row[left_boundary:right_boundary]                       	
		L = len(y)
		t = numpy.arange(0,L)*T
		Y = numpy.fft.fft(y* gain, NFFT)/float(L)
		f = Fs/2 * numpy.linspace(0,1,NFFT/2.0+1)
		Y_plot = 2*abs(Y[0:NFFT/2.0+1])
		peaks = scipy.signal.argrelmax(Y_plot)[0]
		idx = numpy.argmax(Y_plot[peaks])
		peak_freq = f[peaks[idx]]
		horz_freqs.append(peak_freq)
	print horz_freqs
	if horz_freqs[0] < horz_freqs[1] + 300 and horz_freqs[0] > horz_freqs[1] - 300:
		print ("Only one transmitter")
		new_boxes.append(boxs[i])
		new_centers.append(centers[i])
	else:
		print ("Two Transmitters, Must split")
		temp = []
		left = []
		right = []
		#find  best b
		delta_x = boxs[i][1][0] - boxs[i][0][0]
		delta_y = boxs[i][1][1] - boxs[i][0][1]
		left.append(boxs[i][0][0] + delta_x/2)
		left.append(boxs[i][0][1] + delta_y/2)
		right.append(boxs[i][3][0] + delta_x/2)
		right.append(boxs[i][3][1] + delta_y/2)
		box1 = []
		box2 = []
		box1.append(boxs[i][1])
		box1.append(boxs[i][2])
		box1.append(left)
		box1.append(right)
		box2.append(boxs[i][0])
		box2.append(boxs[i][3])
		box2.append(left)
		box2.append(right)
		new_boxes.append(box1)
		new_boxes.append(box2)
		x = [p[0] for p in box1]
		y = [p[1] for p in box1]
		new_center = (int(sum(y)/4),int(sum(x)/4))
		expanded_trans_list.append(Light(new_center[1],new_center[0],left_boundary,right_boundary,10))
		new_centers.append(new_center)	
		x = [p[0] for p in box2]
		y = [p[1] for p in box2]
		new_center = (int(sum(y)/4),int(sum(x)/4))
		expanded_trans_list.append(Light(new_center[1],new_center[0],left_boundary,right_boundary,10))
		new_centers.append(new_center)
	return expanded_trans_list, new_centers, new_boxes


def find_first_transmitters(contours):
	rects = []
	boxs = []
	for contour in contours:
		rect = cv2.minAreaRect(contour)
		if cv2.contourArea(contour) < 104650: #arbitrary
			continue
		else:
			print ("Found Transmitter")
			#find center
			box = cv2.cv.BoxPoints(rect)
			box = numpy.int0(box)
			box = rot_box(box)
			box = numpy.int0(box)
			rects.append(rect)
			boxs.append(box)
	number_of_transmitters = len(rects)
	centers = []
	for i in range(number_of_transmitters):
		x = [p[0] for p in boxs[i]]
		y = [p[1] for p in boxs[i]]
		center = (sum(y)/4,sum(x)/4)
		centers.append(center)
	return rects, boxs, centers, number_of_transmitters

#Determine frequencies of insides of blobs along center line
#def finalize_trans_list(new_centers,new_trans_list):
	
def freq_in_row(j,span,image_row,left_boundary,right_boundary,freq_list):
	Fs = 1/(1/(47.54e3))#camera.rolling_shutter_r
	T = 1/Fs
	NFFT = 1024     
	gain = 5
	while j+span < right_boundary:
		y = image_row[j:j+span]
			                       	
		L = len(y)
		t = numpy.arange(0,L)*T
		Y = numpy.fft.fft(y* gain, NFFT)/float(L)
		f = Fs/2 * numpy.linspace(0,1,NFFT/2.0+1)
		Y_plot = 2*abs(Y[0:NFFT/2.0+1])
#                       pylab.subplot(number_of_transmitters,2,2*i)
#                       pylab.plot(f,Y_plot)
#                       pylab.title(str(centers[i]))
#                       pylab.xlabel('Frequency (Hz)')
#                       pylab.xlim([0,5000])
#                       pylab.savefig('fft/fft' + str(j) +'.png',dpi=1200)
		j = j + 50
		peaks = scipy.signal.argrelmax(Y_plot)[0]
		idx = numpy.argmax(Y_plot[peaks])
		peak_freq = f[peaks[idx]]
		freq_list.append(peak_freq)
#	print (freq_list)
	return freq_list
def seperate_transmitters(freq_list,expanded_trans_list,left_boundary,point,i,cord,types):
	last = freq_list[0]
	left = left_boundary
	last_right = left_boundary
	noise_freq = 300	#arbitrary
	count = 0
	#seperate frequencies of blobs into seperate transmitters
	temp_trans_list = []
	for j in range(len(freq_list)):
		count = count + 1
		if freq_list[j] > last + noise_freq or freq_list[j] < last - noise_freq:
#			print ("last: " + str(last) + " Cur " + str(freq_list[j]))
#			if j + 1 < len(freq_list) and freq_list[j] < freq_list[j + 1] + noise_freq and  freq_list[j] > freq_list[j+1] - noise_freq:#play with line
			x = (last_right+left)/2
			y = point[0]
			temp = []
			temp_trans_list.append(Light(x,y,left,last_right,count-1))
			count = 1
                       	left = last_right                           
		last = freq_list[j]
                if j != 0: last_right = last_right + 50 #could be problem
	x = (last_right+left)/2
	y = point[0]
	temp_trans_list.append(Light(x,y,left,last_right,count))#this is a bit hacky, what if i do the last one twice. WATCH THIS 
	top_count = 0
	top_pos = 0
	sec_count = 0
	sec_pos = 0

	for j in range(len(temp_trans_list)):
		if temp_trans_list[j].count > top_count:
			sec_count = top_count
			sec_pos = top_pos
			top_count = temp_trans_list[j].count
			top_pos = j
		elif temp_trans_list[j].count > sec_count:
			sec_count = temp_trans_list[j].count
			sec_pos = j
	if top_count > 1 and sec_count > 1:
		if temp_trans_list[top_pos].left < temp_trans_list[sec_pos].left:
			if types == 0:
				expanded_trans_list.append(temp_trans_list[top_pos])     
				expanded_trans_list.append(temp_trans_list[sec_pos])
			temp = []
			temp.append(temp_trans_list[top_pos].y)
			temp.append((temp_trans_list[top_pos].right + temp_trans_list[sec_pos].left)/2)
#			temp[-1] = (temp[-1]+temp_trans_list[top_pos].right)/2#experimental
#			temp[-1] = temp_trans_list[top_pos].right#crazy shit
			cord.append(temp)
		else:
			temp = []
			temp.append(temp_trans_list[top_pos].y)
			temp.append((temp_trans_list[top_pos].left + temp_trans_list[sec_pos].right)/2)
#			temp[-1] = (temp[-1]+temp_trans_list[sec_pos].right)/2#experimental
#			temp[-1] = temp_trans_list[sec_pos].right#crazy shit
			cord.append(temp)
			if types == 0:
				expanded_trans_list.append(temp_trans_list[sec_pos])			 
				expanded_trans_list.append(temp_trans_list[top_pos])     
#		print ("Added: " + str(temp_trans_list[top_pos].left) + " To " + str(temp_trans_list[top_pos].right) + " and " + str(temp_trans_list[sec_pos].left) + " To " + str(temp_trans_list[sec_pos].right))         
	elif top_count > 0:
		#should this be if types == 0
		if types == 0:
			expanded_trans_list.append(temp_trans_list[top_pos])        
#		print ("Added: " + str(temp_trans_list[top_pos].count))
	return expanded_trans_list, cord
####################################################################################################################### Cord Could be problem

def find_slope(boxs,i):
	deltax = boxs[i][2][0] - boxs[i][1][0]
	deltay = -(boxs[i][2][1] - boxs[i][1][1])#negative because pixels are not increasing up 
	if deltax == 0: deltax = 1
	slope1 = float(deltay)/float(deltax)
	deltax2 = boxs[i][0][0] - boxs[i][1][0]
	deltay2 = -(boxs[i][0][1] - boxs[i][1][1])#negative because pixels are not increasing up
	if deltax2 == 0: deltax2 = 1
	slope2 = float(deltay2)/float(deltax2)
	return slope1,slope2

def find_vertical_bound(image_row,point,i,average_window,avg_threshold,image):
#	print ("Point: " + str(point))
	left_boundary = point[1] - average_window
	avg_threshold = (sum(image_row[left_boundary:left_boundary+average_window-1])/len(image_row[left_boundary:left_boundary+average_window-1]))/2.5
        right_boundary = point[1] + average_window
        if point[1] > average_window:
		left_boundary = point[1] - average_window
		while left_boundary > 1:
			sub_image_row = image_row[left_boundary:left_boundary+average_window-1]
			if (sum(sub_image_row)/len(sub_image_row)) < avg_threshold:#i can play with this threshold
				break
			else:
				left_boundary -= 1
	else:
		left_boundary = 1

	if point[1] + average_window < min(image.shape):
		right_boundary = point[1] + average_window
		while right_boundary < min(image.shape):
			sub_image_row = image_row[right_boundary-average_window:right_boundary-1]
			if (sum(sub_image_row)/len(sub_image_row)) < avg_threshold:#i can play with this threshold
				break
			else:
				right_boundary += 1
	else:
		right_boundary = min(image.shape)
	return left_boundary,right_boundary

def find_horizontal_bound(image_col,centers,i,average_window,avg_threshold,image):
#	print ("Center-- X: " + str(centers[i][1]) + " Y: " + str(centers[i][0]))
	top_boundary = centers[i][0] - average_window
	bottom_boundary = centers[i][0] + average_window
	avg_threshold = (sum(image_col[top_boundary:top_boundary+average_window-1])/len(image_col[top_boundary:top_boundary+average_window-1]))/2.5
	if centers[i][0] > average_window:
		top_boundary = centers[i][0] - average_window
		while top_boundary > 1:
 			sub_image_col = image_col[top_boundary:top_boundary+average_window-1]
			if (sum(sub_image_col)/len(sub_image_col)) < avg_threshold:
				break
			else:
				top_boundary -= 1
	else:
		top_boundary = 1
	
	if centers[i][0] + average_window < max(image.shape): 
		bottom_boundary = centers[i][0] + average_window
		while bottom_boundary < max(image.shape):
			sub_image_col = image_col[bottom_boundary-average_window:bottom_boundary-1]
			if (sum(sub_image_col)/len(sub_image_col)) < avg_threshold:
				break
			else:
				bottom_boundary += 1
	else:
		bottom_boundary = max(image.shape)
	return top_boundary,bottom_boundary

def adjust_image(filename):
#	filename ='/home/noah/lab/box_light/full/3.jpg'
	image = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)
       	if image.shape[1] > image.shape[0]:
               image = numpy.rot90(image,3)    
        cv2.imwrite('/home/noah/lab/bw.jpg',image)
        imblur = cv2.blur(image,(50,50))
        cv2.imwrite('/home/noah/lab/blur.jpg',imblur)
        thresh, imthresh = cv2.threshold(imblur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        cv2.imwrite('/home/noah/lab/thresh.jpg',imthresh)
        contours, heirarchy = cv2.findContours(imthresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        cont_im = image.copy()

        cv2.drawContours(cont_im,contours,-1,255,3)
        cv2.imwrite('/home/noah/lab/contour.jpg',cont_im)
        return image, imblur,thresh,imthresh,contours,heirarchy,cont_im

def rot_box(box):
	small1 = []
	small2 = []
	small1.append(0)
	small1.append(1)
	small2.append(2)
	small2.append(3)
	small = 100000000
	sec_small = 100000000
	#hypothetically there can be a square...
	for i in range(len(box)):
		j = i + 1
		if i == 3: j = 0
		deltax = abs(box[i][0]-box[j][0])
		deltay = abs(box[i][1]-box[j][1])
		dist = (deltax ** 2.0 + deltay ** 2.0) **(0.5)
#		print (dist)
		if dist < small:
#			print ("Top " + str(i) + " " + str(dist))
			small = dist
			small2[0] = small1[0]
			small2[1] = small1[1]
			small1[0] = i
			small1[1] = j
		elif dist < small + 1 and dist > small - 1:
#			print ("second " + str(i))
			sec_small = dist
			small2[0] = i
			small2[1] = j
#	print (box[small1])
#	print (box[small2])
	low = []
	low2 = []
	lowest1 = box[small1[0]][1]+box[small1[1]][1]
	lowest2 = box[small2[0]][1]+box[small2[1]][1]
	first = 5
	second = 5
	third = 5
	fourth = 5
	if lowest1 > lowest2:
		low.append(small1[0])
		low.append(small1[1])
		low2.append(small2[0])
		low2.append(small2[1])
	else:
		low.append(small2[0])
		low.append(small2[1])
		low2.append(small1[0])
		low2.append(small1[1])
	if box[low[0]][0] > box[low[1]][0]:
		first = low[0]
		second = low[1]
	else:
		first = low[1]
		second = low[0]
	if box[low2[0]][0] < box[low2[1]][0]:
		third = low2[0]
		fourth = low2[1]
	else:
		third = low2[1]
		fourth = low2[0]
	final_box = []
	final_box.append(box[first])
	final_box.append(box[second])
	final_box.append(box[third])
	final_box.append(box[fourth])
	box_copy = []
	for i in range(len(box)):
		box_copy.append(box[i])
	box_copy[0] = box[first]
	box_copy[1] = box[second]
	box_copy[2] = box[third]
	box_copy[3] = box[fourth]
	return box_copy

#check every point down line
"""
	j = left_boundary
	border_list = []
	full_freq_list = []
	lines = image.copy()
	
	for i in range(top_boundary,bottom_boundary):
		print ("line:" + str(i))
		image_row = image[i]
		check = imthresh[i]
		full_freq_list = []
		j = left_boundary
		while j + span < right_boundary:
                        y = image_row[j:j+span]
                        avg_threshold = 3
                        if (sum(y)/len(y)) < avg_threshold:
                                j = j + span
                                continue
			L = len(y)
                        t = numpy.arange(0,L)*T
                        Y = numpy.fft.fft(y* gain, NFFT)/float(L)
                        f = Fs/2 * numpy.linspace(0,1,NFFT/2.0+1)
                        Y_plot = 2*abs(Y[0:NFFT/2.0+1])
                        j = j + 10
                        peaks = scipy.signal.argrelmax(Y_plot)[0]
                        idx = numpy.argmax(Y_plot[peaks])
                        peak_freq = f[peaks[idx]]
                        point = Point(j,i,peak_freq)
			full_freq_list.append(point)
		if full_freq_list:
                	last = full_freq_list[0].freq
                	left = left_boundary
                	last_right = left_boundary

                	for j in range(len(full_freq_list)):
                        	if full_freq_list[j].freq > last + noise_freq or full_freq_list[j].freq < last - noise_freq:

                                	print (str(full_freq_list[j].y) + " "+ str(last) + " Cur " + str(full_freq_list[j].x))
					border_list.append(full_freq_list[j])
					break
				if j != 0: last_right = last_right + 10
	edges = []
	if border_list:
		last = border_list[0]
		for i in xrange(len(border_list)):
#			if i != 0:
			cv2.line(lines,(border_list[i].x,border_list[i].y),(last.x,last.y),(255,0,0),5)
			last = border_list[i]
		cv2.imwrite('/home/noah/lab/lines.jpg',lines)

			
	####################################	
"""
"""
def find_first_centers(contours,centers,radii):
        for contour in contours:
                center, radius = cv2.minEnclosingCircle(contour)

		center = map(int,center)
                radius = int(radius)
                #these however are ovals, not circles
                if radius <= 350:
#                        print ("Skipping transmitter with small pixels")
                        continue
		else:
			print ("Found Transmitter")
                center = (center[1],center[0]) #fuck this line
                contour_area = cv2.contourArea(contour)
                circle_area = math.pi* radius**2
                centers.append(center)
                radii.append(radius)
#                cv2.circle(center_im,center,radius,(124,252,0),10)
#        cv2.imwrite('/home/noah/lab/center.jpg',center_im)
        number_of_transmitters = len(centers)
        print (number_of_transmitters)
	return centers, radii, number_of_transmitters
"""
#Find proposed elements of an oval. run convexhull to eliminate any on inside
#or possibly use fitline to soften the border
#   http://docs.opencv.org/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html?highlight=boundingrect#boundingrect

#MinAreaRect to find original rectangle. can i find angle based off of this? 
#   then call center of mass
