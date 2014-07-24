#!/usr/bin/env python2
# vim: sts=4 ts=4 sw=4 noet:

#This code makes believable assumption that all lights in the room are box lights or are round lights
#This code makes the stretching assumption that any boxlights in the image are fully encompassed by its boundries. (frightening assumption)
	#TODOS: ttempt to fix this by checking points on box for patterns
#This code makes the believable assumption that there are not lights that will end up being squares
#this code makes the hopeful assumption that box lights will never appear as a single transmitter containing 4 frequencies

import argparse

from collections import Counter
import math
import numpy
import cv2
import sys,os
import scipy.signal
import pylab
import opencv_fft

sys.path.append('..')
import pretty_logger
logger = pretty_logger.get_logger()

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

def box_light_fft(filename,debug):
	#Form Contours of lights to be encompassed
	image, imblur,thresh,imthresh,contours,heirarchy,cont_im = adjust_image(filename,debug)
	center_im = image.copy()
	centers = []
	radii = []
	#compute boxes around found transmitters using Bounding Box method
	rects ,boxs, centers, number_of_transmitters = find_first_transmitters(contours)
	if debug == 2:
		box_im = image.copy()
		for box in boxs:
			cv2.drawContours(box_im,[box],0,(255,255,0),10)
		opencv_fft.dbg_save('/tmp/box.png',box_im)

	if number_of_transmitters == 0:
		return exit_box_algorithm(image.shape)

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
		slope1,slope2 = find_slope(boxs,i)
		image_col = image[:,centers[i][1]]
		avg_threshold = []
		top_boundary, bottom_boundary = find_horizontal_bound(image_col,centers,i,average_window,avg_threshold,image)
		if top_boundary == 1:
			top_boundary = boxs[i][2][1]
			bottom_boundary = boxs[i][0][1]
		#Run Check for angle of box
		if abs(slope1) < .2:#i can move this figure after more testing
			expanded_trans_list, new_centers, new_boxes = side_fft(expanded_trans_list,new_centers,new_boxes, centers,i,top_boundary,bottom_boundary,image,average_window,boxs,imthresh)
			print ("Sideways box")
			continue

		avg_threshold = 2#can play!
		layers = add_layers(centers[i],top_boundary,bottom_boundary)	
		temp_trans_list = []
		cord = []
		#Find frequencies along layered points of the transmitter in question
		for k in range(len(layers)):
			point = layers[k]
			image_row = image[point[0]]
			left_boundary, right_boundary = find_vertical_bound(image_row,point,i,average_window,avg_threshold,image)
			j = left_boundary
			span = 100
			freq_list = []
			freq_list = freq_in_row(j,span,image_row,left_boundary,right_boundary,freq_list)
			val = len(expanded_trans_list)
			expanded_trans_list,cord = seperate_transmitters(freq_list,expanded_trans_list,left_boundary,point,i,cord,k)
		
		best_diff = 100000
		best_b = 0
		b = []
		#if there were two boxes found, Split box in two. otherwise keep original.
		if len(cord) >= 3:
			b, best_b = find_intercept(slope1,slope2,cord,layers,boxs,best_diff,i)

			top_cord, bottom_cord = find_box_intercepts(slope1,slope2,b[best_b],boxs,i)

			box1 = create_box(bottom_cord,boxs[i][1],boxs[i][2],top_cord)
			box2 = create_box(boxs[i][0],bottom_cord,top_cord,boxs[i][3])
			#create new algorithm for center of mass calculation. what type of box am i
			new_boxes.append(box1)
			new_boxes.append(box2)

			slidx1,slidy1,slidx2,slidy2 = shift_out(box1,box2,slope2)
			slidx3, slidy3 = shift_vert(boxs,slope1,i)
			mid_topx,mid_topy,mid_botx,mid_boty = find_box_mids(boxs[i])
			sign = find_surroundings(mid_topx,mid_topy,mid_botx,mid_boty,imthresh,image,slope1)
			#modify the individual box centers taking account of surroundings
			add_new_centers(new_centers,slidx1,slidy1,slidx2,slidy2,slidx3,slidy3,box1,box2,sign)
		else:
			#If single box, add original center and box
			new_boxes.append(boxs[i])
			new_centers.append(centers[i])

	print ("New Centers: " + str(new_centers))
	finbox_im = image.copy()
	if  True:
		for box in new_boxes:
			box = numpy.array(box)
			cv2.drawContours(finbox_im,[box],0,(255,255,0),10)
		cv2.imwrite('/home/noah/lab/final_box.png',finbox_im)
		opencv_fft.dbg_save('/temp/final_box.png',finbox_im)
	freqs = []
	new_trans_list = []
	#Edit the bounds of each center found, for 2nd fft run
	for i in range(len(new_centers)):#this could be made more accurate
		expanded_trans_list[i].x = new_centers[i][1]
		expanded_trans_list[i].y = new_centers[i][0]
		edit_light_bounds(expanded_trans_list[i],new_centers[i])

	final_trans_list = []
	#Determine Frequencies of all Transmitters
	spot = 0
	for i in xrange(len(expanded_trans_list)):
		image_row = image[expanded_trans_list[i].y]
		if expanded_trans_list[i].right - expanded_trans_list[i].left > 100:
			y = image_row[expanded_trans_list[i].left + 50:expanded_trans_list[i].right]
		else:
			y = image_row[expanded_trans_list[i].left:expanded_trans_list[i].right]
			continue
		peak_freq = find_peak(y)
		flag = False
		noise = 300		#300 is very noise, can i tone this down?
		#erase transmitters if same frequency as another
		for j in xrange(len(estimated_frequencies)):
			if estimated_frequencies[j] < peak_freq + noise and estimated_frequencies[j] > peak_freq - noise:
				print ("Multiple signals with same frequency")
				flag = True
		if flag == False:
			final_trans_list.append(expanded_trans_list[i])
			estimated_frequencies.append(peak_freq)
			spot = spot + 1

	if len(final_trans_list) < 3:
		return exit_box_algorithm(image.shape)
		
	print ("Estimated Frequencies: " + str(estimated_frequencies))
	center_list = []
	radii_list = []
	for i in xrange(len(final_trans_list)):
		point= []
		point.append(final_trans_list[i].y)
		point.append(final_trans_list[i].x)
		center_list.append(point)
		#the radii list is meaningless right now. what is it used for?
		radii_list.append((final_trans_list[i].right - final_trans_list[i].left)/2)
	circle_im = finbox_im.copy()
	for i in xrange(len(final_trans_list)):
		cv2.circle(circle_im, (final_trans_list[i].x,final_trans_list[i].y),10,(255,255,0),-1,8)
	opencv_fft.dbg_save('/home/noah/lab/circle.png',circle_im)
	centers = numpy.array(center_list) 
	radii = numpy.array(radii_list)
	estimated_frequencies = numpy.array(estimated_frequencies)
	return (centers,radii,estimated_frequencies, image.shape,True)	


