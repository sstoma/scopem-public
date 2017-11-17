#!/usr/bin/env python
__doc__ = """
Script resizes all images in the folder. Parameters which can be specified by the user.
scale (default = 0.5) <= how much we downscale images e.g 0.5 makes images of 1/4 or area of orig.
modify (default = True) <= are images changed in place (origs are overwritten)
path (default = '.') <= where to look for images (with subdirectories)

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
__date__="17-11-01"
__version__="0.1"
__docformat__= "restructuredtext en"

# ----------------------------------------------------------- imports

import os
from fnmatch import fnmatch
import argparse
import subprocess

# ----------------------------------------------------------- conf

conf_fiji_args = ['--headless', '-batch'] 

# ----------------------------------------------------------- parsing args
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--scale', 
	type=float,
	help='how much we downscale images e.g 0.5 makes images of 1/4 or area of orig.',
	default=0.5
)
parser.add_argument('--modify', 
	help='are images changed in place (origs are overwritten)?',
	default=True
)
parser.add_argument('--path', 
	help='where to look for images (with subdirectories)',
	default='.'
)
parser.add_argument('--file_regexp', 
	help='what files to include?',
	default='*'
)
parser.add_argument('--fiji_path', 
	help='path to executable fiji',
	default='fiji'
)
parser.add_argument('--version', action='version', version='%(prog)s '+str(__version__))

args = parser.parse_args()

# ----------------------------------------------------------- getting info about files
"""
root = args.path
pattern = args.file_regexp

to_process = []
for path, subdirs, files in os.walk(root):
	for name in files:
		if fnmatch(name, pattern):
			to_process.append(os.path.join(path, name))
"""
# print(to_process)

# ----------------------------------------------------------- converting files

subprocess.run([args.fiji_path, *conf_fiji_args]) 