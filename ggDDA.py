import ggTools
from ggGrid import GridPosition

def DDA(startPos, endPos):

	# stack of grid positions
	move_stack = [startPos]

	# change in x and y
	dx = endPos.x - startPos.x
	dy = endPos.y - startPos.y

	num_steps = 0

	if abs(dx) > abs(dy):
		num_steps = abs(dx)
	else:
		num_steps = abs(dy)

	x_step = dx / float(num_steps)
	y_step = dy / float(num_steps)

	start_x = startPos.x
	start_y = startPos.y

	for index in range(num_steps):
		start_x = start_x + x_step
		start_y = start_y + y_step
		move_stack.append(GridPosition(round(start_x), round(start_y)))

	return move_stack

