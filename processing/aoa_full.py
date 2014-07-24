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

from aoa import aoa

import pretty_logger
logger = pretty_logger.get_logger()

def dist(c1, c2):
	return ( (c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 - (c1[2] - c2[2])**2)**.5

def resolve_aliased_frequncies(lights):
	l,p = zip(*lights)
	def build_opts(s, p, r):
		if len(p) == 1:
			for e in p[0]:
				new_s = list(s)
				new_s.append(e)
				r.append(new_s)
		else:
			for i in range(len(p[0])):
				sub_s = list(s)
				sub_s.append(p[0][i])
				sub_p = list(p)
				sub_p.pop(0)
				build_opts(sub_s, sub_p, r)
	r = []
	build_opts([], p, r)

	best_dist = 1e12
	for coords in r:
		d = 0
		for i in range(len(coords)-1):
			for j in range(1, len(coords)):
				d += dist(coords[i], coords[j])
		if d < best_dist:
			best_dist = d
			best_coords = coords
	return zip(l, best_coords)

@logger.op("Aoa full on image {0} taken with {1} in {2}")
def aoa_full(file_name, camera, room, imag_proc, debug):
	frequencies = numpy.array(room.transmitters.keys())
	logger.debug("Transmitter frequencies = {}".format(frequencies))

	positions_of_lights, radii_of_lights, frequencies_of_lights, image_shape =\
			imag_proc(file_name, 0, camera, debug)
	print (frequencies_of_lights)
	assert image_shape[0] > image_shape[1], "Processed image is not oriented correctly?"
	# Image is mirrored by the lens, need to reflect the image
	if not hasattr(room, 'origin'):
		raise TypeError('Room object {} does not have an origin'.format(room))
	if room.origin == 'center':
		# Image origin is currently the top left but we want to center it
		center_point = tuple([p /2 for p in image_shape])
		positions_of_lights[:,0] = center_point[0] - positions_of_lights[:,0]
		positions_of_lights[:,1] = center_point[1] - positions_of_lights[:,1]
	elif room.origin == 'south-east':
		positions_of_lights[:,1] = -positions_of_lights[:,1]
	else:
		raise NotImplementedError('Unknown origin type: {}'.format(room.origin))
	logger.debug('Translated light center points: {}'.format(
		positions_of_lights), remove_newlines=True)
	# Convert the measured frequencies to the actual transmitted frequencies:
	actual_frequencies = [frequencies[(numpy.abs(frequencies - f)).argmin()] for
			f in frequencies_of_lights]
	logger.debug("Original frequencies: {}".format(frequencies_of_lights))
	logger.debug("  Actual frequencies: {}".format(actual_frequencies))
	del(frequencies_of_lights) # delete this so we don't accidentally use it
	print ("Frequencies: " + str(frequencies))
	print ("Actual Frequencies: " + str(actual_frequencies))
	if len(actual_frequencies) != len(numpy.unique(actual_frequencies)):
		logger.start_op('Removing duplicate transmitter entries')
		uniq_freq = numpy.unique(actual_frequencies)
		print ("Unique Frequencies: " + str(uniq_freq))
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
				room.transmitters[actual_frequencies[i]]
			) for i in xrange(len(positions_of_lights))]
	logger.debug('Raw lights information: {}'.format(lights))

	# Some frequencies have multiple locations, need to pick one
	lights = resolve_aliased_frequncies(lights)

	# AoA calcualation requires at least 3 transmitters
	assert len(lights) >= 3, "AoA calcualation requires at least 3 transmitters"

	tries = 3
	tries_rx_loc = numpy.empty([tries, 3])
	tries_rx_rot = numpy.empty([tries, 3, 3])
	tries_rx_err = numpy.empty([tries])
	tries_method = ['YS_brute', 'static', 'scipy_basin']
	for i in xrange(tries):
		rx_location, rx_rotation, location_error, valid = aoa(lights, camera.Zf, k_init_method=tries_method[i])
		if valid == False:
			location_error = 999999 #this is hardcoding an exit, i can do better...
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
		rx_location, rx_rotation, location_error = aoa(aoa_lights, camera.Zf)
		logger.info('location with brute  k_init = {}'.format(rx_location))
		logger.info('location error              = {}'.format(location_error))
	'''

	return (rx_location, rx_rotation, location_error)
