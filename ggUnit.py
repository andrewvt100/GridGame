class Unit():
    
    def __init__(self, gridPosition, type):
        self.gridPosition = gridPosition
        self.pathStack = None
        self.type = type