#Algorithm to split box lights that are on their side (slope < .2)
def side_fft(expanded_trans_list, new_centers,new_boxes, centers,i,top_boundary,bottom_boundary,image,average_window,boxs,imthresh):

	avg_threshold = 2#can play!
	layers = []
	layers.append(add_scan_point((centers[i][0]+top_boundary)/2,centers[i][1]))
	layers.append(add_scan_point((centers[i][0]+bottom_boundary)/2,centers[i][1]))

	temp_trans_list = []
	horz_freqs = []
	for k in range(len(layers)):
		point = layers[k]
		image_row = image[point[0]]
		left_boundary, right_boundary = find_vertical_bound(image_row,point,i,average_window,avg_threshold,image)
		y = image_row[left_boundary:right_boundary]                       	
		peak_freq = find_peak(y)
		horz_freqs.append(peak_freq)
	noise = 300
	if horz_freqs[0] < horz_freqs[1] + noise and horz_freqs[0] > horz_freqs[1] - noise:
		print ("Only one transmitter")
		new_boxes.append(boxs[i])
		new_centers.append(centers[i])
	else:
		print ("Two Transmitters, Must split")
		left = []
		right = []
		delta_x = boxs[i][1][0] - boxs[i][0][0]
		delta_y = boxs[i][1][1] - boxs[i][0][1]
		left.append(boxs[i][0][0] + delta_x/2)
		left.append(boxs[i][0][1] + delta_y/2)
		right.append(boxs[i][3][0] + delta_x/2)
		right.append(boxs[i][3][1] + delta_y/2)
		box1 = create_box(left,boxs[i][1],boxs[i][2],right)
		box2 = create_box(boxs[i][0],left,right,boxs[i][3])

		new_boxes.append(box1)
		new_boxes.append(box2)
		#create new algorithm for center of mass calculation. what type of box am i
		x = [p[0] for p in box1]
		y = [p[1] for p in box1]
		
		topy = (box1[1][1] + box1[2][1])/2
		boty = (box1[0][1] + box1[3][1])/2
		mid_leftx = (boxs[i][0][0] + boxs[i][1][0])/2
		mid_rightx = (boxs[i][2][0] + boxs[i][3][0])/2
		length = abs(boxs[i][1][0] - boxs[i][2][0])
		checkx = length/30
		sign = 0
		if mid_leftx - checkx > 1  and imthresh[int(sum(y)/4),mid_leftx - checkx]:
			sign = 1
		elif mid_rightx + checkx < min(image.shape) and imthresh[int(sum(y)/4),mid_rightx + checkx]:
			sign = -1
		else:
			sign = 0
		diff = (boty - topy)/5
		midy = (boty+topy)/2 - diff
		#this method does not rotate well
		new_center = (midy,int(sum(x)/4) + sign*checkx)
		expanded_trans_list.append(Light(new_center[1],new_center[0],left_boundary,right_boundary,10))
		new_centers.append(new_center)	
		topy2 = (box2[1][1] + box2[2][1])/2
		boty2 = (box2[0][1] + box2[3][1])/2
		diff2 = (boty2 - topy2)/5
		midy2 = (boty2+topy2)/2 + diff2
		x = [p[0] for p in box2]
		y = [p[1] for p in box2]
		new_center = (midy2,int(sum(x)/4)+ sign*checkx)
		expanded_trans_list.append(Light(new_center[1],new_center[0],left_boundary,right_boundary,10))
		new_centers.append(new_center)
	return expanded_trans_list, new_centers, new_boxes

