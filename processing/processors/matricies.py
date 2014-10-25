#!/usr/bin/env python
# vim: sts=4 ts=4 sw=4 noet:

from __future__ import print_function
import sys, os
import numpy
import numpy.ma
import scipy
import scipy.misc
import scipy.ndimage
import scipy.signal
import scipy.cluster
import skimage
import skimage.filter
import skimage.morphology
import matplotlib
import matplotlib.mlab
import pylab

sys.path.append('..')
import pretty_logger
logger = pretty_logger.get_logger()

def dbg_save(fname, array):
	scipy.misc.imsave(fname, array)
	logger.debug('Saved WIP to {}'.format(fname))

def dbg_plot(fname, *args):
	return
	pylab.plot(*args)
	pylab.savefig(fname)
	logger.debug('Plotted WIP to {}'.format(fname))

def dbg_plot_subplots(fname):
	logger.start_op('plot_subplots for ' + fname)
	pylab.savefig(fname, dpi=1200)
	logger.debug('Plotted WIP subplots to {}'.format(fname))
	logger.end_op()

def disk(radius):
	x, y = numpy.meshgrid(range(-radius, radius+1), range(-radius, radius+1))
	x = numpy.square(x)
	y = numpy.square(y)
	r = numpy.sqrt(x + y)
	f = r <= radius
	f = f / float(sum(sum(f)))
	return f

def static_imag_proc(file_name, num_of_tx, phone_type, debug):
	logger.info("Returning static_imag_proc results")
	centers = numpy.array([[3045, 1380], [3055, 3010], [3894, 2189], [4735, 1366], [4747, 3009]])
	estimated_frequencies = numpy.array([2954.19921875, 3363.2421875, 3954.08203125, 2408.80859375, 1999.765625])
	shape = (7712, 4352)
	return (centers, estimated_frequencies, shape)

