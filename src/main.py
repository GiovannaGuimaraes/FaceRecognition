'''
Main source file for Facial Characteristics Extraction

Lucas Alexandre Soares - 9293265
Giovanna Oliveira Guimarães - 9293693
Julia Diniz - 9364865
'''

import filters
import numpy as np
import cv2
import sys
import os

from PIL import Image, ImageOps, ImageFilter
from red_eye_detection import *
from filters import *

# Define possible filters in options dict
options = {'blur': ImageFilter.BLUR,
		  'contour': ImageFilter.CONTOUR,
		  'detail': ImageFilter.DETAIL,
		  'edge_enhance': ImageFilter.EDGE_ENHANCE,
		  'edge_enhance_more': ImageFilter.EDGE_ENHANCE_MORE,
		  'emboss': ImageFilter.EMBOSS,
		  'find_edges': ImageFilter.FIND_EDGES,
		  'smooth': ImageFilter.SMOOTH,
		  'smooth_more': ImageFilter.SMOOTH_MORE,
		  'sharpen': ImageFilter.SHARPEN
		  }
options2 = ['autocontrast', 
		   'equalize', 
		   'flip', 
		   'invert', 
		   'grayscale',
		   'mirror', 
		   'posterize', 
		   'solarize'
		   ]

# Menu handlers
def printMenu():
	print("\nOptions:")
	print("\t1 - Load image")
	print("\t2 - Filter image")
	print("\t3 - Distort image")
	print("\t4 - Remove red eyes")
	print("\t5 - Reset")
	print("\t6 - Save")
	print("\t0 - Exit")

def printFilterMenu():
	print("\n\tFilters: blur, contour, detail, edge_enhance, emboss, find_edges, smooth, sharpen, autocontrast, equalize, flip, invert, mirror, posterize, solarize")

def filterMenu(img):

	printFilterMenu()
	operation = input(">>> ")

	if operation in options:

		try:
			img2 = applyFilter(img, options[operation])

		except Exception as e:
			raise

	elif operation in options2:

		try:
			img2 = getattr(filters, operation)(img)

		except Exception as e:
			raise

	else:
		raise Exception("\nUnknown operation")

	return img2

def distortMenu(img):
	
	try:
		xGridResolution = int(input(">>> x Grid Resolution: "))
		yGridResolution = int(input(">>> y Grid Resolution: "))
		distortion = int(input(">>> Max Distortion: "))

	except Exception as e:
		print("\nInvalid parameters.")
		raise

	dest = griddify(createRect(img.size), xGridResolution, yGridResolution)
	src = distort(dest, distortion)

	return img.transform(img.size, Image.MESH, gridToMesh(src, dest))

# Helpers
def pil2cv(img):
	return np.array(img)[:, :, ::-1] # Convert from RGB to BGR

def cv2pil(img):
	return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) # Convert from BGR to RGB

def updateImg(processingImg):
	cv2.destroyWindow("Modified")
	cv2.imshow("Modified", processingImg)
	cv2.waitKey(200)


########
# Main #
########

# Select initial image
selectedImg = Image.open(input(">>> Image file: ")).convert("RGB")
# selectedImg = Image.open("databases/tests/redeye-test.jpg").convert("RGB")
processingImg = selectedImg.copy()

# Convert from pillow to opencv format and display images
cv2.imshow("Original", pil2cv(selectedImg))
cv2.imshow("Modified", pil2cv(processingImg))
cv2.waitKey(200)

# Loop forever
while True:

	printMenu()

	# Transform op in invalid command
	try:
		op = int(input(">>> "))
	except Exception as e:
		op = -1

	if op == 0:
		
		# Cleanup and exit
		cv2.destroyAllWindows()
		sys.exit()

	elif op == 1:

		try:

			selectedImg = Image.open(input(">>> Image file: ")).convert("RGB")
			processingImg = selectedImg.copy()
			cv2.destroyAllWindows()
			
			# Convert from pillow to opencv format and display images
			tmp = pil2cv(selectedImg)
			cv2.imshow("Original", tmp)
			cv2.imshow("Modified", tmp)
			cv2.waitKey(100)

		except IOError as e:
			print("\nImage not found.")

	elif op == 2:
		try:
			
			tmp = filterMenu(processingImg)
			
			# Preserve processing image in case something bad happens
			processingImg = tmp
			updateImg(pil2cv(processingImg))

		except Exception as e:
			print(e)
	
	elif op == 3:
		try:
			
			tmp = distortMenu(processingImg)
			
			# Preserve processing image in case something bad happens
			processingImg = tmp
			updateImg(pil2cv(processingImg))
			
		except Exception as e:
			print(e)

	elif op == 4:
		try:
			tmp = correctRedEye(pil2cv(processingImg), int(input(">>> Threshold: ")))
			
			# Preserve processing image in case something bad happens
			processingImg = cv2pil(tmp)
			updateImg(pil2cv(processingImg))

		except Exception as e:
			print(e)
			

	elif op == 5:
		processingImg = selectedImg
		updateImg(pil2cv(processingImg))

	elif op == 6:
		path = input(">>> Filename: ")
		img = pil2cv(processingImg)
		try:
			cv2.imwrite(path, img)
		except Exception as e:
			print("Directory does not exists or is inaccessible")

	else:
		print("\nUnknown operation.")

