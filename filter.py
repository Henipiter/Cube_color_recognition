import cv2
import numpy as np
import scipy
import drawContoures
import images

def adjust_gamma(image, gamma=1.0):
   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")
   return cv2.LUT(image, table)

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    if(value>=0):
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value
    else:
        value = -value
        v[v < value] = 0
        v[v >= value] -= value 

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

def darkBackground(image, showSteps, steps):
	
	print("Filtering...", end = '')
	kernel = np.ones((5, 5), np.uint8)
	not_image = cv2.bitwise_not(image)
	gamma_image = adjust_gamma(not_image, 1.5)
	bright_image = increase_brightness(gamma_image, 100)
	dilate_image = cv2.dilate(bright_image,kernel,iterations = 5)
	not_image2 = cv2.bitwise_not(dilate_image)
	gray_image = cv2.cvtColor(not_image2, cv2.COLOR_BGR2GRAY)
	black_white_image = cv2.threshold(gray_image, 20, 255, cv2.THRESH_BINARY)[1]
	if(showSteps):
		cv2.imwrite('buf.jpg', gray_image)
		gray_image = cv2.imread("buf.jpg")
		cv2.imwrite('buf.jpg', black_white_image)
		black_white1_image = cv2.imread("buf.jpg")
		imagesList = (image,not_image, gamma_image, bright_image, dilate_image, not_image2, gray_image,black_white1_image)
		nameList = ("Original", "Negative", "Gamma", "Bright", "Dilate", "Negative2", "Gray", "Mask")
		steps.addImages(imagesList, nameList)
	print("Done.")
	return black_white_image
	



