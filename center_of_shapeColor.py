# import the necessary packages
import statistics
import imutils
import cv2
import numpy as np

def adjust_gamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)

args= {"image" : "img7.jpg"}
gamma = 0.5
ori_image = cv2.imread(args["image"])

image = adjust_gamma(ori_image, gamma)
kernel = np.ones((5, 5), np.uint8)
for i in range(0,5):
    image = cv2.erode(image, kernel) 
#image = cv2.bilateralFilter(image, 40 ,200,  200)
#image = cv2.GaussianBlur(image, (7,7), 0)
#image = cv2.medianBlur(image, 25)
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image = cv2.threshold(image, 30, 255, cv2.THRESH_BINARY)[1]
# find contours in the thresholded image

cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
areas = []

for c in cnts:
		area = cv2.contourArea(c)
		areas.append(area)
		print(area)
		q = len(areas)//2
medianArea = statistics.median(areas[:q])
print("3 kwantyl: ", medianArea)
print("maks: ", max(areas))
for c in cnts:
	#compute the center of the contour
	M = cv2.moments(c)
	area = cv2.contourArea(c)
	if(M["m00"]!=0 and area > medianArea//10 and area > max(areas)//20 ):
		mask = np.zeros(image.shape,np.uint8)
		cv2.drawContours(mask,[c],0,255,-1)
		pixelpoints = np.transpose(np.nonzero(mask))
		mean_val = cv2.mean(ori_image,mask)

		##### draw mean color on tiles
		(x, y, w, h) = cv2.boundingRect(c)
		rect = cv2.minAreaRect(c)
		box = cv2.boxPoints(rect)
		box = np.int0(box)
		im=cv2.drawContours(ori_image,[box],0,mean_val,-1)
		###
		if( mean_val < (0,0,0) ):
				color = "R"
		else:
			color = "O"

		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		#cv2.drawContours(ori_image, [c], -1, (255, 0, 255), 30)
		cv2.circle(ori_image, (cX, cY), 7, (255, 255, 255), -1)
		cv2.putText(ori_image, color, (cX - 20, cY - 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

		
		print(mean_val)

		
		#print(area)



cv2.imwrite("g.png", im) 
#cv2.imwrite("g.png", image) 

#cv2.waitKey(0)
