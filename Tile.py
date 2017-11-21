class Tile():
    tilesize = 0
    def __init__(self, x, y, tilesize, tileheight):
        self.x = (x * tilesize + (x + 1) * tilesize) / 2
        self.y = ((tileheight - y) * tilesize + (tileheight - (y + 1)) * tilesize) / 2
        self.tilesize = tilesize
    def get_bb(self):
        return self.x - self.tilesize/2, self.y - self.tilesize/2, self.x + self.tilesize/2, self.y + self.tilesize/2