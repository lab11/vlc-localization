#!/usr/bin/env python2
# vim: sts=4 ts=4 sw=4 noet:

from __future__ import print_function
import sys
import os
import argparse

import pretty_logger
logger = pretty_logger.get_logger()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
			formatter_class=argparse.RawDescriptionHelpFormatter,
			description='Program Action: Run image processing',
			epilog='''\
Control debug level with DEBUG evinronment environment variable.
  Default: no debugging
  DEBUG=1: print debugging information
  DEBUG=2: print debugging information and write out intermediate images to /tmp (slow)
''')
	parser.add_argument('-f', '--filename', type=str,
			default='./samples/x_0_y_1.27.jpg',
			help='image to process')
	parser.add_argument('-c', '--camera', type=str,
			default='lumia_1020',
			help='phone type; must be in phones/')
	parser.add_argument('-m', '--method', type=str,
			default='opencv_fft',
			help='image processing method; must be in processors/')
	parser.add_argument('-r', '--room', type=str,
			default='test_rig',
			help='room the image was taken in; must be in rooms/')
	parser.add_argument('--only-image', action='store_true',
			help='stop after image processing (do not attempt localization)')
	parser.add_argument('-b','--box',action='store_true',
			help='Box light handleing')

	args = parser.parse_args()

	try:
		if os.environ['DEBUG'] == '2':
			debug = True
		else:
			debug = False
	except KeyError:
		debug = False

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
			centers, radii, estimated_frequencies, shape =\
					imag_proc(args.filename, 0, camera, debug)
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
					args.filename, camera, room, imag_proc, debug)
			logger.info('rx_location = {}'.format(rx_location))
			logger.info('rx_rotation =\n{}'.format(rx_rotation))
			logger.info('location_error = {}'.format(location_error))
		except Exception as e:
			logger.warn('Exception: {}'.format(e))
			raise
