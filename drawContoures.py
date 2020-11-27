
import cv2
import numpy as np
import colorIdentify
import statistics
import imutils

def getAverageColor (ori_image, image, c):
	kernel = np.ones((5, 5), np.uint8)
	mask = np.zeros(image.shape,np.uint8)
	cv2.drawContours(mask,[c],0,255,-1)
	
	image = cv2.erode(image,kernel,iterations = 5)
	val = cv2.mean(ori_image,mask)
	return val

def findContour(image):
	cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL,
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

def makeMark(cnts, ori_image, image, areas, showParam, showSteps, steps):
	
	print("Contouring...", end = '')
	i=0
	if(showSteps):
		colored = ori_image.copy()
	for c in cnts:
		avgColor=0
		minArea=0.0
		countAreas = len(areas)
		if(countAreas < 60):
			minArea=3400.0
		M = cv2.moments(c)
		area = cv2.contourArea(c)
		if(M["m00"]!=0 and area>= minArea):
			avgColor = getAverageColor(ori_image, image, c)
			nameC = colorIdentify.colorName(avgColor)
			#nameC = nameC+str(i)
			i+=1
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
			
			
			if(showSteps):
				(x, y, w, h) = cv2.boundingRect(c)
				rect = cv2.minAreaRect(c)
				box = cv2.boxPoints(rect)
				box = np.int0(box)
				colored=cv2.drawContours(colored,[box],0,avgColor,-1)
			
			cv2.drawContours(ori_image, [c], -1, (160, 255, 255), 5)
			
		

			cv2.circle(ori_image, (cX, cY), 12, (0, 255, 255), -1)
			cv2.putText(ori_image, nameC, (cX - 20, cY - 20),
			cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 10)
			cv2.putText(ori_image, nameC, (cX - 20, cY - 20),
			cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2)
			if( showParam ):
				print(nameC, area, avgColor )
		
	if(showSteps):
		colored = cv2.cvtColor(colored, cv2.COLOR_HSV2BGR)
		steps.addImages([colored], ["Colored"])
	
	print("Done.")
	return ori_image
