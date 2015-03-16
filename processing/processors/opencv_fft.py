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

def dbg_save(fname, array):
	cv2.imwrite(fname, array)
	logger.debug('Saved WIP to {}'.format(fname))

def dbg_plot_subplots(fname):
	logger.start_op('plot_subplots for ' + fname)
	pylab.savefig(fname, dpi=300)
	logger.debug('Plotted WIP subplots to {}'.format(fname))
	logger.end_op()

@logger.op("Process image {0} with {1} transmitter(s) taken with {2}")
def imag_proc(file_name, num_of_tx, camera, debug):

	# Load image and convert to grayscale
	logger.start_op("Loading image")
	gray_image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
	logger.debug('gray_image.shape = {}'.format(gray_image.shape))
	if debug:
		dbg_save('/tmp/gray_image.png', gray_image)
	logger.end_op()

	# Handle orientation
	logger.start_op("Normalizing image rotation")
	if gray_image.shape[1] > gray_image.shape[0]:
		gray_image = numpy.rot90(gray_image, 3)
	if debug:
		dbg_save('/tmp/gray_image_rotated.png', gray_image)
	logger.debug('gray_image.shape = {}'.format(gray_image.shape))
	logger.end_op()

	# Blur image
	logger.start_op("Applying blur")
	#m2 = cv2.GaussianBlur(gray_image, (31,31), 0)
	m2 = cv2.blur(gray_image, (50,50)) # faster and good enough
	#m2 = cv2.blur(gray_image, (150,150)) # faster and good enough
	if debug:
		dbg_save('/tmp/after_blur.png', m2)
	logger.debug('m2.shape = {}'.format(m2.shape))
	logger.end_op()

	# Replace manual threshold with more efficient OTSU filter
	logger.start_op("Threshold image")
	threshold, thresholded_img = cv2.threshold(m2, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	if debug:
		dbg_save('/tmp/thresholded_img.png', thresholded_img)
	logger.end_op()

	# Find and label disjoint sets of pixels (each transmitter blob)
	logger.start_op("Locate transmitters")

	# opencv3.0 has a connectedComponents API but that's sadly not released yet
	#ret, markers = cv2.connectedComponents(thresholded_img)

	# We solve this by drawing an outline ("contour") around each blob
	contours, heirarchy = cv2.findContours(thresholded_img, cv2.RETR_LIST,
			cv2.CHAIN_APPROX_SIMPLE)
	logger.debug('heirarchy = {}'.format(heirarchy))

	if debug:
		# drawContours draws contours on the supplied image, need a copy
		contour_image = gray_image.copy()
		cv2.drawContours(contour_image, contours, -1, 255, 3)
		dbg_save('/tmp/contours.png', contour_image)

		contours_kept_image = gray_image.copy()

	# And then fitting a circle to that contour
	centers = []
	radii = []
	for contour in contours:
		center, radius = cv2.minEnclosingCircle(contour)
		center = map(int, center)
		radius = int(radius)
		if radius <= 5:
			logger.info('Skipping transmitter at {} with small radius ({} pixels)'.format(
				center, radius))
			continue
		# For some reason minEnclosingCircle flips x and y?
		center = (center[1], center[0])
		#assert thresholded_img[center[0], center[1]] == 1, 'Center of blob is not lit?'
		logger.debug('Transmitter at {}. Radius of {} pixels'.format(center, radius))

		contour_area = cv2.contourArea(contour)
		circle_area = math.pi * radius**2
		logger.debug('Transmitter area {}. Contour area {}. %age {}'.format(
			circle_area, contour_area, (contour_area / circle_area)*100 ))
		if (contour_area / circle_area) < .5:
			logger.info('Rejecting non-circular contour at {}'.format(center))
			continue
		centers.append(center)
		radii.append(radius)

		if debug:
			cv2.drawContours(contours_kept_image, [contour,], -1, 255, 3)

	if debug:
		dbg_save('/tmp/contours-kept.png', contours_kept_image)

	number_of_transmitters = len(centers)
	assert number_of_transmitters >= 3, 'not enough transmitters'
	logger.end_op()


	# Compute transmitter frequencies
	logger.start_op("Computing transmitter frequencies")

	Fs = 1/camera.rolling_shutter_r
	T = 1/Fs
	NFFT = 1024
	gain = 5

	estimated_frequencies = []
	window_size = 100

	average_window = 40;
	avg_threshold = 20;

	for i in xrange(number_of_transmitters):
		image_row = gray_image[centers[i][0]]
		'''
		if (centers[i][1] - window_size) < 1:
			sig = image_row[0:centers[i][1]+window_size+1]
		elif (centers[i][1]+window_size) > min(gray_image.shape):
			sig = image_row[centers[i][1]-window_size:min(gray_image.shape)]
		else:
			sig = image_row[centers[i][1]-window_size:centers[i][1]+window_size]

		y = sig
		'''
		if centers[i][1] > average_window:
			left_boundary = centers[i][1] - average_window
			while left_boundary > 1:
				sub_image_row = image_row[left_boundary:left_boundary+average_window-1]
				if (sum(sub_image_row)/len(sub_image_row)) < avg_threshold:
					break
				else:
					left_boundary -= 1
		else:
			left_boundary = 1
		
		if centers[i][1] + average_window < min(gray_image.shape):
			right_boundary = centers[i][1] + average_window
			while right_boundary < min(gray_image.shape):
				sub_image_row = image_row[right_boundary-average_window:right_boundary-1]
				if (sum(sub_image_row)/len(sub_image_row)) < avg_threshold:
					break
				else:
					right_boundary += 1
		else:
			right_boundary = min(gray_image.shape)
		y = image_row[left_boundary:right_boundary]
		

		if debug:
			pylab.subplot(number_of_transmitters,2,2*i-1)
			pylab.title(str(centers[i]), size='xx-small')
			pylab.ylim([0,260])
			pylab.yticks([0,127,255])
			pylab.tick_params(labelsize=4)
			pylab.plot(y)

		L = len(y)
		t = numpy.arange(0,L) * T
		Y = numpy.fft.fft(y* gain, NFFT) / float(L)
		f = Fs/2 * numpy.linspace(0,1,NFFT/2.0+1)
		Y_plot = 2*abs(Y[0:NFFT/2.0+1])

		if debug:
			pylab.subplot(number_of_transmitters,2,2*i)
			pylab.plot(f, Y_plot)
			pylab.title(str(centers[i]), size='xx-small')
			#pylab.xlabel('Frequency (Hz)')
			pylab.xlim([0,6000])
			pylab.tick_params(labelsize=4)

		peaks = scipy.signal.argrelmax(Y_plot)[0]
		#logger.debug('peaks =\n{}'.format(peaks))
		#logger.debug('f[peaks] =\n{}'.format(f[peaks]))
		#logger.debug('Y_plot[peaks] =\n{}'.format(Y_plot[peaks]))

		idx = numpy.argmax(Y_plot[peaks])
		peak_freq = f[peaks[idx]]

		logger.debug('center {} peak_freq = {}'.format(centers[i], peak_freq))
		if debug:
			cv2.putText(
					contours_kept_image,
					"{} {} Hz".format(centers[i], int(peak_freq)),
					(centers[i][1]+100, centers[i][0]),
					cv2.FONT_HERSHEY_TRIPLEX,
					2,
					255)

		estimated_frequencies.append(peak_freq)

	if debug:
		dbg_plot_subplots('/tmp/freq_fft_transmitters.png')
		dbg_save('/tmp/contours-kept-labeled.png', contours_kept_image)

	logger.debug('estimated_frequencies = {}'.format(estimated_frequencies))
	logger.end_op()

	centers = numpy.array(centers)
	radii = numpy.array(radii)
	estimated_frequencies = numpy.array(estimated_frequencies)

	return (centers, radii, estimated_frequencies, gray_image.shape)
