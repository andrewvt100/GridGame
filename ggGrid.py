import math

class GridPosition():

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.tup = (x,y)

	def move(self, x, y):
		return GridPosition(self.x + x, self.y + y)

	def __eq__(self, other):
		if other == None:
			return False
		if float(self.x) == float(other.x) and float(self.y) == float(other.y):
			return True
		else:
			return False

	def __ne__(self, other):
		return not self == other

	def __str__(self):
		return "x:{} y:{}".format(self.x, self.y)

	def __hash__(self):
		return hash(self.tup)

class Grid():

	def __init__(self, x, y, square_size):
		self.numrows = int(y)
		self.numcols = int(x)
		self.square_size = square_size
		self.grid = []
		for i in range(self.numcols):
			col = []
			for j in range(self.numrows):
				col.append(False)
			self.grid.append(col)

	def queryPosition(self, gridPosition):
		return self.grid[int(gridPosition.x)][int(gridPosition.y)]

	def setPosition(self, gridPosition, value):

		if (value == True):
			self.grid[int(gridPosition.x)][int(gridPosition.y)] = True
		elif (value == False):
			self.grid[int(gridPosition.x)][int(gridPosition.y)] = False
		else:
			print("Grid.setPosition() error: bad argument")

	def printUnitLocations(self):
		print("BEGIN GRID PRINT")
		for i in range(self.numcols):
			for j in range (self.numrows):
				if self.queryPosition(GridPosition(i,j)) == True:
					print("{} {}".format(i, j))
		print("END GRID PRINT")

	def findGridSquareForPos(self, vector):

		x = math.floor(vector[0] / self.square_size)
		y = math.floor(vector[1] / self.square_size)

		return GridPosition(x, y)