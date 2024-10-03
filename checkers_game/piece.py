class Piece:
    def __init__(self, color, position, is_king = False):
        self.color = color
        self.position = position
        self.is_king = is_king

    def make_king(self):
        self.is_king = True

    def move(self, new_position):
        self.position = new_position