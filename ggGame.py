###### NOTES ######

# World coordinate system and grid both operate on an x, y indexing scheme
# Grid access is col, row
# Mouse coordinates and object positions are x, y

###### SYSTEM IMPORTS ######

import sys
import pdb
import math

###### PYGAME IMPORTS ######

import pygame
import pygame.mouse
import pygame.key
import pygame.time

###### GRIDGAME IMPORTS ######

import ggTools
import ggA_star
from ggGrid import GridPosition
from ggGrid import Grid
from ggUnit import Unit

###### HELPER FUNCTIONS ######

def unitAtGridPosition(gridPosition):
	for unit in current_units:
		if unit.gridPosition == gridPosition:
			return unit
	return None

###### MAIN FUNCTION ######

# Perform initialize and set window/grid size

pygame.init()

print(pygame.display.get_driver())

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

grid = Grid(numcols, numrows, grid_square_size)

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
		grid_pos = grid.findGridSquareForPos(click_pos)

		if keys & pygame.KMOD_SHIFT != 0:
			current_units.append(Unit(grid_pos, "wall"))
			grid.setPosition(grid_pos, True)
		else:
			unit = unitAtGridPosition(grid_pos)
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
		grid_pos = grid.findGridSquareForPos(click_pos)

		if (selected_unit != None):
			unit = unitAtGridPosition(grid_pos)
			if unit == None:
				if (selected_unit.pathStack != None):
					if len(selected_unit.pathStack) > 0:
						if selected_unit.pathStack[0] != grid_pos:
							# print(selected_unit.pathStack[0])
							# print(grid_pos)
							selected_unit.pathStack = ggA_star.Search(selected_unit.gridPosition, grid_pos, grid)
							print("Moving unit to {} {}".format(grid_pos.x, grid_pos.y))
					else:
						selected_unit.pathStack = ggA_star.Search(selected_unit.gridPosition, grid_pos, grid)
						print("Moving unit to {} {}".format(grid_pos.x, grid_pos.y))
				else:
					selected_unit.pathStack = ggA_star.Search(selected_unit.gridPosition, grid_pos, grid)
					print("Moving unit to {} {}".format(grid_pos.x, grid_pos.y))

	# Perform unit movements

	for unit in current_units:
		if unit.type == "player":
			if unit.pathStack != None:
				if len(unit.pathStack) > 0:
					clear_cells.append(unit.gridPosition)
					newGridPos = unit.pathStack.pop()
					grid.setPosition(unit.gridPosition, False)
					unit.gridPosition = newGridPos
					grid.setPosition(unit.gridPosition, True)

	# Clear dirty grid squares

	for cell in clear_cells:
		# print("Clearing: {} {}".format(cell.x, cell.y))
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

	pygame.display.flip()
	# print(clock.tick(60))
	# clock.tick(60)
