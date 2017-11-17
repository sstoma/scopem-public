#!/usr/bin/env python
__doc__ = """
Script creates a preview of a plate based on all images in the folder. TODO

Requires: 
* xvfb to not block the screen

Python: 
* requires python-3.2

:bug:
	None known.
	
:organization:
	ETH
"""
__authors__="""Szymon Stoma"""
__contact__="<Your contact>"
__license__="Cecill-C"
__date__="17-11-05"
__version__="0.2"
__docformat__= "restructuredtext en"

# imports ============================================================================================================================================

#import csv # for CSV files
import os
from fnmatch import fnmatch
import argparse
import subprocess

from os.path import join as pj
import os
import os.path
from copy import copy
from math import sqrt
import yaml # config
import fnmatch
import os
import re
#from PIL import Image 
from subprocess import call

# ---------------------------------------------------------------- HELPERS
def err( s ):
	# drops a line and exits with errorcode
	print(''.join(s))
	exit(1)

def wrn( s ):
	# drops a line and continues
	print(''.join(s))

def well_coord( str1 ):
	return (str1[0], int(str1[1:]))

def well_coord_inv( letter, num ):
	return letter+"%.2d"%num

def well2cords( id ):
	# (0..15), (0,23)
	letter = id[ 0 ]
	num = int(id[1:])
	letters = 'ABCDEFGHIJKLMNOP'
	return (letters.index(letter), num-1)

# local confs
config_fn = 'config.yaml'

