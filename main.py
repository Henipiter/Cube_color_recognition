# import the necessary packages
import statistics
import imutils
import cv2
import numpy as np
import filter
import drawContoures
import colorIdentify
directorySource = "./source/"
directoryResult = "./result/"
nameList=[]
singlePhoto = "img1.jpg"
loop = False
showParam = False
if( loop ):
	for i in range (1,8):
		nameList.append("img"+str(i)+".jpg")
else:
	nameList.append(singlePhoto)

for name in nameList:
	ori_image = cv2.imread(directorySource+name)
	print("Processing... ", name)
	

	# filtering
	image = filter.make_filters(ori_image)
	cv2.imwrite(directoryResult+"Gray_"+name, image)

	# find contours in the thresholded image
	cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	areas = []

	for c in cnts:
			area = cv2.contourArea(c)
			areas.append(area)
			if(showParam):
				print(area)
	avgColor=0
	medianArea = 0
	if(len(areas)>1):
		medianArea = statistics.median(areas[:len(areas)//2])
	if(showParam):
		print("3 kwantyl: ", medianArea)
		print("maks: ", max(areas))


	ori_image = filter.adjust_gamma(ori_image, gamma=1.5)
	ori_image = cv2.cvtColor(ori_image, cv2.COLOR_BGR2HSV)
	ori_image = drawContoures.makeMark(cnts, ori_image, image, medianArea, areas,showParam)
	ori_image = cv2.cvtColor(ori_image, cv2.COLOR_HSV2BGR)

	cv2.imwrite(directoryResult+"Final_"+name, ori_image)
	print("Processing done.\n")

#cv2.imwrite("g.png", image) 

#cv2.waitKey(0)
