"""
Script resizes all images in the folder. Parameters which can be specified by the user.
scale (default = 0.5) <= how much we downscale images e.g 0.5 makes images of 1/4 or area of orig.
modify (default = True) <= are images changed in place (origs are overwritten)
path (default = '.') <= where to look for images (with subdirectories)

requires python-3.4
"""

import os
from fnmatch import fnmatch

root = '/some/directory'
pattern = "*.py"

for path, subdirs, files in os.walk(root):
	for name in files:
		if fnmatch(name, pattern):
			print os.path.join(path, name)