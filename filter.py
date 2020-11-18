import cv2
import numpy as np
import scipy

def adjust_gamma(image, gamma=1.0):
   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")
   return cv2.LUT(image, table)

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

def increase_sharpness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    lim = 255 - value
    s[s > lim] = 255
    s[s <= lim] += value
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

def brightFilter(image):
	kernel = np.ones((5, 5), np.uint8)
	image = adjust_gamma(image, 2.0)
	image = increase_brightness(image, 150)
	image = cv2.bitwise_not(image)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	image = cv2.threshold(image, 20, 255, cv2.THRESH_BINARY)[1]
	image = cv2.dilate(image,kernel,iterations = 5)
	return image
	
def eraseBackground(img,c):
	fill_color = [0, 0, 0]
	mask_value = 255
	stencil  = np.zeros(img.shape[:-1]).astype(np.uint8)
	cv2.fillPoly(stencil, [c], mask_value)
	sel = stencil != mask_value
	img[sel] = fill_color   
	return img

def darkFilter(image):
	kernel = np.ones((5, 5), np.uint8)
	print("Bilateral filter...", end = '')
	#image = cv2.bilateralFilter(image, 40 ,200,  200)
	print(" Done.")

	print("Gamma filter...", end = '')
	#image = adjust_gamma(image, 0.5)
	print(" Done.")

	print("Erode filter...", end = '')
	image = cv2.erode(image, kernel,iterations=5) 
	print(" Done.")

	print("Gaussian filter...", end = '')
	#image = cv2.GaussianBlur(image, (7,7), 0)
	print(" Done.")

	print("Median filter...", end = '')
	#image = cv2.medianBlur(image, 25)
	print(" Done.")

	print("Gray filter...", end = '')
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	image = cv2.threshold(image, 30, 255, cv2.THRESH_BINARY)[1]
	print(" Done.")
	cv2.imwrite("nal.jpg", image)

	return image
