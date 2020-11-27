import numpy as np
import cv2

colorStruct = []

boundaries = {}
boundaries["blue"] = ( (82,70,20), (130,255,255), "B")
boundaries["green"] = ((40,70,20), (82,255,255), "G")

boundaries["ured"] = ( (0,70,20), (7,255,255), "R")
boundaries["dred"] = ( (130,70,20), (179,255,255), "R")
boundaries["orange"] =( (7,70,20), (21,255,255), "O" )

boundaries["yellow"] = ( (21,70,20) , (40,255,255), "Y")
boundaries["white"] = ( (0,70,50), (180,255,255), "W")



def colorName(color):

	for x in boundaries:
		i = boundaries[x]
		if( i[0][0] <= color[0] < i[1][0] and i[0][1] <= color[1] < i[1][1] and i[0][2] <= color[2] < i[1][2]):
			return i[2]
	return "Z"

def getBoudary(name):
	return boundaries[name]

def getDictColor():
	return boundaries