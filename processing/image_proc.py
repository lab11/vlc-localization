#!/usr/bin/env python
# vim: sts=4 ts=4 sw=4 noet:

from __future__ import print_function
import sys
import os
import argparse

import pretty_logger
logger = pretty_logger.get_logger()

if __name__ == '__main__':
	logger.info('Starting standalone image processing')
	parser = argparse.ArgumentParser(
			formatter_class=argparse.RawDescriptionHelpFormatter,
			description='Program Action: Run image processing',
			epilog='''\
Control debug level with DEBUG evinronment environment variable.
  Default: no debugging
  DEBUG=1: print debugging information
  DEBUG=2: print debugging information and write out intermediate images to /tmp (slow)
''')
	parser.add_argument('filename', type=str, nargs='?',
			default='/tmp/x_0_y_1.27.jpg',
			help='image to process')
	parser.add_argument('phone_type', type=str, nargs='?',
			default='lumia_1020',
			help='phone type; must be in phones/')
	parser.add_argument('processor', type=str, nargs='?',
			default='opencv_fft',
			help='image processing backend; must be in processors/')

	args = parser.parse_args()

	logger.debug('Processing image {} phone type {}'.\
			format(args.filename, args.phone_type))

	try:
		if os.environ['DEBUG'] == '2':
			debug = True
		else:
			debug = False
	except KeyError:
		debug = False

	try:
		#from phones import args.phone_type.split('-')[0] as phone
		phone = __import__('phones.' + args.phone_type.split('-')[0], fromlist=[1,])
	except ImportError:
		logger.error("Unknown phone: {}".format(args.phone_type.split('-')[0]))
		raise
	try:
		camera = getattr(phone, args.phone_type.split('-')[1])
	except IndexError:
		# A camera was not specified, use the default (elem 0) for this phone
		camera = phone.cameras[0]
	except AttributeError:
		# Found the phone, but not the specified camera
		logger.error("Unknown phone / camera combination")
		raise

	try:
		imag_proc = __import__('processors.' + args.processor, fromlist=[1,]).imag_proc
		print(imag_proc)
	except ImportError:
		logger.error('Unknown image processing backend.')
		raise

	try:
		centers, radii, estimated_frequencies, shape =\
				imag_proc(args.filename, 0, camera, debug)
		for c,r,f in zip(centers, radii, estimated_frequencies):
			logger.info('{}: {} pixel radius. Freq {}'.format(c, r, f))
		logger.info('shape = {}'.format(shape))
	except Exception as e:
		logger.warn('Exception: {}'.format(e))
		raise
