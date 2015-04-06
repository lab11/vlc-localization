#!/usr/bin/env python
# vim: sts=4 ts=4 sw=4 noet:

from __future__ import print_function
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

import pretty_logger
logger = pretty_logger.get_logger()

def get_Z_offset_guess(room):
	# Assume we are ~2.5 m away in Z
	DEFAULT_OFFSET = 2.5

	if room.units == 'm':
		offset = DEFAULT_OFFSET
	elif room.units == 'cm':
		offset = DEFAULT_OFFSET * 100
	elif room.units == 'in':
		offset = (DEFAULT_OFFSET * 100) / 2.54
	else:
		raise NotImplementedError('Unknown unit: {}'.format(room.units))

	if room.user_is == 'below':
		pass
	elif room.user_is == 'above':
		offset = -offset
	else:
		raise NotImplementedError('Unkonwn user position: {}'.format(room.user_is))

	return offset

@logger.op("AoA on lights {1} with Zf={2}")
def aoa(room, lights, Zf, k_init_method='scipy_basin', actual_location=None):
	# Convert argument to useful array format
	centers = numpy.array(zip(*lights)[0])
	transmitters = numpy.array(zip(*lights)[1])

	# Add Zf column to centers array (light z coordinate is fixed by Zf)
	centers = numpy.append(centers, Zf * numpy.ones((len(lights), 1)), axis=1)

	logger.debug('centers\n{}'.format(centers))
	logger.debug('transmitters\n{}'.format(transmitters), remove_blanklines=True)

	## Precompute static properties of locations (constant calculation)
	logger.start_op("Pre-computing static arrays used for AoA")

	# Compute squared distance from lens center to each projection
	image_squared_distance = numpy.sum(numpy.square(centers), axis=1)
	logger.debug2('image_squared_distance\n{}'.format(image_squared_distance))

	# Compute pairwise constants (2*K_m*K_n term and abosulte square distances)
	pair_shape = (len(lights)-1, len(lights))
	transmitter_pair_squared_distance = numpy.zeros(pair_shape)
	pairwise_image_inner_products     = numpy.zeros(pair_shape)
	for i in xrange(len(lights)-1):
		for j in xrange(i+1, len(lights)):
			transmitter_pair_squared_distance[i][j] =\
					numpy.sum(numpy.square(transmitters[i] - transmitters[j]))
			pairwise_image_inner_products[i][j]=\
					numpy.dot(centers[i], centers[j])
	logger.debug2('transmitter_pair_squared_distance\n{}'.format(transmitter_pair_squared_distance))
	logger.debug2('pairwise_image_inner_products\n{}'.format(pairwise_image_inner_products))

	logger.end_op()
	## End precompute constants

	# In the Python version we use an explicit least-squares algorithm so the
	# return value from this function is not squared (the leastsq algorithm does that)
	def least_squares_scaling_factors(k_vals):
		errs = []
		for i in xrange(len(lights)-1):
			for j in xrange(i+1, len(lights)):
				errs.append(
						k_vals[i]**2 * image_squared_distance[i] +\
						k_vals[j]**2 * image_squared_distance[j] -\
						2*k_vals[i]*k_vals[j] * pairwise_image_inner_products[i][j] -\
						transmitter_pair_squared_distance[i][j]
						)
		#errs = numpy.array(errs)
		#logger.debug('')
		#logger.debug('k_vals = {}'.format(k_vals))
		#logger.debug('errs = {}'.format(errs))
		#logger.debug('err2 = {}'.format(errs**2))
		#logger.debug('sum = {}'.format(sum(errs**2)))
		return errs

	def scalar_scaling(k_vals):
		errs = numpy.array(least_squares_scaling_factors(k_vals))
		#print(numpy.sum(errs))
		return numpy.sum(errs)

	# Brute force find scaling factors
	# start guessing first scaling factor and solves for rest
	# putting all scaling factors into constraint to find errors
	def sol_guess_subset(index, var_cnt, sol_guess):
		sol_guess_sub = numpy.array([sol_guess[0,0]])
		for i in range(1,len(lights)):
			if sol_guess[i, 1] < 0:
				sol_guess_sub = numpy.append(sol_guess_sub, sol_guess[i, int((index%(2**var_cnt))/2**(var_cnt-1))])
				var_cnt -= 1
			else:
				sol_guess_sub = numpy.append(sol_guess_sub, sol_guess[i, 0])
		return sol_guess_sub

	@logger.op('Brute force K Values')
	def brute_force_k():
		number_of_iteration = 500
		k0_vals = numpy.linspace(-0.1, -0.01, number_of_iteration)
		err_history = []
		idx_history = []
		k_vals = numpy.array([])
		for j in range(number_of_iteration+1):
			# Last iteration, Find minimum
			if (j==number_of_iteration):
				min_error_history_idx = err_history.index(min(err_history))
				min_idx = idx_history[min_error_history_idx]
				print("Using index ", min_idx, "for initial guess")
				k0_val = k0_vals[min_idx]
				#print(k0_val)
			else:
				k0_val = k0_vals[j]
			sol_guess = numpy.array([[k0_val, 0]])
			sol_found = 1
			multiple_sol = 0
			for i in range(1, len(lights)):
				sol = numpy.roots([image_squared_distance[i], -2*sol_guess[0,0]*pairwise_image_inner_products[0,i], (sol_guess[0,0]**2*image_squared_distance[0]-transmitter_pair_squared_distance[0, i])]);
				if numpy.isreal(sol)[0]:
					if (sol[0] < 0) and (sol[1] < 0):
						sol_guess = numpy.append(sol_guess, [sol], axis=0)
						multiple_sol += 1
					elif sol[0] < 0:
						sol_guess = numpy.append(sol_guess, numpy.array([[sol[0], 0]]), axis=0)
					elif sol[1] < 0:
						sol_guess = numpy.append(sol_guess, numpy.array([[sol[1], 0]]), axis=0)
					else:
						sol_found = 0
						break
				else:
					sol_found = 0
					break
			if sol_found:
				scaling_factors_error_combination = []
				#print ("index:", j)
				for m in range(1, 2**multiple_sol+1):
					sol_guess_combination = sol_guess_subset(m, multiple_sol, sol_guess)
					scaling_factors_error_arr = least_squares_scaling_factors(sol_guess_combination)
					scaling_factors_error = 0
					for n in scaling_factors_error_arr:
						scaling_factors_error += n**2
					scaling_factors_error_combination.append(scaling_factors_error)
					#print("m: ", m, sol_guess_subset(m, multiple_sol, sol_guess), "error: ", scaling_factors_error)
				k_vals = sol_guess_subset(numpy.argmin(scaling_factors_error_combination)+1, multiple_sol, sol_guess)
				#print("mininum index", numpy.argmin(scaling_factors_error_combination), "K values: ", k_vals)
				if len(err_history)==0:
					print ("First found index: ", j)
				err_history.append(min(scaling_factors_error_combination))
				idx_history.append(j)
		return k_vals
		# End of brute force method

	logger.start_op('Minimize distance function')
	if actual_location is not None:
		k_vals_actual = []
		for i in range(len(centers)):
			# T is phone location in transmitter's frame of reference
			# (Tx - x)^2 + (Ty - y)^2 + (Tz - z)^2 = K^2*(a^2 + b^2 + Zf^2)
			t_sum = (actual_location[0] - transmitters[i][0][0])**2 +\
					(actual_location[1] - transmitters[i][0][1])**2 +\
					(actual_location[2] - transmitters[i][0][2])**2
			px_sum = image_squared_distance[i]
			k_sqared = t_sum / px_sum
			k_vals_actual.append(k_sqared**.5)

		logger.debug('{} (k_vals_actual)'.format(k_vals_actual))

	if k_init_method == 'static':
		k_val_from_z = get_Z_offset_guess(room) / Zf
		k_vals_init = [k_val_from_z] * len(lights)
	elif k_init_method == 'YS_brute':
		k_vals_init = brute_force_k()
	elif k_init_method == 'scipy_brute':
		k_ranges = [slice(.01, .1, (.1-.01)/10) for i in xrange(len(lights))]
		k_vals_init = scipy.optimize.brute(scalar_scaling, k_ranges, disp=True)
	elif k_init_method == 'scipy_basin':
		# The basin method still requires somewhere to start from but hops much
		# more aggressively around the space than leastsq eventually will
		k_vals_init = [-.05] * len(lights)
		res = scipy.optimize.basinhopping(scalar_scaling, k_vals_init,
				T=1e12,
				stepsize=0.01,
				)
		k_vals_init = res.x
	elif k_init_method == 'actual':
		assert actual_location is not None
		k_vals_init = k_vals_actual
	else:
		logger.error("Unknown k_init_method. Valid options are:\n"\
				"  static YS_brute scipy_brute scipy_basin")

	logger.debug('{} (k_vals_init from {})'.format(k_vals_init, k_init_method))
	k_vals, ier = scipy.optimize.leastsq(least_squares_scaling_factors, k_vals_init)

	if ier not in (1,2,3,4):
		# ier is a return code that must be in (1,2,3,4) if leastsq succeeded:
		# http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.leastsq.html
		raise ValueError("Least squares failed to minimize distance function")
	logger.debug('{} (k_vals after leastsq)'.format(k_vals))

	logger.end_op()

	def least_squares_rx_location(rx_location):
		dists = []
		for i in xrange(len(lights)):
			dists.append(
					numpy.sum(numpy.square(rx_location - transmitters[i])) -\
					k_vals[i]**2 * image_squared_distance[i]
					)
		return dists

	def initial_position_guess(room, transmitters):
		'''Need to see huerisitic with a location; use the average of lights'''
		guess = numpy.mean(transmitters, axis=0)[0]
		offset = get_Z_offset_guess(room)
		guess[2] = guess[2] - offset
		return guess

	logger.start_op('Minimize location function')
	if k_init_method == 'actual':
		rx_location_init = actual_location
	else:
		rx_location_init = initial_position_guess(room, transmitters)
	logger.debug('seed_loc_guess = {}'.format(rx_location_init))
	rx_location, ier = scipy.optimize.leastsq(least_squares_rx_location, rx_location_init)
	if ier not in (1,2,3,4):
		raise ValueError("Least squares failed to minimize location function")
	logger.debug('   rx_location = {}'.format(rx_location))
	logger.end_op()

	def least_squares_rotation(rotation):
		rotation = rotation.reshape((3,3))
		r = transmitters.T - rotation.dot(absolute_centers) - rx_location.reshape(3,1)
		r = numpy.square(r)
		r = r.flatten()
		return r

	# Compute the scaled and transformed transmitter locations
	absolute_centers = centers.T * numpy.vstack([k_vals, k_vals, k_vals])
	logger.debug('absolute_centers =\n{}'.format(absolute_centers))

	# Compute the rotation matrix -- this requires a little bit of re-shaping
	# because the scipy optimizer flattens matricies into 1d arrays when passing
	# arugments in and out. We just have to correct this in the called function
	# and in the return value.
	logger.start_op('Minimize rotation function')
	rx_rotation_init = numpy.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
	rx_rotation, ier = scipy.optimize.leastsq(least_squares_rotation, rx_rotation_init)
	if ier not in (1,2,3,4):
		raise ValueError("Least squares failed to minimize rotation function")
	rx_rotation = numpy.array(rx_rotation).reshape((3,3))
	logger.debug('rx_rotation =\n{}'.format(rx_rotation))
	logger.end_op()

	# Compute the error
	logger.start_op('Compute error')
	rx_location_error = numpy.sum(numpy.abs(
			numpy.sqrt(numpy.sum(numpy.square(rx_location - transmitters[i]))) -\
			numpy.sqrt(k_vals[i]**2 * image_squared_distance[i])
			))
	logger.debug('rx_location_error = {}'.format(rx_location_error))
	logger.end_op()

	return (rx_location, rx_rotation, rx_location_error)

