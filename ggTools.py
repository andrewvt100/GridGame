import math
from random import randint

def magnitude(vector):

	return math.sqrt(vector[0]*vector[0] + vector[1] * vector[1])

def euclideanDistance(gridPosA, gridPosB):

	# return math.sqrt( 
	# 	(gridPosB.x - gridPosA.x)*(gridPosB.x - gridPosA.x) + 
	# 	(gridPosB.y - gridPosA.y)*(gridPosB.y - gridPosA.y)
	# )

	return (gridPosB.x - gridPosA.x)*(gridPosB.x - gridPosA.x) + (gridPosB.y - gridPosA.y)*(gridPosB.y - gridPosA.y)


def normalize(vector):
   
	length = magnitude(vector)

	return_vector = [0,0]

	if length != 0:
		return_vector = [vector[0] / length, vector[1] / length]

	return(return_vector)

def randomColor():

	return (randint(0,255),randint(0,255),randint(0,255))
