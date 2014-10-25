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
	pylab.savefig(fname, dpi=1200)
	logger.debug('Plotted WIP subplots to {}'.format(fname))
	logger.end_op()

@logger.op("Process image {0} with {1} transmitter(s) taken with {2.__name__}")
def imag_proc(file_name, num_of_tx, camera, debug):
	BLACK  = (  0,   0,   0)
	WHITE  = (255, 255, 255)
	BLUE   = (255,   0,   0)
	GREEN  = (  0, 255,   0)
	RED    = (  0,   0, 255)
	YELLOW = (  0, 255, 255)
	TEAL   = (255, 255,   0)
	MAGENTA= (255,   0, 255)

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
		dbg_save('/tmp/contours_on_gray.png', contour_image)
		contour_blur_image = m2.copy()
		cv2.drawContours(contour_blur_image, contours, -1, 255, 3)
		dbg_save('/tmp/contours_on_blur.png', contour_blur_image)
		dim = (gray_image.shape[0], gray_image.shape[1], 3)
		blank_image = numpy.zeros(dim, numpy.uint8)
		cv2.drawContours(blank_image, contours, -1, WHITE, 3)
		dbg_save('/tmp/contours_only.png', blank_image)

	# And then fitting a circle to that contour
	centers = []
	radii = []
	freqs = []
	cnt = 0
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

		logger.start_op('light #{}'.format(cnt))
		centers.append(center)
		radii.append(radius)

		if False: #debug:
			px_scale = max(1, int(round(.05*radius)))
			cv2.circle(blank_image, center, px_scale, YELLOW, -1)
			cv2.circle(blank_image, center, radius, YELLOW, 3)
			dbg_save('/tmp/counters_with_center_and_circle.png', blank_image)
			gray_circle = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
			cv2.circle(gray_circle, center, px_scale, TEAL, -1)
			cv2.circle(gray_circle, center, radius, TEAL, 3)
			dbg_save('/tmp/orig_with_circle.png', gray_circle)

		r = radius + 30
		x1 = max(0, center[0]-r)
		x2 = min(gray_image.shape[0], center[0]+r+1)
		y1 = max(0, center[1]-r)
		y2 = min(gray_image.shape[1], center[1]+r+1)
		one_light = gray_image[x1:x2, y1:y2]
		if debug:
			dbg_save('/tmp/one-{}_light.png'.format(cnt), one_light)

		def image_to_impulses(factor):
			blur_width = int(factor*radius)+1

			one_blur = cv2.blur(one_light, (blur_width, radius))
			one_threshold, one_thresholded_img =\
					cv2.threshold(one_blur, 0, 255, cv2.THRESH_TOZERO+cv2.THRESH_OTSU)
			logger.debug("otsu threshold for {} = {}".format(cnt, one_threshold))

			#adapt_kernel_size = blur_width * 20 + 1
			#one_adapt = cv2.adaptiveThreshold(one_blur, 255,
			#		cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
			#		adapt_kernel_size, 0)

			ratio = 3
			kernel_size = round(int(.1*radius))+1
			lowThreshold = one_threshold / 5
			highThreshold = one_threshold
			logger.debug('Light {} running Canny with low {} high {} kernel {}'.\
					format(cnt, lowThreshold, highThreshold, kernel_size))
			post_canny = cv2.Canny(one_blur, lowThreshold, highThreshold, kernel_size)

			if debug:
				dbg_save('/tmp/one-{}_blur.png'.format(cnt), one_blur)
				dbg_save('/tmp/one-{}_thres.png'.format(cnt), one_thresholded_img)
				#dbg_save('/tmp/one-{}_adapt.png'.format(cnt), one_adapt)
				dbg_save('/tmp/one-{}_canny.png'.format(cnt), cv2.add(one_light, post_canny))

			vals = numpy.sum(post_canny, axis=0)

			v_idx = -1
			tot = 0
			div = 0
			impulses = []
			while v_idx < len(vals)-1:
				v_idx += 1
				if vals[v_idx] < (.3 * max(vals)):
					continue
				while vals[v_idx] > (.3 * max(vals)):
					tot += v_idx * vals[v_idx]
					div += vals[v_idx]
					v_idx += 1
				try:
					impulses.append(float(tot) / div)
				except ZeroDivisionError:
					pass
				tot = 0
				div = 0

			return impulses, one_threshold

		base_factor = 1.0 / radius
		impulses, one_threshold = image_to_impulses(base_factor)

		logger.debug(impulses)
		if len(impulses) < 4:
			logger.info("Not enough impulses. Trying finer blur")
			impulses, one_threshold = image_to_impulses(.1*base_factor)
			if len(impulses) < 4:
				logger.warn("Not enough impulses to decode light #{}, skipping".\
					format(cnt))
				centers.pop()
				radii.pop()
				cnt += 1
				logger.end_op()
				continue

		if debug:
			scale_target = 2500
			scale = scale_target / one_light.shape[0]
			scale_thickness = max(1, scale / 2)
			logger.start_op('Scaling {} by {} to 2500 x-pixels'.format(
				one_light.shape, scale))
			one_impulse_img = cv2.resize(one_light, (0,0), fx=scale, fy=scale)
			one_impulse_img = cv2.cvtColor(one_impulse_img, cv2.COLOR_GRAY2BGR)
			logger.end_op()

		def get_intervals(imps):
			ivals = []
			for i1,i2 in zip(imps[:-1], imps[1:]):
				ivals.append(i2-i1)
			return ivals

		def get_light_over_range(p1, p2, offset):
			p1 = int(round(p1))
			p2 = int(round(p2))
			p1_25 = p1 + (p2-p1)/4
			p2_75 = p2 - (p2-p1)/4
			ret = sum(one_light[one_light.shape[0]/2 + offset][p1_25:p2_75]) / (p2_75-p1_25)
			logger.debug('light val for pts {}--{} offset {} measured over range {}--{}: {}'.\
					format(p1, p2, offset, p1_25, p2_75, ret))
			return ret

		def is_range_lit(p1, p2):
			votes = 0
			for offset in (-radius/3, 0, radius/3):
				if get_light_over_range(p1, p2, offset) > one_threshold:
					votes += 1
			is_lit = votes >= 2
			logger.debug('range between {}--{} is lit: {}'.\
					format(p1, p2, is_lit))
			return is_lit

		@logger.debug_op('remove_impulse')
		def remove_impulse():
			# Algo assumes first and last impulse always valid
			last = is_range_lit(impulses[0], impulses[1])
			for z in xrange(1, len(impulses)-1):
				if debug:
					pt1 = (int(round(impulses[z]*scale)), 0)
					pt2 = (int(round(impulses[z]*scale)), one_impulse_img.shape[1])

				cur = is_range_lit(impulses[z], impulses[z+1])
				#if last < one_threshold and cur < one_threshold:
				#	logger.debug('impuluses {} -- {} -- {} all dark, dropping middle'.\
				#					format(impulses[z-1], impulses[z], impulses[z+1]))
				#	cv2.line(one_impulse_img, pt1, pt2, RED, thickness=scale_thickness)
				#	impulses.pop(z)
				#	return
				if last and cur:
					logger.debug('impuluses {} -- {} -- {} all light, dropping middle'.\
									format(impulses[z-1], impulses[z], impulses[z+1]))
					if debug:
						cv2.line(one_impulse_img, pt1, pt2, RED, thickness=scale_thickness)
					impulses.pop(z)
					return True
				last = cur
			logger.debug("No more bad impulses found")
			return False

		while remove_impulse():
			pass
		logger.debug('imuplses = {}'.format(impulses))

		intervals = get_intervals(impulses)
		logger.debug('intervals = {}'.format(intervals))

		if debug:
			for impulse in impulses:
				pt1 = (int(round(impulse*scale)), 0)
				pt2 = (int(round(impulse*scale)), one_impulse_img.shape[1])
				cv2.line(one_impulse_img, pt1, pt2, TEAL, thickness=scale_thickness)
			for dist in (0, -(radius*scale)/3, (radius*scale)/3):
				pt1 = (0, one_impulse_img.shape[1]/2 + dist)
				pt2 = (one_impulse_img.shape[0], one_impulse_img.shape[1]/2 + dist)
				cv2.line(one_impulse_img, pt1, pt2, YELLOW, thickness=scale_thickness/3)

		# Try to detect missing edges
		def add_missing_edge(x0, x1, target):
			assert impulses == sorted(impulses), "impulses not sorted?"
			my_range = x1 - x0
			num_missing = int(round(my_range / est_mean))
			logger.debug('add missing between {}--{}, num_missing = {} = {} / {}'.\
					format(x0, x1, num_missing, my_range, est_mean))
			incr = my_range / num_missing
			for p in xrange(1, num_missing):
				new_p = x0 + p*incr
				logger.debug('adding edge at {}'.format(new_p))
				impulses.append(new_p)
				if debug:
					pt1 = (int(round(new_p * scale)), 0)
					pt2 = (int(round(new_p * scale)), one_impulse_img.shape[1]/2)
					cv2.line(one_impulse_img, pt1, pt2, GREEN, thickness=scale_thickness)
			impulses.sort()
			return num_missing - 1

		intervals = numpy.array(intervals)
		outliers = intervals > (numpy.mean(intervals) + 2*numpy.std(intervals))
		masked_intervals = numpy.ma.array(intervals, mask = outliers)
		est_mean = numpy.mean(masked_intervals)
		too_wide = numpy.nonzero(outliers)[0]
		idx_offset = 0
		for idx in too_wide:
			idx_offset += add_missing_edge(
					impulses[idx+idx_offset], impulses[idx+idx_offset+1], est_mean)

		intervals = numpy.array(intervals)
		outliers = intervals < (numpy.mean(intervals) - 2*numpy.std(intervals))
		masked_intervals = numpy.ma.array(intervals, mask = outliers)
		est_mean = numpy.mean(masked_intervals)
		too_skinny = numpy.nonzero(outliers)[0]
		idx_offset = 0
		for idx in too_skinny:
			if debug:
				pt1 = (int(round(impulses[idx] * scale)), one_impulse_img.shape[1]/2)
				pt2 = (int(round(impulses[idx] * scale)), one_impulse_img.shape[1])
				cv2.line(one_impulse_img, pt1, pt2, MAGENTA, thickness=scale_thickness)
			impulses.pop(idx + idx_offset)
			idx_offset -= 1

		if debug:
			dbg_save('/tmp/one-{}_impulses.png'.format(cnt), one_impulse_img)

		intervals = get_intervals(impulses)
		logger.debug('intervals = {}'.format(intervals))
		half_period = numpy.mean(intervals)
		logger.debug('half_period = {}'.format(half_period))

		freq = (1/camera.rolling_shutter_r) / (2*half_period)

		if (freq < 900):
			logger.info("Rejecting impossibly low frequency {} Hz".format(freq))
			centers.pop()
			radii.pop()
		else:
			freqs.append(freq)

		cnt += 1
		logger.end_op()

	centers = numpy.array(centers)

	for l in xrange(len(centers)):
		logger.debug('light at {} with radius {} estimated freq = {}'.format(
			centers[l], radii[l], freqs[l]))
	logger.end_op()
	return (centers, radii, freqs, gray_image.shape)

	'''
	number_of_transmitters = len(centers)
	#assert number_of_transmitters >= 3, 'not enough transmitters'
	logger.end_op()


	# Compute transmitter frequencies
	logger.start_op("Computing transmitter frequencies")

	Fs = 1/camera.rolling_shutter_r
	T = 1/Fs
	NFFT = 1024
	gain = 5

	estimated_frequencies = []
	window_size = 100

	for i in xrange(number_of_transmitters):
		image_row = gray_image[centers[i][0]]
		if (centers[i][1] - window_size) < 1:
			sig = image_row[0:centers[i][1]+window_size+1]
		elif (centers[i][1]+window_size) > min(gray_image.shape):
			sig = image_row[centers[i][1]-window_size:min(gray_image.shape)]
		else:
			sig = image_row[centers[i][1]-window_size:centers[i][1]+window_size+1]

		#y = sig
		y = vals_arr[i]
		window_size = len(y) / 2

		if debug:
			pylab.subplot(number_of_transmitters,2,2*i-1)
			pylab.plot(range(-window_size, window_size+1), y)
			pylab.xlabel('Pixel x-coordinate offset from center')
			pylab.ylabel('Intensity (8-bit gray)')
			pylab.plot((-window_size, window_size), (255, 255),
					'--', color='red', markersize=5)
			pylab.annotate('Saturation\n', (-80, 255),
					color='red', size='large')

		L = len(y)
		t = numpy.arange(0,L) * T
		Y = numpy.fft.fft(y* gain, NFFT) / float(L)
		f = Fs/2 * numpy.linspace(0,1,NFFT/2.0+1)
		Y_plot = 2*abs(Y[0:NFFT/2.0+1])

		peaks = scipy.signal.argrelmax(Y_plot)[0]
		#logger.debug('peaks =\n{}'.format(peaks))
		#logger.debug('f[peaks] =\n{}'.format(f[peaks]))
		#logger.debug('Y_plot[peaks] =\n{}'.format(Y_plot[peaks]))

		idx = numpy.argmax(Y_plot[peaks])
		peak_freq = f[peaks[idx]] / 2

		logger.debug('center {} peak_freq = {}'.format(centers[i], peak_freq))

		estimated_frequencies.append(peak_freq)

		if debug:
			pylab.subplot(number_of_transmitters,2,2*i)
			pylab.plot(f, Y_plot)
			#pylab.title(str(centers[i]))
			#pylab.xlabel('Frequency (Hz)')
			pylab.xlim([0,15000])
			pylab.axvline(x=peak_freq*2, ls='--', color='black')
			pylab.annotate(' {} Hz'.format(int(round(peak_freq*2))),
					(peak_freq*2, .8*max(Y_plot)), size='large')

	if debug:
		dbg_plot_subplots('/tmp/freq_fft_transmitters.png')
		dbg_plot_subplots('/tmp/freq_fft_transmitters.eps')

	logger.debug('estimated_frequencies = {}'.format(estimated_frequencies))
	logger.end_op()

	return (centers, estimated_frequencies, gray_image.shape)
	'''
