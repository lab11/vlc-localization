#!/usr/bin/env python2
# vim: sts=4 ts=4 sw=4 noet:

from __future__ import print_function
import sys
import os
import argparse

import pretty_logger
import pickle
import numpy
import test_pics

logger = pretty_logger.get_logger()

#holds error of localization,location on comp, type of image, error in frequency
class Picture:
	def __init__(self,a,b,c,d):
		self.error = a
		self.loca = b
		self.ptype = c
		self.freq_diff = d

def run_test(filename,only_im,roomin):
	#comment out to silence logger
	try:
		if os.environ['DEBUG'] == '2':
			debug = True #this line is changed
		else:
			debug = False
	except KeyError:
		debug = False
	
	#from phones import args.camera.split('-')[0] as phone
	phone = __import__('phones.' + 'lumia_1020', fromlist=[1,])
	camera = phone.cameras[0]

	imag_proc = __import__('processors.' + 'opencv_fft', fromlist=[1,]).imag_proc

	if only_im:
		try:
			centers, radii, estimated_frequencies, shape =\
					imag_proc(filename, 0, camera, debug)
			return estimated_frequencies
		except Exception as e:
			logger.warn('Exception: {}'.format(e))
			raise
	else:
		from aoa_full import aoa_full
		room = __import__('rooms.' + roomin, fromlist=[1,])
		try:
			rx_location, rx_rotation, location_error = aoa_full(
					filename, camera, room, imag_proc, debug)
			return location_error
		except Exception as e:
			return "false"
			logger.warn('Exception: {}'.format(e))
			raise

#finds statistics on error in localization (improvement/depreciation)
def find_error_diffs(error_list):
	infile = open("error_list.txt","r")
	saved_error_list = pickle.load(infile)
	infile.close()
	i = 0
	num_better = 0
	num_worse = 0
	num_same = 0
	delta_e  = 0.0
	print ("----------------------------------------")
	while i < len(error_list):
		if error_list[i].error < saved_error_list[i].error:
			num_better = num_better + 1
			if error_list[i].error == "false":
				print ("Error in " + error_list[i].loca)
				i = i + 1
				continue
			delta_e = delta_e + (numpy.float64(error_list[i].error) - numpy.float64(saved_error_list[i].error))
			print ("Error Improved to " + str(error_list[i].error) + " from " + str(saved_error_list[i].error) +"!")
			print ("	File Type: " + error_list[i].ptype + "  -- " + error_list[i].loca)
		elif error_list[i].error > saved_error_list[i].error:
			num_worse = num_worse + 1
			print (delta_e)
			print (error_list[i].error)
			print (saved_error_list[i].error)
			if error_list[i].error == "false":
				print ("Error in " + error_list[i].loca)
				i = i + 1
				continue
			delta_e = delta_e + (numpy.float64(error_list[i].error) - numpy.float64(saved_error_list[i].error))
			print ("Error Depreciated to " + str(error_list[i].error) + " from " + str(saved_error_list[i].error) +"!")
			print ("	File Type: " + error_list[i].ptype + "  -- " + error_list[i].loca)
		elif error_list[i].error == saved_error_list[i].error: 
			num_same = num_same + 1
		i = i + 1
	avg_delta_e = (delta_e)/(num_better + num_worse + num_same)
	i = 0
	total_error = 0
	while i < len(error_list):
		if error_list[i].error < 0.00001 and error_list[i].error > -0.00001:
			error_list[i].error = 0.0
		total_error = total_error + error_list[i].error
		if i < 9:
			print (error_list[i].loca + "   ---   " + str(error_list[i].error)) 
		else:
			print (error_list[i].loca + "  ---   " + str(error_list[i].error)) 
		i = i + 1
	avg_error = total_error/len(error_list)
	print ("Average Error: " + str(avg_error))
	return avg_delta_e,num_better,num_worse,num_same

#finds statistics on error in frequency calculation (improvement/depreciation)
def find_freq_diff(freq_list):
	infile = open("freq_list.txt","r")
	saved_freq_list = pickle.load(infile)
	infile.close()
	i = 0
	num_dep = 0
	num_imp = 0
	num_eq = 0
	print ("----------------------------------------")
	while i < len(freq_list):
		if abs(freq_list[i].freq_diff) < abs(saved_freq_list[i].freq_diff):
			num_imp = num_imp + 1
			print ("Freq diff Improved to" + str(freq_list[i].freq_diff) +" from " + str(saved_freq_list[i].freq_diff) + "!")
			print ("	File Type: " + str(freq_list[i].ptype) + "  -- " + str(freq_list[i].loca))
		elif abs(freq_list[i].freq_diff) > abs(saved_freq_list[i].freq_diff):
			num_dep = num_dep + 1
			print ("Freq diff Depreciated to" + str(freq_list[i].freq_diff) +" from " + str(saved_freq_list[i].freq_diff) + "!")
			print ("	File Type: " + str(freq_list[i].ptype) + "  -- " + str(freq_list[i].loca))
		else:
			num_eq = num_eq + 1
		i = i + 1
	return num_imp-num_dep, num_imp, num_dep,num_eq

