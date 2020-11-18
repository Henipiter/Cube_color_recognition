import numpy as np
import cv2

colorStruct = []

blue = ( (80,50,50), (130,255,255), "B")
green = ((35,50,50), (80,255,255), "G")

ured = ( (0,50,50), (7,255,255), "R")
dred = ( (170,50,50), (179,255,255), "R")
orange =( (7,50,50), (20,255,255), "O" )

yellow = ( (20,50,50) , (35,255,255), "Y")
white = ( (0,0,50), (180,50,255), "W")


colorStruct.append(blue)
colorStruct.append(green)
colorStruct.append( ured)
colorStruct.append( dred)
colorStruct.append(orange)
colorStruct.append(  yellow)
colorStruct.append(white)



def colorName(color):

	for i in colorStruct:
		if( i[0][0] <= color[0] < i[1][0] and i[0][1] <= color[1] < i[1][1] and i[0][2] <= color[2] < i[1][2]):
			return i[2]
	return "Z"


	
		#		color = "R"
		#else:
	#		color = "O"

