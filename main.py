# import the necessary packages

import cv2
import numpy as np
import filter
import drawContoures
import colorIdentify
import glob
import images

loop = False
showParam = False
showStep = False
singlePhoto = "hard1.jpg"

directorySource = "./hard/"
directoryResult = "./hard/"
nameList=[]
steps = images.ImageList()
if( loop ):
	for i in glob.glob(directorySource+"*.jpg"):
		print(i)
		i = i[len(directorySource):]
		nameList.append(i)
	showStep = False

else:
	nameList.append(singlePhoto)


for name in nameList:
	ori_image = cv2.imread(directorySource+name)
	print("Processing... ", name)
	blackwhite_image = filter.darkBackground(ori_image, showStep, steps)
	cnts = drawContoures.findContour(blackwhite_image)
	areas = drawContoures.findAreas(cnts, showParam)
	cv2.imwrite(directoryResult+"Mask_"+name, blackwhite_image)
	original = cv2.imread(directorySource+name)

	original = cv2.cvtColor(original, cv2.COLOR_BGR2HSV)
	original = drawContoures.makeMark(cnts, original, blackwhite_image, areas, showParam, showStep, steps)
	original = cv2.cvtColor(original, cv2.COLOR_HSV2BGR)

	cv2.imwrite(directoryResult+"Final_"+name, original)
	if(showStep):
		steps.addImages([original], ["Final"])
		steps.concat()
	print("Processing done.\n")