def print_localization_stats(num_better,num_worse,num_same,avg_delta_e):
	print ("----------------------------------------")
	print ("Number of Improved Images: " +  str(num_better))
	print ("Number of Depreciated Images: " + str(num_worse))
	print ("Number of Unchanged Images: " + str(num_same))
	print ("Average Error Change: " + str(avg_delta_e))
	print ("----------------------------------------")


def print_frequency_stats(num_imp,num_dep,num_eq):
	print ("----------------------------------------")
	print ("Number of Improved Frequencies: " + str(num_imp))
	print ("Number of Depreciated Frequencies: " + str(num_dep))
	print ("Number of Unchanged Frequencies: " + str(num_eq))
	print ("----------------------------------------")
def print_stats(error_list,freq_list,args):

	if args.localization == True:
		avg_delta_e, num_better, num_worse, num_same  = find_error_diffs(error_list)
		print_localization_stats(num_better,num_worse,num_same,avg_delta_e)

	if args.frequency == True:
		delta_f, num_imp, num_dep, num_eq = find_freq_diff(freq_list)
		print_frequency_stats(num_imp,num_dep,num_eq)
	
	if args.frequency == False and args.localization == False:
		avg_delta_e, num_better, num_worse, num_same  = find_error_diffs(error_list)
		delta_f, num_imp, num_dep, num_eq = find_freq_diff(freq_list)
		print_localization_stats(num_better,num_worse,num_same,avg_delta_e)
		print_frequency_stats(num_imp,num_dep,num_eq)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
			formatter_class=argparse.RawDescriptionHelpFormatter,
			description='Program Action: Regression Test Image Processing',
			epilog='''Can only save data if running Localization AND Frequency Testing
		
To test you must set enviroment variable SHED_DATA to location of dir "shed-data"
EX: export SHED_DATA="~/shed-data"

TEST ALL THE THINGZ!!!
''')
	parser.add_argument('-s', '--save',
			action = "store_true",
			help='save data as comparison data')
	parser.add_argument('-u', '--update',
			action = "store_true",
			help='add to image stores')
	parser.add_argument('-l', '--localization',
			action = "store_true",
			help='only run localization testing')
	parser.add_argument('-f', '--frequency',
			action = "store_true",
			help='only run frequency testing')
	parser.add_argument('-b','--box',
			action = "store_true",
			help='run box test')

	args = parser.parse_args()
	if args.box == False:
		try:
			path = os.environ['SHED_DATA']
		except KeyError:
			#SHED-DATA not set
			print ("Path Not Found to directory \"shed-data\"")
			print ("Edit Environment variable SHED_DATA to path to dir shed-data")
			print ("EX: export SHED_DATA=\"~/shed-data\"")
			sys.exit()
	
	error_list = []
	freq_list = []
	all_ins = args.frequency == False and args.localization == False and args.box == False
	if args.localization == True or all_ins :
		error_list = test_pics.sample_test(error_list)
		error_list = test_pics.angle_x_test(error_list,path)
		error_list = test_pics.angle_y_test(error_list,path)
		error_list = test_pics.angle_y_test(error_list,path)
	if args.frequency == True or all_ins:
		freq_list = test_pics.dist_TX1K_test(freq_list,path)
		freq_list = test_pics.dist_TX3K_test(freq_list,path)
	
	if args.box == True or all_ins:
		error_list = test_pics.full_box_test(error_list)

	if args.update:
		pickle.dump(error_list,open("error_list.txt","w"))
		pickle.dump(freq_list,open("freq_list.txt","w"))

	print_stats(error_list,freq_list,args)

	if args.save == True and all_ins:
		infile1 = open("error_list.txt","w")
		infile2 = open("freq_list.txt","w")
		pickle.dump(error_list,infile1)
		pickle.dump(freq_list,infile2)
		infile1.close()
		infile2.close()
		print ("Data Saved")
	
	print ("Session Ended")


