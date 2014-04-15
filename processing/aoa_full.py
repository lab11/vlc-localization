#!/usr/bin/env python
# vim: sts=4 ts=4 sw=4 noet:

from __future__ import print_function
import sys, os
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

from imag_proc_opencv_fft import imag_proc
#from imag_proc_opencv import imag_proc
#from imag_proc import static_imag_proc as imag_proc
from aoa import aoa

import pretty_logger
logger = pretty_logger.get_logger()

@logger.op("Aoa full on image {0} taken with {1}")
def aoa_full(file_name, phone_type, debug):

	w = 28.0
	l = 29.0

	#position_of_transmitters = [-w/2*2.54 l/2*2.54 0; w/2*2.54 l/2*2.54 0; w/2*2.54 -l/2*2.54 0; -w/2*2.54 -l/2*2.54 0; 0 0 0];
	#frequency_of_transmitter = [2000; 2500; 3000; 3500; 4000];
	transmitters = {
			2000 : (-w/2*2.54,  l/2*2.54, 0),
			2500 : ( w/2*2.54,  l/2*2.54, 0),
			3000 : ( w/2*2.54, -l/2*2.54, 0),
			3500 : (-w/2*2.54, -l/2*2.54, 0),
			4000 : (        0,         0, 0),
			}
	frequencies = numpy.array(transmitters.keys())
	logger.debug("Transmitter frequencies = {}".format(frequencies))

	Zf_lumia = 5620;
	Zf_lumia_front = 1039;
	Zf_iphone = 2950;

	if phone_type == 'iphone':
		Zf = Zf_iphone
	elif phone_type == 'lumia':
		Zf = Zf_lumia
	elif phone_type == 'lumia-front':
		Zf = Zf_lumia_front
	else:
		raise NotImplementedError("Unknown phone type: {} (need to add Zf info to this script)".format(phone_type))

	positions_of_lights, radii_of_lights, frequencies_of_lights, image_shape =\
			imag_proc(file_name, 0, phone_type, debug)

	# Image is mirrored by the lens, need to reflect the image
	# Image origin is currently the top left but we want to center it
	assert image_shape[0] > image_shape[1], "Processed image is not oriented correctly?"
	center_point = tuple([p /2 for p in image_shape])
	positions_of_lights[:,0] = center_point[0] - positions_of_lights[:,0]
	positions_of_lights[:,1] = center_point[1] - positions_of_lights[:,1]
	logger.debug('Translated light center points: {}'.format(
		positions_of_lights), remove_newlines=True)

	# Convert the measured frequencies to the actual transmitted frequencies:
	actual_frequencies = [frequencies[(numpy.abs(frequencies - f)).argmin()] for
			f in frequencies_of_lights]
	logger.debug("Original frequencies: {}".format(frequencies_of_lights))
	logger.debug("  Actual frequencies: {}".format(actual_frequencies))
	del(frequencies_of_lights) # delete this so we don't accidentally use it

	if len(actual_frequencies) != len(numpy.unique(actual_frequencies)):
		logger.start_op('Removing duplicate transmitter entries')
		uniq_freq = numpy.unique(actual_frequencies)
		for freq in uniq_freq:
			matches = []
			for i in xrange(len(actual_frequencies)):
				if freq == actual_frequencies[i]:
					matches.append((i, positions_of_lights[i], radii_of_lights[i]))
			if len(matches) > 1:
				idxs, centers, radii = zip(*matches)
				logger.debug('Duplicate frequency {} --'\
						' idxs {} centers {} radii {}'.format(
							freq, idxs, centers, radii))
				logger.debug('pos = {}'.format(positions_of_lights))
				positions_of_lights = numpy.delete(positions_of_lights, idxs, axis=0)
				logger.debug('pos = {}'.format(positions_of_lights))
				logger.debug('rad = {}'.format(radii_of_lights))
				radii_of_lights = numpy.delete(radii_of_lights, idxs)
				logger.debug('rad = {}'.format(radii_of_lights))
				actual_frequencies = numpy.delete(actual_frequencies, idxs)
				best_idx = numpy.argmax(radii)
				logger.debug('pos = {}'.format(positions_of_lights))
				logger.debug('centers[{}] = {}'.format(best_idx, centers[best_idx]))
				positions_of_lights = numpy.vstack((positions_of_lights, centers[best_idx]))
				logger.debug('pos = {}'.format(positions_of_lights))
				radii_of_lights = numpy.append(radii_of_lights, radii[best_idx])
				actual_frequencies = numpy.append(actual_frequencies, freq)

		logger.debug('After duplicate removal:')
		for pos, rad, freq in zip(positions_of_lights, radii_of_lights, actual_frequencies):
			logger.debug('  {} with radius {}\t= {} Hz'.format(pos, rad, freq))
		logger.end_op()

	# Create pairs (light_position_on_image, transmitter_position)
	assert len(positions_of_lights) == len(actual_frequencies), "# of center points != # of frequencies?"
	lights = [
			(
				positions_of_lights[i],
				transmitters[actual_frequencies[i]]
			) for i in xrange(len(positions_of_lights))]
	logger.debug('Lights information: {}'.format(lights))

	# AoA calcualation requires at least 3 transmitters
	assert len(lights) >= 3, "AoA calcualation requires at least 3 transmitters"

	tries = 3
	tries_rx_loc = numpy.empty([tries, 3])
	tries_rx_rot = numpy.empty([tries, 3, 3])
	tries_rx_err = numpy.empty([tries])
	tries_method = ['YS_brute', 'static', 'scipy_basin']
	for i in xrange(tries):
		rx_location, rx_rotation, location_error = aoa(lights, Zf, k_init_method=tries_method[i])
		logger.info('location estimate = {}'.format(rx_location))
		logger.info('location error    = {}'.format(location_error))
		tries_rx_loc[i] = rx_location
		tries_rx_rot[i] = rx_rotation
		tries_rx_err[i] = location_error

		if location_error > 1:
			if i == tries - 1:
				min_err_idx = numpy.argmin(tries_rx_err)
				rx_location = tries_rx_loc[min_err_idx]
				rx_rotation = tries_rx_rot[min_err_idx]
				location_error = tries_rx_err[min_err_idx]
				
				logger.info('Error ({}) too high, but max tries exceeded'.format(location_error))
				logger.warn('Returning measurement with high error estimate')
			else:
				logger.info('Error ({}) too high, trying again'.format(location_error))
		else:
			break

	'''
	for k in xrange(len(lights)):
		aoa_lights = [lights[k]]
		r = range(len(lights))
		r.pop(k)
		for i in r:
			aoa_lights.append(lights[i])
		logger.info('aoa_lights = {}'.format(aoa_lights))
		rx_location, rx_rotation, location_error = aoa(aoa_lights, Zf)
		logger.info('location with brute  k_init = {}'.format(rx_location))
		logger.info('location error              = {}'.format(location_error))
	'''

	return (rx_location, rx_rotation, location_error)

if __name__ == '__main__':
	logger.info("aoa_full.py is main. Running aoa_full")
	parser = argparse.ArgumentParser(
			formatter_class=argparse.RawDescriptionHelpFormatter,
			description='Program Action: Run AoA full (image proc + AoA)',
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
			default='lumia',
			help='phone type; one of "iphone" "lumia" "lumia-front" "glass"')

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
		rx_location, rx_rotation, location_error = aoa_full(
				args.filename, args.phone_type, debug)
		logger.info('rx_location = {}'.format(rx_location))
		logger.info('rx_rotation =\n{}'.format(rx_rotation))
		logger.info('location_error = {}'.format(location_error))
	except Exception as e:
		logger.warn('Exception: {}'.format(e))
		raise
