# import the necessary packages

import cv2
import numpy as np
import filter
import drawContoures
import colorIdentify
import glob
#from skimage import io

directorySource = "./source1/"
directoryResult = "./result/"
nameList=[]
singlePhoto = "kosc.jpg"
loop = False
showParam = True
if( loop ):
	for i in glob.glob(directorySource+"b*.jpg"):
		i = i[10:]
		nameList.append(i)
else:
	nameList.append(singlePhoto)

for name in nameList:
	## wczytanie obrazu
	ori_image = cv2.imread(directorySource+name)
	hsv = cv2.cvtColor(ori_image, cv2.COLOR_BGR2HSV)
	average = hsv.mean(axis=0).mean(axis=0)
	if(average[2]<120):
		dark = True
	else:
		dark = False
	image = ori_image 
	
	image = filter.adjust_gamma(image, 1.5)
	cnts = filter.selectColors(image)
	blackwhite_image = np.full(image.shape, 255, dtype=np.uint8)
	areas = drawContoures.findAreas(cnts,showParam)
	for c in cnts:
		area = cv2.contourArea(c)
		i=0
		if( 100<= area <=100000):
			cv2.imwrite("mask.jpg", image)
			original = cv2.imread(directorySource+name)
			#original = filter.increase_sharpness(original, 80)
			#original = filter.adjust_gamma(original, gamma=1.5)
			cv2.drawContours(ori_image, [c], -1, (160, 255, 255), 5)
	
	cv2.imwrite("mask.jpg", ori_image)
	for c in cnts:
		area = cv2.contourArea(c)
		i=0
		if( 1000<= area <=100000):
			cv2.imwrite("mask.jpg", image)
			original = cv2.imread(directorySource+name)
			#original = filter.increase_sharpness(original, 80)
			#original = filter.adjust_gamma(original, gamma=1.5)
			cv2.drawContours(ori_image, [c], -1, (160, 255, 255), 5)
			
			cv2.imwrite("mask.jpg", ori_image)
			ori_image = cv2.cvtColor(ori_image, cv2.COLOR_BGR2HSV)
			avgColor = drawContoures.getAverageColor(ori_image, image, c)
			nameC = colorIdentify.colorName(avgColor)
			nameC = nameC+str(i)
			i+=1
			
			M = cv2.moments(c)
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
			(x, y, w, h) = cv2.boundingRect(c)
			rect = cv2.minAreaRect(c)
			box = cv2.boxPoints(rect)
			box = np.int0(box)
			#ori_image=cv2.drawContours(ori_image,[box],0,avgColor,-1)
			###
			
			cv2.circle(ori_image, (cX, cY), 12, (0, 255, 255), -1)
			cv2.putText(ori_image, nameC, (cX - 20, cY - 20),
			cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 10)
			cv2.putText(ori_image, nameC, (cX - 20, cY - 20),
			cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2)
			
			original = cv2.cvtColor(ori_image, cv2.COLOR_HSV2BGR)
			#cv2.drawContours(image, [c], -1, (255, 0, 255), 15)
			cv2.imwrite("mask.jpg", original)
	
	
	
	##########################
	print("Processing... ", name)

	
	blackwhite_image = filter.darkBackground(ori_image)
	
	
	cnts = drawContoures.findContour(blackwhite_image)
	areas = drawContoures.findAreas(cnts, showParam)
	
	cv2.imwrite(directoryResult+"Mask_"+name, blackwhite_image)
	original = cv2.imread(directorySource+name)
	original = cv2.cvtColor(original, cv2.COLOR_BGR2HSV)
	original = drawContoures.makeMark(cnts, original, blackwhite_image, areas, showParam)
	original = cv2.cvtColor(original, cv2.COLOR_HSV2BGR)
	
	cv2.imwrite(directoryResult+"Final_"+name, original)
	
	
	print("Processing done.\n")

#cv2.imwrite("g.png", image) 

#cv2.waitKey(0)
