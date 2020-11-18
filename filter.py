import cv2
import numpy as np

def adjust_gamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)



def make_filters(image):
	kernel = np.ones((5, 5), np.uint8)

	print("Bilateral filter...", end = '')
	image = cv2.bilateralFilter(image, 40 ,200,  200)
	print(" Done.")

	print("Gamma filter...", end = '')
	image = adjust_gamma(image, 0.5)
	print(" Done.")

	print("Erode filter...", end = '')
	for i in range(0,5):
		image = cv2.erode(image, kernel) 
	print(" Done.")

	print("Gaussian filter...", end = '')
	image = cv2.GaussianBlur(image, (7,7), 0)
	print(" Done.")

	print("Median filter...", end = '')
	image = cv2.medianBlur(image, 25)
	print(" Done.")

	print("Gray filter...", end = '')
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	image = cv2.threshold(image, 30, 255, cv2.THRESH_BINARY)[1]
	print(" Done.")

	return image
