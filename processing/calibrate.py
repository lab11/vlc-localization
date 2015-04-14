#!/usr/bin/env python
# vim: sts=4 ts=4 sw=4 noet:

from __future__ import print_function
import sys, os
import math
import glob
import argparse

import numpy
np = numpy

from aoa import aoa

import pretty_logger
logger = pretty_logger.get_logger()

def dist(c1, c2):
	return ( (c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 - (c1[2] - c2[2])**2)**.5

def cround(x, base):
	return base * round(float(x)/base)

@logger.op("Calibrate {1} Hz light at {0} px at height {4} m")
def calibrate_light(px_pos, freq, z_f, correction, z_val):
	z_f = float(z_f)

	atan_x = math.atan2(px_pos[0], z_f)
	logger.debug('          atan(x): {:0.4f}\t({:0.4f} deg)'.format(atan_x, math.degrees(atan_x)))
	atan_x += correction['x']
	logger.debug('corrected atan(x): {:0.4f}\t({:0.4f} deg)'.format(atan_x, math.degrees(atan_x)))

	atan_y = math.atan2(px_pos[1], z_f)
	logger.debug('          atan(y): {:0.4f}\t({:0.4f} deg)'.format(atan_y, math.degrees(atan_y)))
	atan_y += correction['y']
	logger.debug('corrected atan(y): {:0.4f}\t({:0.4f} deg)'.format(atan_y, math.degrees(atan_y)))

	x = math.tan(atan_x) * z_val
	y = math.tan(atan_y) * z_val
	return x, y, z_val

@logger.op("Calibrate using image {0} taken with {2}::{3} facing {5} at {4}")
def calibrate(
		file_name, z_dict, gt,
		camera, cam_id, cam_pos, cam_orient, center_bulb,
		imag_proc,
		):
	raw_positions_of_lights, radii_of_lights, frequencies_of_lights, image_shape =\
			imag_proc(file_name, 0, camera)

	assert image_shape[0] > image_shape[1], "Processed image is not oriented correctly?"


	# Image is mirrored by the lens, need to reflect the image
	# Image origin is currently the top left but we want to center it
	center_point = tuple([p /2 for p in image_shape])
	positions_of_lights = np.zeros(raw_positions_of_lights.shape)
	positions_of_lights[:,0] = raw_positions_of_lights[:,1] - center_point[1]
	positions_of_lights[:,1] = center_point[0] - raw_positions_of_lights[:,0]

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


	# Debug
	logger.debug("Kept, normalized centers after rotation:")
	for i in range(len(frequencies_of_lights)):
		logger.debug('\t{}: {}'.format(
			frequencies_of_lights[i], positions_of_lights[i]))

	assert len(z_dict) >= len(positions_of_lights)


	locs = {}
	abs_locs = {}
	for i in range(len(positions_of_lights)):
		x, y, z = calibrate_light(
				positions_of_lights[i],
				frequencies_of_lights[i],
				camera.Zf,
				camera.correction[cam_id],
				z_dict[frequencies_of_lights[i]],
				)
		locs[frequencies_of_lights[i]] = (x, y, z)
		if cam_orient == '+x':
			# 90 deg rot left from -y, (-x, -y) rot90 (y, -x)
			abs_locs[frequencies_of_lights[i]] = (y + cam_pos[0], -x + cam_pos[1], z)
		elif cam_orient == '-x':
			# 90 deg rot left from +y, (x, y) rot90 (-y, x)
			abs_locs[frequencies_of_lights[i]] = (-y + cam_pos[0], x + cam_pos[1], z)
		elif cam_orient == '+y':
			abs_locs[frequencies_of_lights[i]] = (x + cam_pos[0], y + cam_pos[1], z)
		elif cam_orient == '-y':
			abs_locs[frequencies_of_lights[i]] = (-x + cam_pos[0], -y + cam_pos[1], z)
		else:
			assert False and 'Bad camera orientation: {}'.format(cam_orient)

		if center_bulb is not None:
			if frequencies_of_lights[i] == center_bulb:
				center_x_y = (x, y)

	if center_bulb is not None:
		for i in range(len(positions_of_lights)):
			locs[frequencies_of_lights[i]] = (
					locs[frequencies_of_lights[i]][0] - center_x_y[0],
					locs[frequencies_of_lights[i]][1] - center_x_y[1]
					)
			if cam_orient == '+x':
				abs_locs[frequencies_of_lights[i]] = (
						abs_locs[frequencies_of_lights[i]][0] - center_x_y[1],
						abs_locs[frequencies_of_lights[i]][1] + center_x_y[0]
						)
			elif cam_orient == '-x':
				abs_locs[frequencies_of_lights[i]] = (
						abs_locs[frequencies_of_lights[i]][0] + center_x_y[1],
						abs_locs[frequencies_of_lights[i]][1] - center_x_y[0]
						)
			elif cam_orient == '+y':
				abs_locs[frequencies_of_lights[i]] = (
						abs_locs[frequencies_of_lights[i]][0] - center_x_y[0],
						abs_locs[frequencies_of_lights[i]][1] - center_x_y[1]
						)
			elif cam_orient == '-y':
				abs_locs[frequencies_of_lights[i]] = (
						abs_locs[frequencies_of_lights[i]][0] + center_x_y[0],
						abs_locs[frequencies_of_lights[i]][1] + center_x_y[1]
						)

	return locs, abs_locs


def calibrate_from_files(fname, cal_f):
	fname = os.path.expanduser(fname)
	cal_f = os.path.expanduser(cal_f)

	z_vals = {}
	names = {}
	gt = {}
	center_bulb = None
	for l in open(cal_f):
		if len(l.strip()) == 0 or l[0] == '#':
			continue

		l = l.split()

		if l[0] == 'CAM_POS:':
			cam_pos = map(float, l[1:3])
			continue
		if l[0] == 'CAM_ID:':
			cam_id = l[1]
			continue
		if l[0] == 'CAM_ORIENT:':
			cam_orient = l[1]
			continue
		if l[0] == 'CENTER_BULB:':
			center_bulb = int(l[1])
			continue

		z_vals[int(l[1])] = float(l[2])
		names[int(l[1])] = l[0]
		try:
			gt[int(l[1])] = map(float, l[3:5])
		except KeyError:
			gt[int(l[1])] = None

	from phones.cameras import lumia_1020_back as camera
	from processors import opencv_fft

	locs, abs_locs = calibrate(
			fname, z_vals, gt,
			camera, cam_id, cam_pos, cam_orient, center_bulb,
			opencv_fft.imag_proc)

	return locs, abs_locs, names, gt


@logger.op('Averaging images in {0}')
def calibrate_from_directory(path):
	cal_f = os.path.join(path, 'cal.txt')
	if path[-1] != '/':
		path += '/'

	ret = {}
	abs_ret = {}
	for pic in glob.glob(path + '*.jpg'):
		locs, abs_locs, names, gt = calibrate_from_files(pic, cal_f)

		for f in sorted(locs):
			logger.info('{} Hz: {}'.format(f, map(lambda x: round(x, 3), locs[f])))

		for f in locs:
			if f not in ret:
				ret[f] = np.array(locs[f])
				abs_ret[f] = np.array(abs_locs[f])
			else:
				ret[f] = np.vstack((ret[f], locs[f]))
				abs_ret[f] = np.vstack((abs_ret[f], abs_locs[f]))

		if 'BULB_LIMIT' in os.environ:
			break

	return ret, abs_ret, names, gt


if __name__ == '__main__':
	if len(sys.argv) == 1:
		path = '~/Dropbox/benpat/research/vlc-data/calibration/bulb7/'
		path = os.path.expanduser(path)
		locs, abs_locs, names, gt = calibrate_from_directory(path)
	elif len(sys.argv) == 2:
		path = sys.argv[1]
		path = os.path.expanduser(path)
		locs, abs_locs, names, gt = calibrate_from_directory(path)
	elif len(sys.argv) == 3:
		path = sys.argv[1]
		path = os.path.expanduser(path)
		cal_f = sys.argv[2]
		cal_f = os.path.expanduser(cal_f)
		locs, abs_locs, names, gt = calibrate_from_files(path, cal_f)

	np.set_printoptions(suppress=True)
	for f in sorted(locs):
		print('Bulb {} ({} Hz):'.format(names[f], f))
		if len(locs[f].shape) > 1:
			logger.debug('{}'.format(locs[f]))
			print('{} (camera-relative)'.format(np.mean(locs[f], axis=0)))
			if gt[f]:
				print('{} (camera-relative error)'.format(
					np.mean(locs[f], axis=0) - gt[f]))
			logger.debug('{}'.format(abs_locs[f]))
			print('{} (global)'.format(np.mean(abs_locs[f], axis=0)))
		else:
			print(locs[f])
			print(abs_locs[f])

