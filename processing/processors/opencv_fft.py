#!/usr/bin/env python
# vim: sts=4 ts=4 sw=4 noet:

from __future__ import print_function
import sys, os
import math
import argparse

import cv2
import numpy
import scipy.signal
import pylab

sys.path.append('..')
import pretty_logger
logger = pretty_logger.get_logger()

# n.b. step counter is not thread-safe, but only for deep debug anyway
dbg_step = 0
def dbg_fname(fname):
	global dbg_step
	dbg_step += 1
	return '/tmp/luxp-opencv_fft-step{}-'.format(dbg_step) + fname + '.png'

def dbg_save(fname, array):
	fname = dbg_fname(fname)
	cv2.imwrite(fname, array)
	logger.debug('Saved WIP to {}'.format(fname))

def dbg_plot_subplots(fname):
	logger.start_op('plot_subplots for ' + fname)
	fname = dbg_fname(fname)
	pylab.savefig(fname, dpi=300)
	logger.debug('Plotted WIP subplots to {}'.format(fname))
	logger.end_op()

@logger.op("Process image {0} taken with {2}")
def imag_proc(file_name, num_of_tx, camera):
	BLACK  = (  0,   0,   0)
	WHITE  = (255, 255, 255)
	BLUE   = (255,   0,   0)
	GREEN  = (  0, 255,   0)
	RED    = (  0,   0, 255)
	YELLOW = (  0, 255, 255)
	TEAL   = (255, 255,   0)
	MAGENTA= (255,   0, 255)

	if 'PICS' in os.environ:
		debug = True
	else:
		debug = False

	if 'DEBUG' in os.environ and int(os.environ['DEBUG']) >= 3:
		logger.warn("DEBUG=3 doesn't save pictures any more")
		logger.warn("I split saving pictures out to its own independent setting")
		logger.warn("Use PICS=1 to save intermediate images")

	if debug:
		global dbg_step
		dbg_step = 0

	# Load image and convert to grayscale
	logger.start_op("Loading image")
	gray_image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
	logger.debug('gray_image.shape = {}'.format(gray_image.shape))
	if debug:
		dbg_save('gray_image', gray_image)
	logger.end_op()

	# Handle orientation
	logger.start_op("Normalizing image rotation")
	if gray_image.shape[1] > gray_image.shape[0]:
		logger.debug("Rotated image")
		gray_image = numpy.rot90(gray_image, 3)
	else:
		logger.debug("No rotation")
	if debug:
		dbg_save('gray_image_rotated', gray_image)
	logger.debug('gray_image.shape = {}'.format(gray_image.shape))
	logger.end_op()

	# Blur image
	logger.start_op("Applying blur")
	#m2 = cv2.GaussianBlur(gray_image, (31,31), 0)
	m2 = cv2.blur(gray_image, (50,50)) # faster and good enough
	#m2 = cv2.blur(gray_image, (150,150)) # faster and good enough
	if debug:
		dbg_save('after_blur', m2)
	logger.debug('m2.shape = {}'.format(m2.shape))
	logger.end_op()

	# Replace manual threshold with more efficient OTSU filter
	logger.start_op("Threshold image")
	#threshold, thresholded_img = cv2.threshold(m2, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	thresholded_img = cv2.adaptiveThreshold(m2, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 101, 2)
	if debug:
		dbg_save('thresholded_img', thresholded_img)
	logger.end_op()

	# Find and label disjoint sets of pixels (each transmitter blob)
	logger.start_op("Locate transmitters")

	# opencv3.0 has a connectedComponents API but that's sadly not released yet
	#ret, markers = cv2.connectedComponents(thresholded_img)

	# We solve this by drawing an outline ("contour") around each blob
	contours, heirarchy = cv2.findContours(thresholded_img, cv2.RETR_LIST,
			cv2.CHAIN_APPROX_SIMPLE)

	if debug:
		# drawContours draws contours on the supplied image, need a copy
		contour_image = gray_image.copy()
		cv2.drawContours(contour_image, contours, -1, 255, 3)
		dbg_save('contours', contour_image)

		#contours_kept_image = gray_image.copy()
		contours_kept_image = cv2.imread(file_name, cv2.IMREAD_COLOR)

		# Draw the center point; useful for eyeballing calibration
		kept_center = (contours_kept_image.shape[1] / 2, contours_kept_image.shape[0] / 2)
		cv2.circle(
				contours_kept_image,
				kept_center,
				5, # radius
				RED, # color
				-1 # fill circle
				)
		cv2.circle(
				contours_kept_image,
				(kept_center[0], kept_center[1]+20),
				5, # radius
				RED, # color
				-1 # fill circle
				)
		cv2.circle(
				contours_kept_image,
				(kept_center[0]+20, kept_center[1]),
				5, # radius
				RED, # color
				-1 # fill circle
				)
		cv2.circle(
				contours_kept_image,
				(kept_center[0]+40, kept_center[1]),
				5, # radius
				RED, # color
				-1 # fill circle
				)

	# And then fitting a circle to that contour
	centers = []
	radii = []
	for contour in contours:
		center, radius = cv2.minEnclosingCircle(contour)
		center = map(int, center)
		radius = int(radius)
		if radius <= 33:
			logger.debug('Skipping transmitter at {} with small radius ({} pixels)'.format(center, radius))
			continue
		# For some reason minEnclosingCircle flips x and y?
		center = (center[1], center[0])
		#assert thresholded_img[center[0], center[1]] == 1, 'Center of blob is not lit?'

		reject = False
		for pt in contour:
			# List of lists? Maybe some contour structure could have blob points?
			assert len(pt) == 1
			pt = pt[0]
			# More x,y flip?
			if \
			pt[1] < 10 or \
			pt[0] < 10 or \
			pt[1] > (thresholded_img.shape[0]-10) or \
			pt[0] > (thresholded_img.shape[1]-10):
				reject = True
				logger.debug("Bad edge point: {}".format(pt))
				break

		if reject:
			logger.debug('Rejecting edge contour at {}'.format(center))
			continue

		contour_area = cv2.contourArea(contour)
		circle_area = math.pi * radius**2
		logger.debug('Transmitter area {:0.1f}. Radius {} px. Contour area {}.  %age {:0.1f}'.format(
			circle_area, radius, contour_area, (contour_area / circle_area)*100 ))
		if (contour_area / circle_area) < .5:
			logger.debug('Rejecting non-circular contour at {}'.format(center))
			continue
		centers.append(center)
		radii.append(radius)

		if debug:
			cv2.drawContours(contours_kept_image, [contour,], -1, TEAL, 3)

	if debug:
		dbg_save('contours-kept', contours_kept_image)

	number_of_transmitters = len(centers)
	#assert number_of_transmitters >= 3, 'not enough transmitters'
	logger.end_op()


	# Compute transmitter frequencies
	logger.start_op("Computing transmitter frequencies")

	Fs = 1/camera.rolling_shutter_r
	T = 1/Fs
	# 2**14 good balance of speed / resolution [5~10 hz for small sample set]
	NFFT = 2**14
	gain = 5

	estimated_frequencies = []
	window_size = 100

	average_window = 40;
	avg_threshold = 20;

	light_circles = gray_image.copy()

	for i in xrange(number_of_transmitters):
		try:
			row_start = max(0, centers[i][0] - radii[i])
			row_end = min(gray_image.shape[0]-1, centers[i][0] + radii[i])
			column_start = max(0, centers[i][1] - radii[i])
			column_end = min(gray_image.shape[1]-1, centers[i][1] + radii[i])

			#Slice image around current center and sum across all rows
			image_slice = gray_image[row_start:row_end, column_start:column_end]
			image_slice_mean = numpy.mean(image_slice)
			image_row = numpy.sum(image_slice, axis=0)

			#Remove any DC component
			image_row = image_row - numpy.mean(image_row)

			#Apply window
			y = image_row * numpy.hamming(image_row.shape[0])

			#Take FFT
			L = len(y)
			Y = numpy.fft.fft(y* gain, NFFT) / float(L)
			f = Fs/2 * numpy.linspace(0,1,NFFT/2.0+1)
			Y_plot = 2*abs(Y[0:NFFT/2.0+1])

			#TODO: Apply heuristic to determine SNR

			if debug:
				pylab.subplot(number_of_transmitters,2,2*i+1)
				pylab.title(str(centers[i]), size='xx-small')
				pylab.ylim([-13000,13000])
				pylab.yticks([-13000,0,13000])
				pylab.tick_params(labelsize=4)
				pylab.plot(y)

			##Improve center by thresholding image and obtaining minimum enclosing circle
			#_, image_slice_thresh = cv2.threshold(image_slice, image_slice_mean*1.5, 1, cv2.THRESH_BINARY)
			#image_slice_thresh_contours, _ = cv2.findContours(image_slice_thresh, cv2.RETR_LIST,
			#	cv2.CHAIN_APPROX_SIMPLE)
			#image_slice_thresh_contours = numpy.vstack(image_slice_thresh_contours)
			#center, radius = cv2.minEnclosingCircle(image_slice_thresh_contours)
			#center = map(int, center)
			#radius = int(radius)
			#center = (center[1] + row_start, center[0] + column_start)
			#cv2.circle(light_circles, (center[1], center[0]), radius + 3, WHITE, 3)
			#centers[i] = center
			#radii[i] = radius

			#Find the best fit for the largest circle
			radius = int(image_slice.shape[0]/2)
			first_time = True
			max_val = 0
			circle_area = 0
			max_loc = (0, 0)
			while radius > 0:
				last_radius = radius
				last_max_loc = max_loc
				last_max_val = max_val
				last_circle_area = circle_area

				circle_template = numpy.zeros((radius*2+1, radius*2+1), type(image_slice[0][0]))
				cv2.circle(circle_template, (radius, radius), radius, WHITE, -1)
				res = cv2.matchTemplate(image_slice, circle_template, cv2.TM_CCORR)
				min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
				circle_area = math.pi*math.pow(radius,2)
				#Continue to decrease the circle size until more than 10% of the remaining pixels 
				#print('{} {}'.format(max_val, last_max_val))
				if first_time or max_val > last_max_val*((.4*circle_area+.6*last_circle_area)/last_circle_area):
					first_time = False
					radius = radius-1
				else:
					#print('GOT HERE')
					radii[i] = last_radius
					centers[i] = (row_start + last_max_loc[1] + last_radius + 1, column_start + last_max_loc[0] + last_radius + 1)
					cv2.circle(light_circles, (centers[i][1], centers[i][0]), radius + 5, WHITE, 3)
					break

			# Temporary hack put in place to improve demo reliability. Remove.
			#if radii[i] <= 33:
			#	logger.debug("WARN: HACK")
			#	raise NotImplementedError("hack")

			if debug:
				pylab.subplot(number_of_transmitters,2,2*i+2)
				pylab.plot(f, Y_plot)
				pylab.title(str(centers[i]), size='xx-small')
				#pylab.xlabel('Frequency (Hz)')
				pylab.xlim([0,16000])
				pylab.tick_params(labelsize=4)

			peaks = scipy.signal.argrelmax(Y_plot)[0]
			logger.debug2('peaks =\n{}'.format(peaks))
			logger.debug2('f[peaks] =\n{}'.format(f[peaks]))
			logger.debug2('Y_plot[peaks] =\n{}'.format(Y_plot[peaks]))

			idx = numpy.argmax(Y_plot[peaks])
			peak_freq = f[peaks[idx]]

			logger.debug('center {}\tradius {}\tpeak_freq = {}'.format(centers[i], radii[i], peak_freq))
			if debug:
				cv2.circle(contours_kept_image,
						(centers[i][1], centers[i][0]),
						5,
						GREEN,
						-1)
				cv2.circle(contours_kept_image,
						(centers[i][1], centers[i][0]),
						radius + 5,
						GREEN,
						2)
				cv2.putText(
						contours_kept_image,
						"({} {}) {} Hz".format(
							centers[i][1],
							centers[i][0],
							int(peak_freq)),
						(centers[i][1]+100, centers[i][0]),
						cv2.FONT_HERSHEY_TRIPLEX,
						2,
						YELLOW)

			estimated_frequencies.append(peak_freq)
		except:
			logger.debug("Dropped failed center at {}".format(centers[i]))
			estimated_frequencies.append(10)

	if debug:
		dbg_plot_subplots('freq_fft_transmitters')
		dbg_save('contours-kept-labeled', contours_kept_image)
		dbg_save('circles', light_circles)

	logger.end_op()

	centers = numpy.array(centers)
	radii = numpy.array(radii)
	estimated_frequencies = numpy.array(estimated_frequencies)

	return (centers, radii, estimated_frequencies, gray_image.shape)
