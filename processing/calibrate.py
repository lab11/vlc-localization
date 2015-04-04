#!/usr/bin/env python
# vim: sts=4 ts=4 sw=4 noet:

from __future__ import print_function
import sys, os
import math
import argparse

import numpy
import numpy.ma
import scipy
import scipy.misc
import scipy.ndimage
import scipy.signal
import scipy.cluster
import matplotlib
import matplotlib.mlab
import pylab

from aoa import aoa

import pretty_logger
logger = pretty_logger.get_logger()

def dist(c1, c2):
	return ( (c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 - (c1[2] - c2[2])**2)**.5

def cround(x, base):
	return base * round(float(x)/base)

@logger.op("Calibrate {1} Hz light at {0} px at height {3} m")
def calibrate_light(px_pos, freq, z_f, z_val):
	z_f = float(z_f)
	logger.debug('atan(x): {}'.format(math.degrees(math.atan(px_pos[0] / z_f))))
	logger.debug('atan(y): {}'.format(math.degrees(math.atan(px_pos[1] / z_f))))
	x = (px_pos[0] / z_f) * z_val
	y = (px_pos[1] / z_f) * z_val
	return x, y, z_val

@logger.op("Calibrate using image {0} taken with {1} in {2}")
def calibrate(file_name, z_dict, camera, cam_pos, imag_proc, debug):
	positions_of_lights, radii_of_lights, frequencies_of_lights, image_shape =\
			imag_proc(file_name, 0, camera, debug)

	assert image_shape[0] > image_shape[1], "Processed image is not oriented correctly?"


	# Image is mirrored by the lens, need to reflect the image
	# Image origin is currently the top left but we want to center it
	center_point = tuple([p /2 for p in image_shape])
	positions_of_lights[:,0] = center_point[0] - positions_of_lights[:,0]
	positions_of_lights[:,1] = center_point[1] - positions_of_lights[:,1]


	# Drop frequencies that are unreasonably low
	to_del = []
	for i in range(len(frequencies_of_lights)):
		if frequencies_of_lights[i] < 1250:
			logger.debug("Deleting light with freq too low: {}".format(frequencies_of_lights[i]))
			to_del.append(i)
	positions_of_lights = numpy.delete(positions_of_lights, to_del, axis=0)
	radii_of_lights = numpy.delete(radii_of_lights, to_del)
	frequencies_of_lights = numpy.delete(frequencies_of_lights, to_del)


	# Normalize frequency vals
	for i in range(len(frequencies_of_lights)):
		frequencies_of_lights[i] = cround(frequencies_of_lights[i], 50)


	assert len(z_dict) == len(positions_of_lights)


	locs = {}
	for i in range(len(positions_of_lights)):
		x, y, z = calibrate_light(
				positions_of_lights[i],
				frequencies_of_lights[i],
				camera.Zf,
				z_dict[frequencies_of_lights[i]],
				)
		locs[frequencies_of_lights[i]] = (x, y, z)

	return locs


def calibrate_from_files(fname, cal_f):
	fname = os.path.expanduser(fname)
	cal_f = os.path.expanduser(cal_f)

	z_vals = {}
	names = {}
	for l in open(cal_f):
		if len(l.strip()) == 0 or l[0] == '#':
			continue

		l = l.split()

		if l[0] == 'CAM_POS:':
			cam_pos = map(float, l[1:2])
			continue

		z_vals[int(l[1])] = float(l[2])
		names[int(l[1])] = l[0]

	from phones.cameras import lumia_1020_back as camera
	from processors import opencv_fft as imag_proc

	try:
		debug = int(os.environ['DEBUG']) >= 3
	except KeyError:
		debug = False

	locs = calibrate(fname, z_vals, camera, cam_pos, imag_proc.imag_proc, debug)

	return locs


if __name__ == '__main__':
	if len(sys.argv) == 1:
		fname = '~/Dropbox/benpat/research/vlc-data/calibration/bulb7/2013-05-24--23-29-33-08.jpg'
		cal_f = '~/Dropbox/benpat/research/vlc-data/calibration/bulb7/cal.txt'
	elif len(sys.argv) == 2:
		fname = sys.argv[1]
		cal_f = '/'.join(sys.argv[1].split('/')[:-1]) + '/cal.txt'
	else:
		fname = sys.argv[1]
		cal_f = sys.argv[2]

	locs = calibrate_from_files(fname, cal_f)

	for f in sorted(locs):
		print('{} Hz: {}'.format(f, map(lambda x: round(x, 3), locs[f])))

