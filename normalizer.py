#!/usr/bin/env python

# This script normalizes all the LAS logs in a folder with respect to
# their maximum as to display a nice color texurized version in a 
# vertical seismic display.
# The reason this thing loads all the logs into a single numpy array
# is so that in the future I can normalize across logs, not just individually.

# deps, folders, and file names
import os
import numpy as np

headlen = 36

idir = '/media/gram/DATA_SHARE/raw/'
odir = '/media/gram/DATA_SHARE/ed/'

name = []
for file in os.listdir(idir):
	if file.endswith('.las'):
		name.append(file)

# get the max log length and write headers into new files
maxlen = 0
for i in range(len(name)):
	raw = open(''.join((idir, name[i]))).read().splitlines()

	if len(raw)-headlen > maxlen:
		maxlen = len(raw)-headlen

	with open(''.join((odir, name[i])),'w') as f:
		for j in range(headlen):
			f.write(raw[j])
			f.write("\n")

# initialize
dat = np.zeros((len(name), maxlen))
dep = np.zeros((len(name), maxlen))
loglen = np.zeros(len(name))

# read data into array and do the math
for i in range(len(name)):
	raw = open(''.join((idir, name[i]))).read().splitlines()
	loglen[i] = len(raw) - headlen

	for j in range(int(loglen[i])):
		dat[i,j] = float(raw[j+headlen].split()[1])
		dep[i,j] = float(raw[j+headlen].split()[0])
	
	maxy = np.ndarray.max(dat[i,:])

	for j in range(int(loglen[i])):
		dat[i,j] = dat[i,j] / maxy

	# [do something across the i (log) dimension]

# write out data into the new files
for i in range(len(name)):
	with open(''.join((odir, name[i])), 'a') as f:
		for j in range(int(loglen[i])):
			f.write(''.join(('\t', str(dep[i,j]), '\t', str(dat[i,j]))))
			f.write("\n")