#add layers to places to check for multiple boxes
def add_layers(center,top_boundary,bottom_boundary):
	layers = []
	layers.append(center)
	layers.append(add_scan_point((center[0]+top_boundary)/2,center[1]))
	layers.append(add_scan_point((center[0]+bottom_boundary)/2,center[1]))
	layers.append(add_scan_point((center[0]-(top_boundary))/5+center[0],center[1]))
	layers.append(add_scan_point((-(center[0]-(top_boundary))/5+center[0]),center[1]))
	return layers

#edit the range to run fft on a specific transmitter for better accuracy
def edit_light_bounds(transmitter,center):
	fft_len = transmitter.right-transmitter.left
	sub = fft_len/3
	add = fft_len/2
	remainder1 = sub%25
	remainder2 = add%25
	sub = sub - remainder1 + 25
	add = add - remainder2 + 25
	transmitter.left = center[1] - sub
	transmitter.right = center[1] + add

#find intercepts of shifted slope along box at splitting point
def find_box_intercepts(slope1,slope2,yintercept,boxs,i):
	bottom_cord = []
	top_cord = []
	bottom_cord.append(int(yintercept/(slope2-slope1) + boxs[i][1][0]))
	delta_x = bottom_cord[-1]-boxs[i][1][0]
	bottom_cord.append(int(boxs[i][1][1]-slope2*(bottom_cord[-1]-boxs[i][1][0])))
	delta_y = bottom_cord[-1]-boxs[i][1][1]
	top_cord.append(int(boxs[i][2][0]+delta_x))
	top_cord.append(int(boxs[i][2][1]+delta_y))
	return top_cord,bottom_cord	

#find y intercept of optimal slope location to split box
def find_intercept(slope1,slope2,cord,layers,boxs,best_diff,i):
	b = []
	for j in range(boxs[i][0][0] - boxs[i][1][0]):
		b.append((slope2-slope1)*j)
	for j in range(boxs[i][0][0] - boxs[i][1][0]):
		est_x = []
		total_error = 0
		for k in range(len(cord)):
			est_x.append(((-(layers[k][0]- boxs[i][1][1])-b[j])/slope1)+boxs[i][1][0])
			total_error = total_error + abs(est_x[k]-cord[k][1])
		if total_error < best_diff:
			best_diff = total_error
			best_b = j
	return b,best_b

#edit and add new centers to the new centers list(after splitting)
def add_new_centers(new_centers,slidx1,slidy1,slidx2,slidy2,slidx3,slidy3, box1,box2,sign):
	x = [p[0] for p in box1]
	y = [p[1] for p in box1]	
	y1 = int(sum(y)/4) + int(slidy1) + int(sign*slidy3)
	x1 = int(sum(x)/4) + int(slidx1) + int(sign*slidx3)
	new_center = (y1,x1)
	new_centers.append(new_center)	
	x = [p[0] for p in box2]
	y = [p[1] for p in box2]
	y2 = int(sum(y)/4) + int(slidy2) + int(sign*slidy3)
	x2 = int(sum(x)/4) + int(slidx2) + int(sign*slidx3)
	new_center = (y2,x2)
	new_centers.append(new_center)

