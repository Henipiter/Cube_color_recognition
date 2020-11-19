# import the necessary packages

import cv2
import numpy as np
import filter
import drawContoures
import colorIdentify
import glob
#from skimage import io

directorySource = "./source/"
directoryResult = "./result/"
nameList=[]
singlePhoto = "white1.jpg"
loop = True
showParam = False
if( loop ):
	for i in glob.glob(directorySource+"*.jpg"):
		i = i[9:]
		nameList.append(i)

	#for i in range (1,18):
		#nameList.append("white"+str(i)+".jpg")
else:
	nameList.append(singlePhoto)

#for i in glob.glob(directorySource+"*.jpg"):
#	print(i, end =' ')
#	img = cv2.imread(i)
#	
#	img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#	average = img.mean(axis=0).mean(axis=0)
#	print(average)
	



for name in nameList:
	## wczytanie obrazu
	ori_image = cv2.imread(directorySource+name)
	hsv = cv2.cvtColor(ori_image, cv2.COLOR_BGR2HSV)
	average = hsv.mean(axis=0).mean(axis=0)
	if(average[2]<120):
		dark = True
	else:
		dark = False

	print("Processing... ", name)
	## obraz jest wybielony, zanegowany (z bieli na czern) i wyciagniec
	#bright_image = filter.getBlackElem(ori_image)
	if(not dark):
		ori_image = filter.brightBackground(ori_image)


	blackwhite_image = filter.darkBackground(ori_image)
	
		#ori_image = image = cv2.bitwise_not(ori_image)
		
		#dark_image = filter.darkFilter(ori_image)


	#cv2.imwrite(directoryResult+"Mask_"+name, cube_img)

	##znalezienie konturow
	#cnts = drawContoures.findContour(bright_image)
	##znalezienie pol
	#areas = drawContoures.findAreas(cnts, showParam)
	##znalezienie najwiekszego konturu - kostka
	#contourCube = drawContoures.getMaxContour(cnts,areas)
	## usuniecie tla z obrazu
	
	#cube_img = filter.eraseBackground(ori_image, contourCube)



	#######################
	#cv2.imwrite(directoryResult+"Fiinal_"+name, img)
	#image = cv2.imread(directoryResult+"Fiinal_"+name)

	#dark_image = filter.darkFilter(cube_img)
	
	cnts = drawContoures.findContour(blackwhite_image)
	areas = drawContoures.findAreas(cnts, showParam)
	
	cv2.imwrite(directoryResult+"Mask_"+name, blackwhite_image)
	original = cv2.imread(directorySource+name)
	#original = filter.increase_sharpness(original, 80)
	#original = filter.adjust_gamma(original, gamma=1.5)
			
	original = cv2.cvtColor(original, cv2.COLOR_BGR2HSV)
	original = drawContoures.makeMark(cnts, original, blackwhite_image, areas, showParam)
	original = cv2.cvtColor(original, cv2.COLOR_HSV2BGR)
	#ori_image = filter.adjust_gamma(ori_image, gamma=1.5)
	#ori_image = cv2.cvtColor(ori_image, cv2.COLOR_BGR2HSV)
	#ori_image = drawContoures.makeMark([c], ori_image, image, areas,showParam)
	#ori_image = cv2.cvtColor(ori_image, cv2.COLOR_HSV2BGR)
	
	cv2.imwrite(directoryResult+"Final_"+name, original)
	
	
	print("Processing done.\n")

#cv2.imwrite("g.png", image) 

#cv2.waitKey(0)
