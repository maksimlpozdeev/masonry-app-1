class Node:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def coord_update(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
