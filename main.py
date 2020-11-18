# import the necessary packages
import statistics
import imutils
import cv2
import numpy as np
import filter
import colorIdentify


def getAverageColor (image):
	mask = np.zeros(image.shape,np.uint8)
	cv2.drawContours(mask,[c],0,255,-1)
	return cv2.mean(ori_image,mask)

args= {"image" : "img10.jpg"}
ori_image = cv2.imread(args["image"])

cv2.imwrite("g.png", ori_image)

# filtering
image = filter.make_filters(ori_image)
cv2.imwrite("g2.png", image)
# find contours in the thresholded image
cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
areas = []

for c in cnts:
		area = cv2.contourArea(c)
		areas.append(area)
		print(area)
avgColor=0
medianArea = 0
if(len(areas)>1):
	medianArea = statistics.median(areas[:len(areas)//2])
	print("3 kwantyl: ", medianArea)
print("maks: ", max(areas))


ori_image = cv2.cvtColor(ori_image, cv2.COLOR_BGR2HSV)
i=0;
for c in cnts:
	#compute the center of the contour
	M = cv2.moments(c)
	area = cv2.contourArea(c)
	if(M["m00"]!=0 and area > medianArea//10 and area > max(areas)//20 ):
		avgColor = getAverageColor(image)
		
		nameC = colorIdentify.colorName(avgColor)
		nameC = nameC+str(i)
		i+=1
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		cv2.drawContours(ori_image, [c], -1, (160, 255, 255), 10)
		#cv2.circle(ori_image, (cX, cY), 7, (0, 255, 255), -1)
		cv2.putText(ori_image, nameC, (cX - 20, cY - 20),
		cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 10)
		cv2.putText(ori_image, nameC, (cX - 20, cY - 20),
		cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2)
		print(nameC, avgColor )
ori_image = cv2.cvtColor(ori_image, cv2.COLOR_HSV2BGR)
cv2.imwrite("g3.png", ori_image)
		
		#print(area)




#cv2.imwrite("g.png", image) 

#cv2.waitKey(0)
