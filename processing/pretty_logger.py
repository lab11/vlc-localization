#!/usr/bin/env python
# vim: sts=4 ts=4 sw=4 noet:

from __future__ import print_function
import os, time

try:
	import termcolor
	cprint = termcolor.cprint
except ImportError:
	print('termcolor package not found')
	print('output will not be colored')
	print('to fix:')
	print('\tsudo pip install termcolor')
	print('')

	cprint = lambda s, *args, **kwargs : print(s)

class Logger(object):

	class LoggerOp(object):
		def __init__(self, logger, op_str):
			self.logger = logger
			self.op_str = op_str

		def __enter__(self):
			self.logger.start_op(self.op_str)

		def __exit__(self, exception_type, exception_val, trace):
			if exception_type is None:
				self.logger.end_op()
			else:
				self.logger.end_op(success=False)

	def scoped_op(self, op_str):
		return Logger.LoggerOp(self, op_str)

	def op(self, op_str):
		"""Decorator that wraps an operation with start/end op"""
		def decorator_fn(fn):
			def wrapped_fn(*args, **kwargs):
				self.start_op(op_str.format(*args))
				try:
					ret = fn(*args, **kwargs)
				except Exception:
					self.end_op(success=False)
					raise
				self.end_op()
				return ret
			wrapped_fn.__name__ = 'op{'+fn.__name__+'}'
			return wrapped_fn
		return decorator_fn

	def debug_op(self, op_str):
		"""Decorator that conditionally wraps an operation with start/end op"""
		try:
			os.environ['DEBUG']
			return self.op(op_str)
		except KeyError:
			def nop_decorator_fn(fn):
				return fn
			return nop_decorator_fn

	def __init__(self):
		self.ops = []

	def copy_to_file(self, fname):
		if hasattr(self, 'orig_cprint'):
			raise NotImplementedError("Can only write to one output file at once")
		global cprint
		self.orig_cprint = cprint
		self.fname = fname
		self.f = open(fname, 'w')
		def new_cprint(s, *args, **kwargs):
			self.f.write(s + '\n')
			self.orig_cprint(s, *args, **kwargs)
		cprint = new_cprint
		self.info('Copying all logging output to {}'.format(fname))

	def close_copy_file(self):
		self.info('Closing logging output file {}'.format(self.fname))
		self.f.close()
		global cprint
		cprint = self.orig_cprint
		del(self.orig_cprint)

	def indent(self):
		return ' '*4*len(self.ops)

	def start_op(self, op):
		if len(self.ops) == 0:
			cprint(self.indent() +
					"Starting: " + op, 'white', attrs=['bold'])
		else:
			cprint(self.indent() +
					"Starting: " + op, 'grey', attrs=['bold'])
		self.ops.append((op, time.time()))

	def error(self, s):
		s = str(s)
		cprint(self.indent() + s, 'red', attrs=['bold'])

	def warn(self, s):
		s = str(s)
		cprint(self.indent() + s, 'yellow', attrs=['bold'])

	def info(self, s, remove_newlines=False, indent_newlines=True):
		s = str(s)
		if remove_newlines:
			s = s.replace('\n', ' ')
		elif indent_newlines:
			s = s.replace('\n', '\n'+self.indent())
		cprint(self.indent() + s, 'green', attrs=['bold'])

	def debug(self, s, remove_newlines=False, indent_newlines=True):
		try:
			os.environ['DEBUG']
		except KeyError:
			return
		s = str(s)
		if remove_newlines:
			s = s.replace('\n', ' ')
		elif indent_newlines:
			s = s.replace('\n', '\n'+self.indent())
		cprint(self.indent() + s, 'blue')

	def update(self, msg):
		op, start = self.ops[-1]
		dur = time.time() - start
		cprint(self.indent() + '{} ({:.3f} secs)'.format(msg, dur),
				'grey', attrs=['bold'])

	def end_op(self, success=True):
		op, start = self.ops.pop()
		dur = time.time() - start
		if success:
			if len(self.ops) == 0:
				cprint(self.indent() +
						"Complete: {} ({:.3f} secs)".format(op, dur),
						'white', attrs=['bold'])
			else:
				cprint(self.indent() +
						"Complete: {} ({:.3f} secs)".format(op, dur),
						'grey', attrs=['bold'])
		else:
			cprint(self.indent() + 
					"FAILED: {} ({:.3f} secs)".format(op, dur),
					'red', attrs=['bold'])

def get_logger():
	try:
		return get_logger.logger
	except AttributeError:
		get_logger.logger = Logger()
		return get_logger.logger

