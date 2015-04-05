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
	debug = True
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

	if debug:
		global dbg_step
		dbg_step = 0

	# Load image and convert to grayscale
	logger.start_op("Loading image")
	gray_image = cv2.imread(file_name)
	logger.end_op()

	# Handle orientation
	logger.start_op("Normalizing image rotation")
	if gray_image.shape[1] > gray_image.shape[0]:
		logger.debug("Rotated image")
		gray_image = numpy.rot90(gray_image, 3)
	else:
		logger.debug("No rotation")
	logger.end_op()

	if debug:
		contours_kept_image = gray_image.copy()

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

		dbg_save('circle-point', contours_kept_image)

	raise NotImplementedError

	return ([], [], [], gray_image.shape)