def run():
	# run for files with Take in file name
	#fn_regex ='(\w+\-\w+)(L\w+|F\w+)-Take(\d)_(\w+)_s(\w+)_w(\d{1})'

	# read config
	with open(config_fn, 'r') as f:
		conf = yaml.safe_load(f)
		# getting config vars
		directory_path = conf['directory_path']
		directory_output_path = conf['directory_output_path']
		fiji_path = conf['fiji_path']
		channel = conf['channel']
		file_regexp = conf['file_regexp'] # e.g. img_000000002_dTOM_000.tif
		script_fn = conf['script_fn']
		mosaic_x  =  conf['mosaic_x']
		mosaic_y  =  conf['mosaic_y']
		plate_x = conf['plate_x']
		plate_y = conf['plate_y']
		image_order = conf['image_order']

	print " #: Config used:"
	for i,j in conf.iteritems(): print i,'\t', j
	matches = {}
	matches_rev  = {}
	# prepare reg exp.
	fn_r = re.compile( file_regexp ) # make regex for the name
	for path, subdirs, files in os.walk(directory_path, followlinks=True):
		#print path, subdirs, files
		last_dir = os.path.basename(os.path.normpath( path ))
		for name in files:
			m_file = re.match( fn_r, name) # we first match a file to a template
			# if they both match we can add file to the dictionary
			if m_file:
				x, y = well2cords(m_file.group('well_id'))
				# example regex
				#'b(?P<plate>\w+-\w+)_w(?P<well_id>\w\d{2})_s(?P<site>\d{1})_z1_t1_c(?P<channel>\w+)_u(\w+).tif'
				key = (m_file.group('plate'), x, y, int(m_file.group('site'))-1, m_file.group('channel') )
				value = pj(path, name)
				matches[ key ] = value
				matches_rev[ value ] = key

	# creating mosaic structure to map files into spatial str.
	#for i in matches.keys():
	#	print i
	mosaic = {}
	for (plate_, x, y, site, channel_), v  in matches.iteritems():
		if (channel == channel_ ):
			if mosaic.has_key( (mosaic_y*y+int(image_order[site][1]), mosaic_x*x+int(image_order[site][0]) ) ):
					print " !: Overwriting...", (mosaic_y*y+int(image_order[site][1]), mosaic_x*x+int(image_order[site][0]) )
					print "    Previous key:", mosaic[ (mosaic_y*y+int(image_order[site][1]), mosaic_x*x+int(image_order[site][0]) ) ]
					print "    To be subst.:", v
					print "    Site cords. :", image_order[ site ]
			mosaic[ (mosaic_y*y+int(image_order[site][1]), mosaic_x*x+int(image_order[site][0]) ) ] = v
	# creating output file with path
	fn = pj(directory_output_path, m_file.group('plate')+"_"+m_file.group('channel')+'.txt')
	f = open(fn, 'w')
	for j in range(mosaic_y*plate_y):
		for i in range(mosaic_x*plate_x):
			f.write(mosaic[ (i,j) ]+'\n')
	f.close()


	# preparing script
	with open(pj(directory_output_path, m_file.group('plate')+"_"+m_file.group('channel')+'.ijm'), "w") as ijm_file:
		ijm_file.write("""
			// Script by Szymon Stoma (Scopem). Details: http://let-your-data-speak.com

			// INIT
			setBatchMode(true);
			run("Close All");

		""")

		ijm_file.write("""
			// CONTENT
			print(" #: START processing a set...");
			run("Stack From List...", "open=%s");
			run("8-bit");
			stack_size=nSlices();
			fn = getTitle();
			// use TransformJ to be able to run headless...
			run("Scale...", "x=.1 y=.1 z=1.0 depth="+stack_size+" interpolation=None average process create");
			
			//run("TransformJ Scale", "x-factor=0.1 y-factor=0.1 z-factor=1.0 interpolation=Linear");

			run("Make Montage...", "columns=%s rows=%s scale=1 first=1 last="+stack_size+" increment=1 border=0 font=12");

			run("Invert");
			run("Fire");
			saveAs("Tiff", "%s");
			saveAs("JPEG", "%s");

			run("Enhance Contrast...", "saturated=1 normalize equalize");
			saveAs("JPEG", "%s");

			run("Gaussian Blur...", "sigma=5");
			saveAs("JPEG", "%s");

			// FINISHING
			run("Close All");
			print(" #: DONE processing a set...");
			run("Quit");
			eval("script", "System.exit(0);"); 
		""" % ( fn,
				str(mosaic_x*plate_x), 
				str(mosaic_y*plate_y),
				pj(directory_output_path, m_file.group('plate')+"_"+m_file.group('channel')+"_invertedOrig.tif"),
				pj(directory_output_path, m_file.group('plate')+"_"+m_file.group('channel')+"_invertedOrig.jpg"),
				pj(directory_output_path, m_file.group('plate')+"_"+m_file.group('channel')+"_invertedAndEqualized.jpg"), 
				pj(directory_output_path, m_file.group('plate')+"_"+m_file.group('channel')+"_invertedBlurred.jpg"), 
			)
		)
	#call([fiji_path, "--headless", "-macro", pj(directory_output_path, m_file.group('plate')+"_"+m_file.group('channel')+'.ijm')])
	call([fiji_path, "-macro", pj(directory_output_path, m_file.group('plate')+"_"+m_file.group('channel')+'.ijm')])

with open(config_fn, 'r') as f:
	conf = yaml.safe_load(f)
	# getting config vars
	process_folder_with_plates = conf['process_folder_with_plates']
	directory_with_plates = conf['directory_with_plates']

if not process_folder_with_plates:
	run()
else:
	cnf_file_content = """
directory_path: '%s'
directory_output_path: '/Users/sstoma/Desktop/test'
fiji_path: '/Applications/Fiji.app/Contents/MacOS/ImageJ-macosx'
mosaic_x: 3
mosaic_y: 3
image_order: [[0,0],[0,1], [0,2], [1,2], [1,1], [1,0], [2,0], [2,1], [2,2]]
channel: 'DAPI'
file_regexp: 'b(?P<plate>\w+-\w+)_w(?P<well_id>\w\d{2})_s(?P<site>\d{1})_z1_t1_c(?P<channel>\w+)_u(\w+).tif'
script_fn: 'script.ijm'
plate_x: 2
plate_y: 3
process_folder_with_plates: True
directory_with_plates: '/Volumes/data/data/Paolo_Zanoni/TEST13/'
"""
	d = directory_with_plates
	plate_dirs = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]

	for i in plate_dirs:
		with open('config.yaml', 'w') as f:
			f.write( cnf_file_content % (i) )
		run()

