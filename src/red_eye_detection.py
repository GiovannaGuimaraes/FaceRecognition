'''
Red eyes correction source file for Facial Characteristics Extraction

Lucas Alexandre Soares - 9293265
Giovanna Oliveira Guimarães - 9293693
Julia Diniz - 9364865
'''

import cv2
import numpy as np

def findEyes(img):

	# Load HAAR cascade
	eyesCascade = cv2.CascadeClassifier("cascade/haarcascade_eye.xml")

	# eyeRects contain bounding rectangle of all detected eyes
	return eyesCascade.detectMultiScale(img , 1.1, 5 )

def correctRedEye(img, threshold=80):
	
	if threshold > 100 or threshold < 0:
		raise Exception("Invalid threshold, must be 0 < threshold < 100.")

	outImage = img.copy()
	eyeRects = findEyes(img)

	print(eyeRects)

	# Iterate over all found eyes
	for x, y, w, h in eyeRects:

		# Crop the eye region
		eyeImage = img[y:y+h, x:x+w]

		b, g, r = cv2.split(eyeImage)

		# Add blue and green channels
		bg = cv2.add(b, g)

		# Threshold the mask based on red color and combination of blue and green color
		mask = ( (r > (bg-20)) & (r > threshold) ).astype(np.uint8)*255

		# Find all contours
		# It return (image, contours, hierarchy)
		_, contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

		# Find contour with max Area
		maxArea = 0
		maxCont = None
		
		for cont in contours:
			
			area = cv2.contourArea(cont)
			
			if area > maxArea:
				maxArea = area
				maxCont = cont
		
		mask = mask * 0  # Reset the mask image to complete black image
		
		# Draw the biggest contour on mask to guarantee that we cover entire red
		# region
		cv2.drawContours(mask, [maxCont], 0, (255), -1)
		
		# Close the holes to make a smooth region
		mask = cv2.morphologyEx( mask, cv2.MORPH_CLOSE, 
			cv2.getStructuringElement(cv2.MORPH_DILATE, (5,5)) )

		mask = cv2.dilate(mask, (3,3), iterations=3)

		# The information of only red color is lost, so we fill the mean of blue and
		# green color in all three channels(BGR) to maintain the texture
		mean = bg/2

		mean = mean.astype(np.uint8)
		mask = mask.astype(np.uint8)

		# Fill this black mean value to masked image
		mean = cv2.bitwise_and(mean, mask)
		mean = cv2.cvtColor(mean, cv2.COLOR_GRAY2BGR)
		mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
		eye = cv2.bitwise_and(~mask, eyeImage) + mean
		outImage[y:y+h, x:x+w] = eye

	return outImage

