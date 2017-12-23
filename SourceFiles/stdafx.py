class AABB:
    def __init__(self, min_x, min_y, max_x, max_y):
        self.min_x, self.min_y = min_x, min_y
        self.max_x, self.max_y = max_x, max_y
    def get_bb(self):
        return self.min_x, self.min_y, self.max_x, self.max_y
    def real_get_bb(self, wl, wb):
        return self.min_x + wl, self.min_y + wb, self.max_x + wl, self.max_y + wb

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True