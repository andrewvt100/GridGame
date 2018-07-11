import heapq

import ggTools
from ggGrid import GridPosition

class AStarNode():

	def __init__(self, gridPos, g, h, parent):
		self.gridPos = gridPos
		self.g = g 		# Total distance traveled to get here
		self.h = h 		# Estimated distance to target node
		self.f = g + h	# "Cost" of node - choose the lowest f
		self.parent = parent

	def __lt__(self, other):
		if other == None:
			return False
		if self.f < other.f:
			return True
		else:
			return False

	def __str__(self):
		return "x:{} y:{} g:{} h:{} f:{}".format(self.gridPos.x, self.gridPos.y, self.g, self.h, self.f)

	def __eq__(self, other):
		selfType = type(self)
		otherType = type(other)
		noneType = type(None)
		if selfType == noneType and otherType == noneType:
			return True
		elif selfType == noneType or otherType == noneType:
			return False
		return (self.gridPos == other.gridPos)

	def __hash__(self):
		return hash(self.gridPos)


def Search(startPos, endPos, grid):

	firstNode = AStarNode(startPos, 0, ggTools.euclideanDistance(startPos, endPos), None)

	heap = []
	open_set = set([firstNode])
	closed_set = set()
	heapq.heappush(heap, firstNode)
	
	closed_list = []

	done = False
	moveStack = []

	while len(heap) != 0 and not done:

		best_node = heapq.heappop(heap)
		open_set.remove(best_node)

		# grid_square.fill(blue)
		# screen.blit(grid_square, 
		# 	pygame.Rect(
		# 		best_node.gridPos.x * grid_square_size, 
		# 		best_node.gridPos.y * grid_square_size, 
		# 		grid_square_size, 
		# 		grid_square_size
		# 	)
		# )
		# pygame.event.pump()
		# pygame.display.update()

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
						final_node = AStarNode(gridPos, best_node.g + 1, ggTools.euclideanDistance(gridPos, endPos), best_node)
						next_node = final_node					
						while(next_node.parent != None):
							moveStack.append(next_node.gridPos)
							next_node = next_node.parent
						moveStack.append(next_node.gridPos)
						break
				if (grid.queryPosition(gridPos) == False):
					newNode = AStarNode(gridPos, best_node.g + 1, ggTools.euclideanDistance(gridPos, endPos), best_node)
					if (newNode not in open_set and newNode not in closed_set):
						heapq.heappush(heap, newNode)
						open_set.add(newNode)
		closed_list.append(best_node)
		closed_set.add(best_node)

	return moveStack

def AStarSearch_alternate(startPos, endPos, grid):

	heap = []
	firstNode = AStarNode(startPos, 0, ggTools.euclideanDistance(startPos, endPos), None)
	heapq.heappush(heap, firstNode)
	
	closed_list = []

	done = False
	moveStack = []

	while len(heap) != 0 and not done:

		best_node = heapq.heappop(heap)

		grid_square.fill(blue)
		screen.blit(grid_square, 
			pygame.Rect(
				best_node.gridPos.x * grid_square_size, 
				best_node.gridPos.y * grid_square_size, 
				grid_square_size, 
				grid_square_size
			)
		)

		pygame.event.pump()
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
						final_node = AStarNode(gridPos, best_node.g + 1, ggTools.euclideanDistance(gridPos, endPos), best_node)
						next_node = final_node					
						while(next_node.parent != None):
							moveStack.append(next_node)
							next_node = next_node.parent
						moveStack.append(next_node)
						break
				if (grid.queryPosition(gridPos) == False):
					newNode = AStarNode(gridPos, best_node.g + 1, ggTools.euclideanDistance(gridPos, endPos), best_node)
					isNodeValid = True
					for index, open_node in enumerate(heap):
						if open_node.gridPos == gridPos:
							# The line below should be uncommented, but testing an alternate version of the algorithm
							# if open_node.g >= newNode.g:
							isNodeValid = False
					for index, closed_node in enumerate(closed_list):
						if closed_node.gridPos == gridPos:
							# The line below should be uncommented, but testing an alternate version of the algorithm
							# if closed_node.g >= newNode.g:
							isNodeValid = False
					if (isNodeValid):
						heapq.heappush(heap, AStarNode(gridPos, best_node.g + 1, ggTools.euclideanDistance(gridPos, endPos), best_node))
		closed_list.append(best_node)

	return moveStack

def heuristic(a, b):
	return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

def astar(grid, startPos, goalPos):

	start = (startPos.x, startPos.y)
	goal = (goalPos.x, goalPos.y)

	neighbors = [(0,1),(0,-1),(1,0),(-1,0)]	
	# neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]	

	close_set = set()
	came_from = {}
	gscore = {start:0}
	fscore = {start:heuristic(start, goal)}
	oheap = []

	heappush(oheap, (fscore[start], start))

	counter = 0
	
	while oheap:

		# print(len(oheap))

		current = heappop(oheap)[1]

		grid_square.fill(blue)
		screen.blit(grid_square, 
			pygame.Rect(
				current[0] * grid_square_size, 
				current[1] * grid_square_size, 
				grid_square_size, 
				grid_square_size
			)
		)

		pygame.event.pump()
		pygame.display.update()

		if current == goal:
			data = []
			while current in came_from:
				data.append(current)
				current = came_from[current]
			print(counter)
			return data

		close_set.add(current)
		for i, j in neighbors:
			neighbor = current[0] + i, current[1] + j            
			tentative_g_score = gscore[current] + heuristic(current, neighbor)
			if 0 <= neighbor[0] < grid.numcols:
				if 0 <= neighbor[1] < grid.numrows:                
					if grid.queryPosition(GridPosition(neighbor[0], neighbor[1])) == True:
						continue
				else:
					# array bound y walls
					continue
			else:
				# array bound x walls
				continue
				
			if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
				continue

			addedNeighbor = False

			if neighbor in [i[1]for i in oheap]:
				addedNeighbor = True
				
			if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
				came_from[neighbor] = current
				gscore[neighbor] = tentative_g_score
				fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
				heappush(oheap, (fscore[neighbor], neighbor))
				if addedNeighbor:
					print("Added a duplicate node with a better gscore") 
				
		counter+=1
	
	return False