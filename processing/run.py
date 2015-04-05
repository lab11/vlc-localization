#!/usr/bin/env python2
# vim: sts=4 ts=4 sw=4 noet:

from __future__ import print_function
import sys
import os
import argparse

import numpy as np

import pretty_logger
logger = pretty_logger.get_logger()

def dist(c1, c2):
	return ( (c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2 )**.5

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
			formatter_class=argparse.RawDescriptionHelpFormatter,
			description='Program Action: Run image processing',
			epilog='''\
Control debug level with DEBUG evinronment environment variable.
  Default: no debugging
  DEBUG=1: print debugging information
  DEBUG=2: print lots of debugging information

  QUIET=1: Suppress most output (supersedes DEBUG)

  PICS=1:  Save intermediate images (slow)
''')
	parser.add_argument('-f', '--filename', type=str,
			default='./samples/x_0_y_1.27.jpg',
			help='image to process')
	parser.add_argument('-l', '--actual-location', type=str,
			help='actual location in space, formatted as "x, y, z"')
	parser.add_argument('-c', '--camera', type=str,
			default='lumia_1020',
			help='phone type; must be in phones/')
	parser.add_argument('-m', '--method', type=str,
			default='opencv_fft',
			help='image processing method; must be in processors/')
	parser.add_argument('-k', '--k-val-method', type=str,
			help='Override k-val guess method (useful with -l)')
	parser.add_argument('-r', '--room', type=str,
			default='test_rig',
			help='room the image was taken in; must be in rooms/')
	parser.add_argument('--only-image', action='store_true',
			help='stop after image processing (do not attempt localization)')
	parser.add_argument('-b','--box',action='store_true',
			help='Box light handleing')

	args = parser.parse_args()

	np.set_printoptions(suppress=True)

	if args.actual_location:
		if ',' in args.actual_location:
			args.actual_location = np.array(map(float, args.actual_location.split(',')))
		else:
			args.actual_location = np.array(map(float, args.actual_location.split()))
	else:
		try:
			f = os.path.basename(args.filename)[:-4].split('_')
			if len(f) == 4:
				if f[0] == 'x' and f[2] == 'y':
					args.actual_location = np.array([float(f[1]), float(f[3]), 0])
			if len(f) == 6:
				if f[0] == 'x' and f[2] == 'y' and f[4] == 'z':
					args.actual_location = np.array([float(f[1]), float(f[3]), float(f[5])])
		except IndexError:
			pass

	try:
		#from phones import args.camera.split('-')[0] as phone
		phone = __import__('phones.' + args.camera.split('-')[0], fromlist=[1,])
	except ImportError:
		logger.error("Unknown phone: {}".format(args.camera.split('-')[0]))
		raise
	try:
		camera = getattr(phone, args.camera.split('-')[1])
	except IndexError:
		# A camera was not specified, use the default (elem 0) for this phone
		camera = phone.cameras[0]
	except AttributeError:
		# Found the phone, but not the specified camera
		logger.error("Unknown phone / camera combination")
		raise
	try:
		imag_proc = __import__('processors.' + args.method, fromlist=[1,]).imag_proc
	except ImportError:
		logger.error('Unknown image processing backend.')
		raise

	if args.only_image:
		try:
			centers, radii, estimated_frequencies, shape = imag_proc(
					args.filename,
					0,
					camera,
					)
			for c,r,f in zip(centers, radii, estimated_frequencies):
				logger.info('{}: {} pixel radius. Freq {}'.format(c, r, f))
			logger.info('shape = {}'.format(shape))
		except Exception as e:
			logger.warn('Exception: {}'.format(e))
			raise
	else:
		from aoa_full import aoa_full

		try:
			room = __import__('rooms.' + args.room, fromlist=[1,])
		except ImportError:
			logger.error('Unknown room')
			raise
		try:
			rx_location, rx_rotation, location_error = aoa_full(
					args.filename,
					camera, room,
					imag_proc,
					actual_location=args.actual_location,
					k_val_method=args.k_val_method,
					)
			logger.info('rx_location = {}'.format(rx_location))
			if args.actual_location is not None:
				logger.info(' rx_loc_err = {}'.format(
					map(abs, rx_location - args.actual_location)))
				logger.info('x, y, z err = {} {}'.format(
					dist(rx_location, args.actual_location),
					room.units))
				rx_location[2] = 0
				args.actual_location[2] = 0
				logger.info('   x, y err = {} {}'.format(
					dist(rx_location, args.actual_location),
					room.units))
			logger.info('rx_rotation =\n{}'.format(rx_rotation))
		except Exception as e:
			logger.warn('Exception: {}'.format(e))
			raise
