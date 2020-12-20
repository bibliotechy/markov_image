class Pixel():
    def __init__(self, image, row:int, column:int):
        self.image      = image
        self.row:int    = row
        self.column:int = column


    def ring(self):
        labels = ["top_left", "top_mid", "top_right", "mid_left", "mid_right", "bot_left", "bot_mid", "bot_right"]
        coords = [(i, j) for i in self.row_range() for j in self.column_range() 
                if self.not_orig_pixel(i,j)]
        return dict(zip(labels, coords))
        
    def row_range(self):
        return range(self.row - 1, self.row + 2)
    
    def column_range(self):
        return range(self.column - 1, self.column + 2)
    
    def not_orig_pixel(self,i,j):
        return not((self.column == j) & (self.row == i))




