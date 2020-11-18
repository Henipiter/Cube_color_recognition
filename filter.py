import cv2
import numpy as np

def adjust_gamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)



def make_filters(image):
	gamma = 0.5
	image = adjust_gamma(image, gamma)
	kernel = np.ones((5, 5), np.uint8)
	for i in range(0,5):
		image = cv2.erode(image, kernel) 
	image = cv2.bilateralFilter(image, 40 ,200,  200)
	image = cv2.GaussianBlur(image, (7,7), 0)
	image = cv2.medianBlur(image, 25)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	image = cv2.threshold(image, 30, 255, cv2.THRESH_BINARY)[1]
	return image
