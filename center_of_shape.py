# import the necessary packages
import argparse
import imutils
import cv2
import numpy as np

def adjust_gamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)

args= {"image" : "img1.jpg"}

gamma = 0.5

ori_image = cv2.imread(args["image"])

image = adjust_gamma(ori_image, gamma)
kernel = np.ones((5, 5), np.uint8)
for i in range(0,5):
    image = cv2.erode(image, kernel) 
   
#image = cv2.bilateralFilter(image, 40, 500, 500)

image = cv2.bilateralFilter(image,9 ,200,  200)
#image = cv2.GaussianBlur(image, (7,7), 0)
#image = cv2.medianBlur(image, 25)

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


image = cv2.threshold(image, 30, 255, cv2.THRESH_BINARY)[1]
# find contours in the thresholded image
'''
cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
#cv2.imshow('image',image)
for c in cnts:
	# compute the center of the contour
	M = cv2.moments(c)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
	# draw the contour and center of the shape on the image
	cv2.drawContours(ori_image, [c], -1, (255, 0, 255), 30)
	cv2.circle(ori_image, (cX, cY), 7, (255, 255, 255), -1)
	cv2.putText(ori_image, "center", (cX - 20, cY - 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
'''

#cv2.imwrite("g.png", ori_image) 
cv2.imwrite("g.png", image) 

#cv2.waitKey(0)
