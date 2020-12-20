from matplotlib.image import imread

class Image():

    def __init__(self,image_path):
        self.pixels = self.image_parse(image_path)

    def image_parse(self, image_path):
        return imread(image_path)
    
    def height(self):
        return len(self.pixels) -1
    
    def width(self):
        return len(self.pixels[0]) -1
    
    def bounds(self):
        return (self.width, self.height)


    def __iter__(self):
        for x in range(0,self.height()):
            for y in range(0,self.width()):
                yield(self.ring(row=x, column=y))

    def pixel(self, row, column):
        self.pixels[row][column]


    def ring(self, row, column):
        ring = [ self.rep(i,j) if ((i != None) & (j != None)) else '' for i in self.row_range(row) for j in self.column_range(column) ]
        center = ring.pop(4)
        return (center,":".join(ring))
        
    def row_range(self, row):
        if row == 0:
            r = [None,0, 1] 
        elif row == self.height():
            r = [row -1, row, None]
        else:
            r = range(row - 1, row + 2)
        return r
    
    def column_range(self, column):
        if column == 0:
            c = [None,0, 1] 
        elif column == self.width():
            c = [column -1, column, None]
        else:
            c = range(column - 1, column + 2)
        return c 

    def rep(self,i,j):
        return '%02x%02x%02x' % tuple(self.pixels[i][j])

    