@logger.op("Process image {0} with {1} transmitter(s) taken with {2.__name__}")
def imag_proc(file_name, num_of_tx, camera, debug):
	raise NotImplementedError("This method was abandoned and not updated for new calling signature (no radii)")

	# Load image and convert to grayscale
	logger.start_op("Loading image")
	gray_image = scipy.misc.imread(file_name, flatten=True) #flatten == rbg2gray
	logger.debug('gray_image.shape = {}'.format(gray_image.shape))
	if debug:
		dbg_save('/tmp/gray_image.png', gray_image)
	logger.end_op()

	# Handle orientation
	logger.start_op("Normalizing image rotation")
	if gray_image.shape[1] > gray_image.shape[0]:
		logger.debug('rotating image')
		# MATLAB default is 'nearest', Python's is 'bilinear'
		gray_image = scipy.misc.imrotate(gray_image, 270, 'nearest')
	if debug:
		dbg_save('/tmp/gray_image_rotated.png', gray_image)
	logger.debug('gray_image.shape = {}'.format(gray_image.shape))
	logger.end_op()

	# Blur image
	logger.start_op("Applying blur")
	m2 = scipy.ndimage.gaussian_filter(gray_image, sigma=5)
	if debug:
		dbg_save('/tmp/after_blur.png', m2)
	logger.debug('m2.shape = {}'.format(m2.shape))
	logger.end_op()

	# Replace manual threshold with more efficient OTSU filter
	logger.start_op("OTSU Filter (threshold image)")
	val = skimage.filter.threshold_otsu(m2)
	logger.debug('val = {}'.format(val))
	otsu = m2 > val
	if debug:
		dbg_save('/tmp/otsu.png', otsu)
	logger.end_op()

	# Label finds each disjoint set of pixels and assigns them to a group (fast)
	# The center_of_mass finds the center point of each blob (slower than I'd like)
	logger.start_op("Find blob centers")
	blobs = otsu > otsu.mean()
	blobs_labels, cnt = scipy.ndimage.label(blobs)
	logger.debug('cnt = {}'.format(cnt))
	if debug:
		dbg_save('/tmp/blobs_labels.png', blobs_labels)
	com = scipy.ndimage.measurements.center_of_mass(blobs, blobs_labels, range(1,cnt+1))
	logger.debug('com = {}'.format(com))

	centroids = numpy.array(com)
	number_of_transmitters = cnt
	assert number_of_transmitters >= 3, 'not enough transmitters'
	logger.end_op()

	# Find centers and sort
	centers = centroids.astype(int)
	# idiom for matlab sortrows:
	# http://mathesaurus.sourceforge.net/matlab-numpy.html
	centers = centers[centers[:,0].argsort(),]
	logger.debug('centers = {}'.format(centers), remove_newlines=True)
	#logger.end_op() was clustering's

	Fs = 1/camera.rolling_shutter_r
	T = 1/Fs
	NFFT = 1024
	gain = 5

	estimated_frequencies = []
	window_size = 100

	logger.start_op("Computing transmitter frequencies")
	for i in xrange(number_of_transmitters):
		#row_above = gray_image[centers[i][0]-5]
		image_row = gray_image[centers[i][0]]
		#row_below = gray_image[centers[i][0]+5]
		if (centers[i][1] - window_size) < 1:
			#abv = row_above[0:centers[i][1]+window_size+1]
			sig = image_row[0:centers[i][1]+window_size+1]
			#blw = row_below[0:centers[i][1]+window_size+1]
		elif (centers[i][1]+window_size) > min(gray_image.shape):
			#abv = row_above[centers[i][1]-window_size:min(gray_image.shape)]
			sig = image_row[centers[i][1]-window_size:min(gray_image.shape)]
			#blw = row_below[centers[i][1]-window_size:min(gray_image.shape)]
		else:
			#abv = row_above[centers[i][1]-window_size:centers[i][1]+window_size]
			sig = image_row[centers[i][1]-window_size:centers[i][1]+window_size]
			#blw = row_below[centers[i][1]-window_size:centers[i][1]+window_size]

		orig_sig = sig.copy()

		#logger.debug('abv: {}'.format(abv))
		#logger.debug('sig: {}'.format(sig))
		#logger.debug('blw: {}'.format(blw))
		#abv[abv < matplotlib.mlab.prctile(abv, 90)] = 0
		#sig[sig < matplotlib.mlab.prctile(sig, 90)] = 0
		#blw[blw < matplotlib.mlab.prctile(blw, 90)] = 0
		#logger.debug('abv: {}'.format(abv))
		#logger.debug('sig: {}'.format(sig))
		#logger.debug('blw: {}'.format(blw))
		#y = abv + sig + blw
		#logger.debug('  y: {}'.format(y))

		y = orig_sig

		if debug:
			#pylab.subplot(number_of_transmitters,3,3*i-2)
			#pylab.plot(orig_sig)
			pylab.subplot(number_of_transmitters,2,2*i-1)
			pylab.plot(y)

		L = len(y)
		t = numpy.arange(0,L) * T
		Y = numpy.fft.fft(y* gain, NFFT) / float(L)
		f = Fs/2 * numpy.linspace(0,1,NFFT/2.0+1)
		Y_plot = 2*abs(Y[0:NFFT/2.0+1])

		if debug:
			pylab.subplot(number_of_transmitters,2,2*i)
			pylab.plot(f, Y_plot)
			pylab.title(str(centers[i]))
			pylab.xlabel('Frequency (Hz)')
			pylab.xlim([0,5000])

		peaks = scipy.signal.argrelmax(Y_plot)[0]
		#logger.debug('peaks =\n{}'.format(peaks))
		#logger.debug('f[peaks] =\n{}'.format(f[peaks]))
		#logger.debug('Y_plot[peaks] =\n{}'.format(Y_plot[peaks]))

		idx = numpy.argmax(Y_plot[peaks])
		peak_freq = f[peaks[idx]]

		logger.debug('center {} peak_freq = {}'.format(centers[i], peak_freq))

		estimated_frequencies.append(peak_freq)

	if debug:
		dbg_plot_subplots('/tmp/freq_fft_transmitters.png')

	logger.debug('estimated_frequencies = {}'.format(estimated_frequencies))
	logger.end_op()

	return (centers, estimated_frequencies, gray_image.shape)

