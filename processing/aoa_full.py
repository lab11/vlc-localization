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
	return ( (c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2 )**.5

def cround(x, base):
	return base * round(float(x)/base)

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
def aoa_full(file_name, camera, room, imag_proc,
		actual_location=None, k_val_method=None):
	frequencies = numpy.array(room.transmitters.keys())

	positions_of_lights, radii_of_lights, frequencies_of_lights, image_shape =\
			imag_proc(file_name, 0, camera)

	assert image_shape[0] > image_shape[1], "Processed image is not oriented correctly?"
	# Image is mirrored by the lens, need to reflect the image

	assert len(positions_of_lights) == len(radii_of_lights)
	assert len(radii_of_lights) == len(frequencies_of_lights)

	# Image origin is currently the top left but we want to center it, the AoA
	# processing assumes that (0, 0, 0) in the receiver coordinate system is at
	# the center of the lens
	center_point = tuple([p /2 for p in image_shape])
	positions_of_lights[:,0] = center_point[0] - positions_of_lights[:,0]
	positions_of_lights[:,1] = center_point[1] - positions_of_lights[:,1]

	# 90
	# positions_of_lights[:,0] = -(center_point[1] - positions_of_lights[:,1])
	# positions_of_lights[:,1] = center_point[0] - positions_of_lights[:,0]

	# -90
	# positions_of_lights[:,0] = center_point[1] - positions_of_lights[:,1]
	# positions_of_lights[:,1] = -(center_point[0] - positions_of_lights[:,0])

	logger.debug2('Translated light center points: {}'.format(
		positions_of_lights), remove_newlines=True)


	last_f = None
	min_freq_diff = 10000
	for f in sorted(room.transmitters):
		if last_f is None:
			last_f = f
			continue
		min_freq_diff = min(min_freq_diff, f-last_f)
		last_f = f
	del(last_f)


	# Lock frequencies
	actual_frequencies = [
			cround(f, min_freq_diff)
			for f in frequencies_of_lights
			]
	del(frequencies_of_lights) # delete this so we don't accidentally use it
	del(min_freq_diff)


	assert len(positions_of_lights) == len(radii_of_lights)
	assert len(radii_of_lights) == len(actual_frequencies)


	# Drop unknown frequencies
	to_del = []
	for i in range(len(actual_frequencies)):
		if actual_frequencies[i] not in room.transmitters:
			logger.debug2("Deleting light with unknown freq: {}".format(actual_frequencies[i]))
			to_del.append(i)
	positions_of_lights = numpy.delete(positions_of_lights, to_del, axis=0)
	radii_of_lights = numpy.delete(radii_of_lights, to_del)
	actual_frequencies = numpy.delete(actual_frequencies, to_del)


	assert len(positions_of_lights) == len(radii_of_lights)
	assert len(radii_of_lights) == len(actual_frequencies)


	# Delete duplicate frequencies
	to_del = []
	dups = {}
	for i in range(len(actual_frequencies)):
		if actual_frequencies[i] in dups:
			logger.debug("Deleting dup freq entry {}".format(actual_frequencies[i]))
			to_del.append(i)
			# Check if close by?
			l1 = positions_of_lights[i]
			l2 = positions_of_lights[dups[actual_frequencies[i]]]
			if (l1[0] - l2[0])**2 + (l1[0] - l2[0])**2 > 100**2:
				logger.debug("Remove orig too, far away")
				to_del.append(dups[actual_frequencies[i]])
			else:
				logger.debug("keep orig")
		else:
			dups[actual_frequencies[i]] = i
	positions_of_lights = numpy.delete(positions_of_lights, to_del, axis=0)
	radii_of_lights = numpy.delete(radii_of_lights, to_del)
	actual_frequencies = numpy.delete(actual_frequencies, to_del)


	assert len(positions_of_lights) == len(radii_of_lights)
	assert len(radii_of_lights) == len(actual_frequencies)


	# if len(actual_frequencies) != len(numpy.unique(actual_frequencies)):
	# 	logger.start_op('Removing duplicate transmitter entries')
	# 	uniq_freq = numpy.unique(actual_frequencies)
	# 	for freq in uniq_freq:
	# 		matches = []
	# 		for i in xrange(len(actual_frequencies)):
	# 			if freq == actual_frequencies[i]:
	# 				matches.append((i, positions_of_lights[i], radii_of_lights[i]))
	# 		if len(matches) > 1:
	# 			idxs, centers, radii = zip(*matches)
	# 			logger.debug('Duplicate frequency {} --'\
	# 					' idxs {} centers {} radii {}'.format(
	# 						freq, idxs, centers, radii))
	# 			logger.debug('pos = {}'.format(positions_of_lights))
	# 			positions_of_lights = numpy.delete(positions_of_lights, idxs, axis=0)
	# 			logger.debug('pos = {}'.format(positions_of_lights))
	# 			logger.debug('rad = {}'.format(radii_of_lights))
	# 			radii_of_lights = numpy.delete(radii_of_lights, idxs)
	# 			logger.debug('rad = {}'.format(radii_of_lights))
	# 			actual_frequencies = numpy.delete(actual_frequencies, idxs)
	# 			best_idx = numpy.argmax(radii)
	# 			logger.debug('pos = {}'.format(positions_of_lights))
	# 			logger.debug('centers[{}] = {}'.format(best_idx, centers[best_idx]))
	# 			positions_of_lights = numpy.vstack((positions_of_lights, centers[best_idx]))
	# 			logger.debug('pos = {}'.format(positions_of_lights))
	# 			radii_of_lights = numpy.append(radii_of_lights, radii[best_idx])
	# 			actual_frequencies = numpy.append(actual_frequencies, freq)

	# 	logger.debug('After duplicate removal:')
	# 	for pos, rad, freq in zip(positions_of_lights, radii_of_lights, actual_frequencies):
	# 		logger.debug('  {} with radius {}\t= {} Hz'.format(pos, rad, freq))
	# 	logger.end_op()

	# Create pairs (light_position_on_image, transmitter_position)
	assert len(positions_of_lights) == len(actual_frequencies), "# of center points != # of frequencies?"
	lights = [
			(
				positions_of_lights[i],
				room.transmitters[actual_frequencies[i]]
			) for i in xrange(len(positions_of_lights))]
	logger.debug('Raw lights information:')
	for i in range(len(lights)):
		logger.debug('\t{}: {}'.format(actual_frequencies[i], lights[i]))

	# Some frequencies have multiple locations, need to pick one
	#
	# lights = resolve_aliased_frequncies(lights)

	# AoA calcualation requires at least 3 transmitters
	assert len(lights) >= 3, "AoA calcualation requires at least 3 transmitters"

	tries = 1
	tries_rx_loc = numpy.empty([tries, 3])
	tries_rx_rot = numpy.empty([tries, 3, 3])
	tries_rx_err = numpy.empty([tries])
	#tries_method = ['YS_brute', 'static', 'scipy_basin']
	if k_val_method:
		tries_method = [k_val_method]
	else:
		tries_method = ['static']
	for i in xrange(tries):
		rx_location, rx_rotation, location_error =\
				aoa(
						room, lights, camera.Zf,
						k_init_method=tries_method[i],
						actual_location=actual_location,
						)
		logger.primary('location estimate = {}'.format(rx_location))
		logger.primary('location error    = {}'.format(location_error))
		tries_rx_loc[i] = rx_location
		tries_rx_rot[i] = rx_rotation
		tries_rx_err[i] = location_error

		if location_error > 1:
			if i == tries - 1:
				min_err_idx = numpy.argmin(tries_rx_err)
				rx_location = tries_rx_loc[min_err_idx]
				rx_rotation = tries_rx_rot[min_err_idx]
				location_error = tries_rx_err[min_err_idx]
				
				logger.warn('Error ({}) too high, but max tries exceeded'.format(location_error))
				logger.warn('Returning measurement with high error estimate')

				max_light_i = numpy.argmax(radii_of_lights)
				logger.warn('Prefer estimate of under max radii light:')
				logger.warn('Loc: {}'.format(room.transmitters[actual_frequencies[max_light_i]]))
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
