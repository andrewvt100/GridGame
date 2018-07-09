###### NOTES ######

# World coordinate system and grid both operate on an x, y indexing scheme
# Grid access is col, row
# Mouse coordinates and object positions are x, y

###### SYSTEM IMPORTS ######

import sys
import math
from random import randint
import pdb
import time

###### PYGAME IMPORTS ######

import pygame
import pygame.mouse
import pygame.key
import pygame.time

###### CONSTANTS ######


###### CLASSES ######

class AStarNode():

	def __init__(self, gridPos, g, h, parent):
		self.gridPos = gridPos
		self.g = g 		# Total distance traveled to get here
		self.h = h 		# Estimated distance to target node
		self.f = g + h	# "Cost" of node - choose the lowest f
		self.parent = parent

class GridPosition():

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def move(self, x, y):
		return GridPosition(self.x + x, self.y + y)

	def __eq__(self, other):
		if other == None:
			return False
		if self.x == other.x and self.y == other.y:
			return True
		else:
			return False

class Grid():

	def __init__(self, x, y):
		self.numrows = int(y)
		self.numcols = int(x)
		self.grid = []
		for i in range(self.numcols):
			col = []
			for j in range(self.numrows):
				col.append(False)
			self.grid.append(col)

	def queryPosition(self, gridPosition):
		return self.grid[gridPosition.x][gridPosition.y]

	def setPosition(self, gridPosition, value):

		if (value == True):
			self.grid[gridPosition.x][gridPosition.y] = True
		elif (value == False):
			self.grid[gridPosition.x][gridPosition.y] = False
		else:
			print("Grid.setPosition() error: bad argument")

	def printUnitLocations(self):
		print("BEGIN GRID PRINT")
		for i in range(self.numcols):
			for j in range (self.numrows):
				if self.queryPosition(GridPosition(i,j)) == True:
					print("{} {}".format(i, j))
		print("END GRID PRINT")

class Unit():
    
    def __init__(self, gridPosition, type):
        self.gridPosition = gridPosition
        self.pathNode = None
        # self.gridMoveBegin = None
        self.gridMoveEnd = None
        self.type = type

###### HELPER FUNCTIONS ######

def magnitude(vector):

	return math.sqrt(vector[0]*vector[0] + vector[1] * vector[1])

def euclideanDistance(gridPosA, gridPosB):

	return math.sqrt( 
		(gridPosB.x - gridPosA.x)*(gridPosB.x - gridPosA.x) + 
		(gridPosB.y - gridPosA.y)*(gridPosB.y - gridPosA.y)
	)

def normalize(vector):
   
	length = magnitude(vector)

	return_vector = [0,0]

	if length != 0:
		return_vector = [vector[0] / length, vector[1] / length]

	return(return_vector)

def randomColor():

	return (randint(0,255),randint(0,255),randint(0,255))

def findGridSquareForPos(vector):

	x = math.floor(vector[0] / grid_square_size)
	y = math.floor(vector[1] / grid_square_size)

	return GridPosition(x, y)

def didHitUnit(gridPosition):
	for unit in current_units:
		if unit.gridPosition == gridPosition:
			return unit
	return None

def AStarSearch(startPos, endPos, grid):

	# pdb.set_trace()
	
	open_list =[AStarNode(startPos, 0, euclideanDistance(startPos, endPos), None)]
	closed_list = []

	done = False
	final_node = None

	while len(open_list) != 0 and not done:
		print(len(open_list))
		best_node = open_list[0]
		for node in open_list:
			if node.f < best_node.f:
				best_node = node
		open_list.remove(best_node)

		grid_square.fill(blue)
		screen.blit(grid_square, 
			pygame.Rect(
				best_node.gridPos.x * grid_square_size, 
				best_node.gridPos.y * grid_square_size, 
				grid_square_size, 
				grid_square_size
			)
		)
		pygame.display.update()

		successors = []
		potential_successors = [
			[best_node.gridPos.x-1, best_node.gridPos.y], 
			[best_node.gridPos.x+1, best_node.gridPos.y], 
			[best_node.gridPos.x, best_node.gridPos.y-1],
			[best_node.gridPos.x, best_node.gridPos.y+1]
		]
		for successor in potential_successors:
			gridPos = GridPosition(successor[0], successor[1])
			if (gridPos.x < grid.numcols) and (gridPos.y < grid.numrows) and (gridPos.x >= 0) and (gridPos.y >= 0):
				if (gridPos == endPos):
						done = True
						final_node = AStarNode(gridPos, best_node.g + 1, euclideanDistance(gridPos, endPos), best_node)
						break
				if (grid.queryPosition(gridPos) == False):
					newNode = AStarNode(gridPos, best_node.g + 1, euclideanDistance(gridPos, endPos), best_node)
					isNodeValid = True
					for index, open_node in enumerate(open_list):
						if open_node.gridPos == gridPos:
							isNodeValid = False
							if open_node.f > newNode.f:
								open_list[index] = AStarNode(gridPos, best_node.g + 1, euclideanDistance(gridPos, endPos), best_node)
					for index, closed_node in enumerate(closed_list):
						if closed_node.gridPos == gridPos:
							isNodeValid = False
							if closed_node.f > newNode.f:
								closed_list[index] = AStarNode(gridPos, best_node.g + 1, euclideanDistance(gridPos, endPos), best_node)
					if (isNodeValid):
						open_list.append(AStarNode(gridPos, best_node.g + 1, euclideanDistance(gridPos, endPos), best_node))
		closed_list.append(best_node)

	return final_node

