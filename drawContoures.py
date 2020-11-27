
import cv2
import numpy as np
import colorIdentify
import statistics
import imutils

def getAverageColor (ori_image, image, c):
	
	kernel = np.ones((5, 5), np.uint8)
	mask = np.zeros(ori_image.shape,np.uint8)
	cv2.drawContours(mask,[c],0,255,-1)
	mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
	mask = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY)[1]
	#image = cv2.erode(image,kernel,iterations = 5)
	cv2.imwrite("mask.jpg", mask)
	val = cv2.mean(ori_image,mask)
	return val


def find_contours_and_centers(img_input):

    img_gray = cv2.cvtColor(img_input, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.bilateralFilter(img_gray, 3, 27,27)
    #(T, thresh) = cv2.threshold(img_input, 0, 100, 0)
    contours_raw, hierarchy = cv2.findContours(img_gray, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = [i for i in contours_raw if cv2.contourArea(i) > 20]
    contour_centers = []

    for idx, c in enumerate(contours):
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        samp_bounds = cv2.boundingRect(c)
        contour_centers.append(((cX,cY), samp_bounds))

    print("{0} contour centers and bounds found".format(len(contour_centers)))

    contour_centers = sorted(contour_centers, key=lambda x: x[0])

    return (contours, contour_centers)

def findContour(image):

	cnts = cv2.findContours(image.copy(), cv2.RETR_TREE,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	return cnts

def findAreas(cnts,showParam):
	areas=[]
	for c in cnts:
		area = cv2.contourArea(c)
		areas.append(area)
		if(showParam):
			print(area)
	return areas

def getMaxContour (cnts, areas):
	return cnts[ areas.index(max(areas))   ]

def makeMark(cnts, ori_image, image, areas, showParam):
	i=0
	for c in cnts:
		#compute the center of the contour
		avgColor=0
		minArea=0.0
		countAreas = len(areas)
		if(countAreas < 60):
			minArea=3400.0
		M = cv2.moments(c)
		area = cv2.contourArea(c)
		if(M["m00"]!=0 and area>= minArea): #area > max(areas)//20 ):
			avgColor = getAverageColor(ori_image, image, c)
			nameC = colorIdentify.colorName(avgColor)
			nameC = nameC+str(i)
			i+=1
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
			(x, y, w, h) = cv2.boundingRect(c)
			rect = cv2.minAreaRect(c)
			box = cv2.boxPoints(rect)
			box = np.int0(box)
			#ori_image=cv2.drawContours(ori_image,[box],0,avgColor,-1)
			###
			cv2.drawContours(ori_image, [c], -1, (160, 255, 255), 5)
			cv2.circle(ori_image, (cX, cY), 12, (0, 255, 255), -1)
			cv2.putText(ori_image, nameC, (cX - 20, cY - 20),
			cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 10)
			cv2.putText(ori_image, nameC, (cX - 20, cY - 20),
			cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2)
			if( showParam ):
				print(nameC, area, avgColor )

		
	cv2.imwrite("mask2.jpg", ori_image)
	
	cv2.imwrite("mask3.jpg", image)
	return ori_image