#run fft on a given area of the image, returning highest peak
def find_peak(y):
	Fs = 1/(1/(47.54e3))#camera.rolling_shutter_r
	T = 1/Fs
	NFFT = 1024     
	gain = 5

	L = len(y)
	t = numpy.arange(0,L)*T
	Y = numpy.fft.fft(y* gain, NFFT)/float(L)
	f = Fs/2 * numpy.linspace(0,1,NFFT/2.0+1)
	Y_plot = 2*abs(Y[0:NFFT/2.0+1])
	peaks = scipy.signal.argrelmax(Y_plot)[0]
	idx = numpy.argmax(Y_plot[peaks])
	peak_freq = f[peaks[idx]]

	return peak_freq

#determine if box is part of lower or upper light
def find_surroundings(mid_topx,mid_topy,mid_botx,mid_boty,imthresh,image,slope1):
	val = 1200#arbitrary constant
	checkx = val/slope1
	checky = val
	if mid_topy - checky > 0 and mid_topx + checkx > 1 and mid_topx + checkx < min(image.shape) and imthresh[mid_topy - checky,mid_topx + checkx]:
		#if lower box
		sign = 1
	elif mid_boty + checky < max(image.shape) and mid_botx - checkx > 1 and mid_botx - checkx < min(image.shape)  and imthresh[mid_boty+checky,mid_botx-checkx]:
		#if upper box
		sign = -1
	else:
		#if only box
		sign = 0
	return sign

#find middle of top and bottom of box
def find_box_mids(box):
	mid_topx = int((box[2][0] + box[3][0])/2)
	mid_topy = int((box[2][1] + box[3][1])/2)
	mid_botx = int((box[0][0] + box[1][0])/2)
	mid_boty = int((box[0][1] + box[1][1])/2)
	return mid_topx,mid_topy,mid_botx,mid_boty

#shift center up or down accounting for neighbors 
def shift_vert(boxs,slope1,i):
	diff = re_orient(boxs[i])
	slidy3 = diff
	slidx3 = -diff/slope1
	return slidx3,slidy3

#shift centers out to account for diffuser pushing center to outside
def shift_out(box1,box2,slope2):
	leftx = (box1[1][0] + box1[2][0])/2
	rightx = (box1[0][0] + box1[3][0])/2
	diff1 = (rightx - leftx)/5
	leftx2 = (box2[1][0] + box2[2][0])/2
	rightx2 = (box2[0][0] + box2[3][0])/2
	diff2 = (rightx2 - leftx2)/5
	slidx1 = -diff1
	slidy1 = slope2*diff1
	slidx2 = diff2
	slidy2 = -slope2*diff2	
	return slidx1,slidy1,slidx2,slidy2	

#return distance from top to bottom of box
def re_orient(box):
	order = []
	for i in range(4):
		if i == 0:
			order.append(box[i][1])
		else:
			flag = False
			for j in range(len(order)):
				if box[i][1] < order[j]:
					order.insert(j,box[i][1])
					flag = True
					break
			if flag == False:
				order.append(box[i][1])
	diff = ((order[2] + order[3])/2 -(order[0] + order[1])/2)/30
	return diff

#find centers of original transmitters, also build bounding boxes
def find_first_transmitters(contours):
	rects = []
	boxs = []
	for contour in contours:
		rect = cv2.minAreaRect(contour)
		if cv2.contourArea(contour) < 100000: #arbitrary
			continue
		else:
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
		#create new algorithm for center of mass calculation. what type of box am i
		x = [p[0] for p in boxs[i]]
		y = [p[1] for p in boxs[i]]
		center = (sum(y)/4,sum(x)/4)
		centers.append(center)

	return rects, boxs, centers, number_of_transmitters

#Determine frequencies of insides of blobs along line
def freq_in_row(j,span,image_row,left_boundary,right_boundary,freq_list):
	while j+span < right_boundary:
		y = image_row[j:j+span]   
		peak_freq = find_peak(y)                    	
		j = j + 50
		freq_list.append(peak_freq)
	return freq_list

#finds seperate transmitters and designates the top two frequencies
def seperate_transmitters(freq_list,expanded_trans_list,left_boundary,point,i,cord,types):
	last = freq_list[0]
	left = left_boundary
	last_right = left_boundary+50#changed
	noise_freq = 300	#arbitrary
	count = 0
	#seperate frequencies of blobs into seperate transmitters
	temp_trans_list = []
	for j in range(len(freq_list)):
		count = count + 1
		if freq_list[j] > last + noise_freq or freq_list[j] < last - noise_freq:
			x = (last_right+left)/2
			y = point[0]
			temp = []
			temp_trans_list.append(Light(x,y,left,last_right,count-1))
			count = 1
			left = last_right                           
		last = freq_list[j]
