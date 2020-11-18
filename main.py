# import the necessary packages

import cv2
import numpy as np
import filter
import drawContoures
import colorIdentify
#from skimage import io

directorySource = "./source/"
directoryResult = "./result/"
nameList=[]
singlePhoto = "white4.jpg"
loop = False
showParam = True
if( loop ):
	for i in range (1,8):
		nameList.append("img"+str(i)+".jpg")
else:
	nameList.append(singlePhoto)

for name in nameList:
	## wczytanie obrazu
	ori_image = cv2.imread(directorySource+name)
	original = ori_image
	print("Processing... ", name)
	## obraz jest wybielony, zanegowany (z bieli na czern) i wyciagniec
	bright_image = filter.brightFilter(ori_image)
	##znalezienie konturow
	cnts = drawContoures.findContour(bright_image)
	##znalezienie pol
	areas = drawContoures.findAreas(cnts, showParam)
	##znalezienie najwiekszego konturu - kostka
	contourCube = drawContoures.getMaxContour(cnts,areas)
	## usuniecie tla z obrazu
	
	cube_img = filter.eraseBackground(ori_image, contourCube)
	cv2.imwrite(directoryResult+"F3i2inal_"+name, cube_img)
	#######################
	#cv2.imwrite(directoryResult+"Fiinal_"+name, img)
	#image = cv2.imread(directoryResult+"Fiinal_"+name)

	dark_image = filter.darkFilter(cube_img)
	cv2.imwrite(directoryResult+"dark.jpg", dark_image)
	
	cnts = drawContoures.findContour(dark_image)
	areas = drawContoures.findAreas(cnts, showParam)
	
	original = cv2.imread(directorySource+name)
	original = filter.increase_sharpness(original, 80)
	#original = filter.adjust_gamma(original, gamma=1.5)
	#ori_image = filter.adjust_gamma(ori_image, gamma=1.5)
			
	original = cv2.cvtColor(ori_image, cv2.COLOR_BGR2HSV)
	original = drawContoures.makeMark(cnts, original, dark_image, areas, showParam)
	
	original = cv2.cvtColor(original, cv2.COLOR_HSV2BGR)
	#ori_image = filter.adjust_gamma(ori_image, gamma=1.5)
	#ori_image = cv2.cvtColor(ori_image, cv2.COLOR_BGR2HSV)
	#ori_image = drawContoures.makeMark([c], ori_image, image, areas,showParam)
	#ori_image = cv2.cvtColor(ori_image, cv2.COLOR_HSV2BGR)
	
	cv2.imwrite(directoryResult+"original.jpg", original)
	
	
	print("Processing done.\n")

#cv2.imwrite("g.png", image) 

#cv2.waitKey(0)
