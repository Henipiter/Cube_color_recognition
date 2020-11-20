import numpy as np
import cv2

colorStruct = []

blue = ( (82,70,50), (130,255,255), "B")
green = ((40,70,50), (82,255,255), "G")

ured = ( (0,70,50), (7,255,255), "R")
dred = ( (130,70,50), (179,255,255), "R")
orange =( (7,70,50), (21,255,255), "O" )

yellow = ( (21,70.5,50) , (40,255,255), "Y")
white = ( (0,0,50), (180,255,255), "W")


colorStruct.append(blue)
colorStruct.append(green)
colorStruct.append(ured)
colorStruct.append(dred)
colorStruct.append(orange)
colorStruct.append(yellow)
colorStruct.append(white)



def colorName(color):

	for i in colorStruct:
		if( i[0][0] <= color[0] < i[1][0] and i[0][1] <= color[1] < i[1][1] and i[0][2] <= color[2] < i[1][2]):
			return i[2]
	return "Z"