###### MAIN FUNCTION ######

# Perform initialize and set window/grid size

pygame.init()

clock = pygame.time.Clock()

size = width, height = 1280, 720

black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255

grid_square_size = 10

screen = pygame.display.set_mode(size)

numrows = height / grid_square_size
numcols = width / grid_square_size

grid_square = pygame.Surface((grid_square_size, grid_square_size))

grid = Grid(numcols, numrows)

# Create variables to hold game data

current_units = [Unit(GridPosition(10,10), "player")]
grid.setPosition(current_units[0].gridPosition, True)
selected_unit = None

# Draw all grid squares to initial color

col, row = 0, 0

while row < numrows:
	col = 0
	while col < numcols:
		grid_square.fill(white)
		screen.blit(
			grid_square, 
			pygame.Rect(
				col * grid_square_size, 
				row * grid_square_size, 
				grid_square_size, 
				grid_square_size
			)
		)
		col += 1
	row+=1

pygame.display.flip()

while 1:

	clear_cells = []

	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()

	# Handle left mouse button 

	keys = pygame.key.get_mods()

	if pygame.mouse.get_pressed()[0]:

		click_pos = pygame.mouse.get_pos()
		grid_pos = findGridSquareForPos(click_pos)

		if keys & pygame.KMOD_SHIFT != 0:
			current_units.append(Unit(grid_pos, "wall"))
			grid.setPosition(grid_pos, True)
		else:
			unit = didHitUnit(grid_pos)
			if unit != None:
				if selected_unit != unit:
					selected_unit = unit
					print("Selected unit at {} {}".format(grid_pos.x, grid_pos.y))
			else:
				if selected_unit != None:
					selected_unit = None
					print("Deselected unit")

	# Handle right mouse button

	if pygame.mouse.get_pressed()[2]:

		click_pos = pygame.mouse.get_pos()
		grid_pos = findGridSquareForPos(click_pos)

		if (selected_unit != None):

			unit = didHitUnit(grid_pos)
			if unit == None:

				if selected_unit.gridMoveEnd != grid_pos:

					selected_unit.gridMoveEnd = grid_pos
					print("Moving unit to {} {}".format(grid_pos.x, grid_pos.y))
					selected_unit.pathNode = AStarSearch(selected_unit.gridMoveEnd, selected_unit.gridPosition, grid)

					print("Moving unit to {} {}".format(
						grid_pos.x, grid_pos.y))

	# Perform unit movements

	for unit in current_units:
		if unit.pathNode != None:
			clear_cells.append(unit.gridPosition)
			newGridPos = unit.pathNode.gridPos
			grid.setPosition(unit.gridPosition, False)
			unit.gridPosition = newGridPos
			grid.setPosition(unit.gridPosition, True)
			unit.pathNode = unit.pathNode.parent
		else:
			unit.gridMoveEnd = None

	# Clear dirty grid squares

	for cell in clear_cells:
		print("Clearing: {} {}".format(cell.x, cell.y))
		grid_square.fill(white)
		screen.blit(grid_square, 
			pygame.Rect(
				cell.x * grid_square_size, 
				cell.y * grid_square_size, 
				grid_square_size, 
				grid_square_size
			)
		)

	# Draw all units

	for unit in current_units:
		if unit.type == "player":
			grid_square.fill(red)
		elif unit.type == "wall":
			grid_square.fill(black)
		screen.blit(grid_square, 
			pygame.Rect(
				unit.gridPosition.x * grid_square_size, 
				unit.gridPosition.y * grid_square_size, 
				grid_square_size, 
				grid_square_size
			)
		)

	# grid.printUnitLocations()

	# sleep(1)

	pygame.display.flip()
	clock.tick(100)