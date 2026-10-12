class GridMap:
    def __init__(self,
                 grid_width: int,
                 grid_height: int):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.grid_matrix = [[0] * self.grid_width for i in range(self.grid_height)]

    def print_grid(self):
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                symbol = self.grid_matrix[row][col]
                print(symbol, end=" ")
            print("\n")

    # Use to draw obstructions on grid
    def set_index_value(self, x, y, value) -> bool:
        if x >= 0 and x < self.grid_width and y >= 0 and y < self.grid_height:
            self.grid_matrix[x][y] = value
            return True
        else:
            return False