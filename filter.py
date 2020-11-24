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

def increase_sharpness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    lim = 255 - value
    s[s > lim] = 255
    s[s <= lim] += value
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img


def getBlackElem(image):
	
	kernel = np.ones((5, 5), np.uint8)
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	lower_black = np.array([0,0,0])
	upper_black = np.array([179,255,30])
	mask = cv2.inRange(hsv, lower_black, upper_black)
	background = np.full(image.shape, 255, dtype=np.uint8)
	res = cv2.bitwise_and(background,background, mask=mask)
	image = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
	image = cv2.threshold(image, 10, 255, cv2.THRESH_BINARY)[1]
	image = cv2.dilate(image,kernel,iterations = 2)
	cv2.imwrite("frame.jpg", image)
	return image


def eraseBackground(img,c):
	fill_color = [0, 0, 0]
	mask_value = 255
	stencil  = np.zeros(img.shape[:-1]).astype(np.uint8)
	cv2.fillPoly(stencil, [c], mask_value)
	sel = stencil != mask_value
	img[sel] = fill_color   
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
		steps.addImages(imagesList)
	print("Done.")
	return black_white_image
	

def brightBackground(ori_image):

	kernel = np.ones((5, 5), np.uint8)
	
	image = cv2.bitwise_not(ori_image)
	image = adjust_gamma(image, 0.5)
	image = increase_brightness(image, -50)
	
	image = cv2.dilate(image,kernel,iterations = 8)
	cv2.imwrite("dark.jpg", image)
	print("Gray filter...", end = '')
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	image = cv2.threshold(image, 20, 255, cv2.THRESH_BINARY)[1]
	print(" Done.")
	cv2.imwrite("nal.jpg", image)
	cnts = drawContoures.findContour(image)
	##znalezienie pol
	areas = drawContoures.findAreas(cnts, False)
	##znalezienie najwiekszego konturu - kostka
	contourCube = drawContoures.getMaxContour(cnts,areas)
	## usuniecie tla z obrazu
	
	image = eraseBackground(ori_image, contourCube)
	cv2.imwrite("nalww.jpg", image)
	return image