#		if j != 0: last_right = last_right + 50 
		last_right = last_right + 50
	x = (last_right+left)/2
	y = point[0]
	temp_trans_list.append(Light(x,y,left,last_right,count))
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
#			temp[-1] = (temp[-1]+temp_trans_list[top_pos].right)/2#make right boundary between middle and left boundary of second box
			temp[-1] = temp_trans_list[top_pos].right#make right boundary, left boundary of second box
			cord.append(temp)
		else:
			temp = []
			temp.append(temp_trans_list[top_pos].y)
			temp.append((temp_trans_list[top_pos].left + temp_trans_list[sec_pos].right)/2)
#			temp[-1] = (temp[-1]+temp_trans_list[sec_pos].right)/2#make right boundary between middle and left boundary of second box
			temp[-1] = temp_trans_list[sec_pos].right#make right boundary, left boundary of second box
			cord.append(temp)
			if types == 0:
				expanded_trans_list.append(temp_trans_list[sec_pos])			 
				expanded_trans_list.append(temp_trans_list[top_pos])     
  
	elif top_count > 0:
		if types == 0:
			expanded_trans_list.append(temp_trans_list[top_pos])        
	return expanded_trans_list, cord

#find slopes of bounding box
def find_slope(boxs,i):
	deltax = boxs[i][2][0] - boxs[i][1][0]
	deltay = -(boxs[i][2][1] - boxs[i][1][1])#negative because pixels are not increasing up 
	if deltax == 0: deltax = 1
	slope1 = float(deltay)/float(deltax)
	deltax2 = boxs[i][0][0] - boxs[i][1][0]
	deltay2 = -(boxs[i][0][1] - boxs[i][1][1])
	if deltax2 == 0: deltax2 = 1
	slope2 = float(deltay2)/float(deltax2)
	return slope1,slope2

#find side boundaries of box
def find_vertical_bound(image_row,point,i,average_window,avg_threshold,image):
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

#find top and bottom boundaries of box
def find_horizontal_bound(image_col,centers,i,average_window,avg_threshold,image):
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

#build usable image contours for bounding box algorithm
def adjust_image(filename,debug):
	image = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)
	if image.shape[1] > image.shape[0]:
		image = numpy.rot90(image,3)    
	imblur = cv2.blur(image,(50,50))
	thresh, imthresh = cv2.threshold(imblur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	contours, heirarchy = cv2.findContours(imthresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	cont_im = image.copy()
	cv2.drawContours(cont_im,contours,-1,255,3)
	if debug == 2:
		opencv_fft.dbg_save('/tmp/bw.png',image)
		opencv_fft.dbg_save('/tmp/blur.png',imblur)
		opencv_fft.dbg_save('/tmp/thresh.png',imthresh)
		opencv_fft.dbg_save('/tmp/contour.png',cont_im)
	return image, imblur,thresh,imthresh,contours,heirarchy,cont_im

#add coordinate to scan
def add_scan_point(y,x):
	temp = []
	temp.append(y)
	temp.append(x)
	return temp

#create box for new bounding box after split
def create_box(pos0,pos1,pos2,pos3):
	box = []
	box.append(pos0)
	box.append(pos1)
	box.append(pos2)
	box.append(pos3)
	return box
		
#check if need to exit code because not box lights
def exit_box_algorithm(shape):
	empty_center = []
	empty_radii = []
	empty_freq = []
	empty_shape = shape
	return empty_center,empty_radii,empty_freq,empty_shape,False

#rotate box such that 0 and 1 go along short side, and 2-3 go along short side. 0-1 is either further left or lower or both
#either 0 or 1 is bottom left position, box must go 0,1,2,3 clockwise
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
		if dist < small:
			small = dist
			small2[0] = small1[0]
			small2[1] = small1[1]
			small1[0] = i
			small1[1] = j
		elif dist < small + 1 and dist > small - 1:
			sec_small = dist
			small2[0] = i
			small2[1] = j
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
	final_box = create_box(box[first],box[second],box[third],box[fourth])

	box_copy = []
	for i in range(len(box)):
		box_copy.append(box[i])	
	box_copy[0] = box[first]
	box_copy[1] = box[second]
	box_copy[2] = box[third]
	box_copy[3] = box[fourth]
	return box_copy


