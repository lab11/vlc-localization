#!/usr/bin/env python
# vim: sts=4 ts=4 sw=4 noet:

from __future__ import print_function
import sys, os
import multiprocessing.pool
import threading, Queue

import json
import urllib2

#hack
import PIL

sys.path.append('../image_proc/')
from aoa_full import aoa_full

import pretty_logger
logger = pretty_logger.get_logger()

PYTHON3 = sys.version_info >= (3, 0)

if PYTHON3:
	from http.server import SimpleHTTPRequestHandler
	import socketserver
else:
	from SimpleHTTPServer import SimpleHTTPRequestHandler
	import SocketServer as socketserver

PORT = 4908

def work_fn(work_queue):
	while True:
		try:
			fn, args = work_queue.get()
			fn(args)
		except Exception as e:
			logger.warn("Worker exception: {}".format(e))

def on_image_received(input_image_path):
	directory, fname = os.path.split(input_image_path)
	img_name, ext = os.path.splitext(fname)
	root, img = os.path.split(directory)
	result_path = os.path.join(root, 'result', img_name + '.result.txt')
	output_path = os.path.join(root, 'result', img_name + '.log.txt')

	size = PIL.Image.open(input_image_path).size
	if (7712 in size) and (4352 in size):
		phone = 'lumia'
	elif (7136 in size) and (5360 in size):
		phone = 'lumia'
	elif (960 in size) and (1280 in size):
		phone = 'lumia-front'
	else:
		raise NotImplementedError('Unknown phone type for image dimensions: ' + str(size))

	# Copy work to an output file
	logger.copy_to_file(output_path)

	try:
		rx_location, rx_rotation, location_error = aoa_full(input_image_path, phone, False)
		logger.info('rx_location = {}'.format(rx_location))
		logger.info('rx_rotation =\n{}'.format(rx_rotation))
		logger.info('location_error = {}'.format(location_error))

		ofile = open(result_path, 'w')
		ofile.write('rx_location = {}\n'.format(rx_location))
		ofile.write('rx_rotation =\n{}\n'.format(rx_rotation))
		ofile.write('location_error = {}\n'.format(location_error))
		ofile.close()
		logger.info('Result saved to {}'.format(result_path))

		data = {
				'rx_location' : list(rx_location),
				'rx_rotation' : rx_rotation.tolist(),
				'location_error' : location_error,
				'image_name' : img_name,
		}

		req = urllib2.Request('http://inductor.eecs.umich.edu:8081/WEgwAGyc9N')
		req.add_header('Content-Type', 'application/json')

		response = urllib2.urlopen(req, json.dumps(data))
		logger.info('Result posted to gatd')

	finally:
		logger.close_copy_file()

def callback(*args):
	print("Callback")
	print("callback args = {}".format(args))

class SimpleHTTPRequestHandlerWithPUT(SimpleHTTPRequestHandler):
	def do_PUT(self):
		try:
			logger.info("do_PUT")
			logger.debug(self.headers)
			length = int(self.headers['Content-Length'])
			if length:
				content = self.rfile.read(length)
				logger.debug(content)
			self.send_response(200)
		except:
			self.send_response(500)

	def do_POST(self):
		try:
			length = int(self.headers['Content-Length'])
			if length:
				content = self.rfile.read(length)
				if self.headers['Content-Type'] == 'image/jpeg':
					path = os.path.abspath(self.path[1:])
					f = open(path, 'wb')
					f.write(content)
					f.close()
					logger.debug("Wrote {}".format(path))
					self.send_response(200)
					#r = pool.apply_async(on_image_received, path, callback=callback)
					work_queue.put((on_image_received, path))
				else:
					logger.debug(self.headers)
					#logger.debug(content)
					self.send_response(500)
		except Exception as e:
			logger.warn(e)
			logger.debug(self)
			logger.debug(self.headers)
			#logger.debug(self.__dict__)
			self.send_response(500)
			raise

if __name__ == '__main__':
	socketserver.TCPServer.allow_reuse_address = True
	socketserver.ForkingTCPServer.allow_reuse_address = True
	httpd = socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandlerWithPUT)

	logger.info("Initializing image-processing thread pool")
	#pool = multiprocessing.pool.Pool(1)
	work_queue = Queue.Queue()
	t = threading.Thread(target=work_fn, args=(work_queue,))
	t.daemon = True
	t.start()

	logger.info("Server running at port {}".format(PORT))
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		logger.info("Caught Ctrl-C. Cleaning up...")

	logger.info("Shutdown complete.")

