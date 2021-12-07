#!/usr/bin/env python

# display an image and print out coordinates clicked

# Example usage:
# ./coord_clicker.py image1.fits
#
# Notes:
# Reading mouseclicks is best done with matplotlib.pyplot.ginput
# did not need pygame, pynput, tk etc

import sys
import os
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from astropy.wcs import WCS
#from astropy.coordinates import SkyCoord  # High-level coordinates
#from astropy import units as u
import skimage.measure as sk

def tellme(s):
    print(s)
    plt.title(s, fontsize=16)
    plt.draw()

imagefile = sys.argv[1]
print("Opening ", imagefile)

# Open image to get image parameters.
image_data = fits.getdata(imagefile)

# Have to be careful here as hdu = fits.open(imagefile)[0] gave a null wcs,
# CRVAL, CRPIX = 0, pc1_1, pc2_2 = 1, pc1_2, pc2_1 = 0 and cdelt =1
# so that it is just the pixel coords, and it looks like no WCS has been used.
hdu = fits.open(imagefile)

# [0] is a null WCS, [1] is the right one.
wcs = WCS(hdu[1].header)

#print(wcs)
#  Create a popup figure window, 10cm by 5cm
fig = plt.figure(figsize=(10, 5))

# Need space for two side-by-side plots, this is the left one.
fig.add_subplot(121, projection=wcs)

#ax = plt.subplot(projection=wcs)
#ax.grid(color='white', ls='solid')
#ax.set_xlabel('RA')
#ax.set_ylabel('Dec')
#ax = plt.subplot(projection=wcs, label='overlays')

#  Plot the image data 
plt.imshow(image_data, cmap='hot', origin='lower', vmin=10, vmax=200)

#plt.xlabel('RA')
#plt.ylabel('Dec')

# Draw the image
plt.draw()

# write some instructions
tellme("Click the mouse to continue")

# stop here until mouse is clicked
plt.waitforbuttonpress()

# Announce by changing the plot title what to do
# tellme('Click twice and a line will be drawn between the 2 clicked points.')
tellme('Select 2 points with a mouse')

# Get coords of first point
point1 = plt.ginput(1, timeout=-1, show_clicks='true')
#print("point1 is ",point1)

tellme('And now the second point.')

# Get coords of second point
point2 = plt.ginput(1, timeout=-1, show_clicks='true')
#print("point2 is ",point2)

# Convert pixel coords to RA and Dec using WCS
radec1 = wcs.pixel_to_world_values(point1)
radec2 = wcs.pixel_to_world_values(point2)

print("Point 1: pix coords, Ra, Dec",point1, radec1)
print("Point 2: pix coords, Ra, Dec",point2, radec2)

# This was for debugging
#print("type of point1 ",type(point1))
#print("type of point2 ",type(point2))

#print("point1[0] is ", point1[0][0])

# Turns out ginput returns an array within a list (or something)
x_values = [point1[0][0], point2[0][0]]
y_values = [point1[0][1], point2[0][1]]

#print("type of x_values ",type(x_values))
#print("type of y_values ",type(y_values))

# Plot a line to show where the cut in the data will be.
plt.plot(x_values, y_values)

# Use skimage.measure.profile_line to grab the pixel values
# details as below
# skimage.measure.profile_line(image, src, dst, linewidth=1,
# order=None, mode='reflect',
# cval=0.0, *, reduce_func=<function mean>)

cutline = sk.profile_line(image_data, point1[0], point2[0], linewidth=3,mode='reflect')

#fig.add_subplot(122, projection=wcs)
fig.add_subplot(122)

#plt.waitforbuttonpress()
plt.plot(cutline)

tellme('Happy? Tap keyboard key \n or click mouse to quit.')


plt.waitforbuttonpress()
#plt.show()


