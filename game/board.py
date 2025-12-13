from typing import List, Tuple

BOARD_N = 9  # default size (9x9)

class Board:
    def __init__(self, size: int = BOARD_N):
        self.size = size
        s = size - 1
        self.h_walls: List[List[bool]] = [[False]*s for _ in range(s)]
        self.v_walls: List[List[bool]] = [[False]*s for _ in range(s)]

    def inside(self, r: int, c: int) -> bool:
        return 0 <= r < self.size and 0 <= c < self.size

    def can_place_horizontal(self, wr: int, wc: int) -> bool:
        s = self.size - 1
        if not (0 <= wr < s and 0 <= wc < s):
            return False
        # can't place where one already exists
        if self.h_walls[wr][wc]:
            return False
        return True

    def can_place_vertical(self, wr: int, wc: int) -> bool:
        s = self.size - 1
        if not (0 <= wr < s and 0 <= wc < s):
            return False
        if self.v_walls[wr][wc]:
            return False
        return True

    def place_horizontal(self, wr:int, wc:int) -> None:
        self.h_walls[wr][wc] = True

    def place_vertical(self, wr:int, wc:int) -> None:
        self.v_walls[wr][wc] = True

    def remove_horizontal(self, wr:int, wc:int) -> None:
        self.h_walls[wr][wc] = False

    def remove_vertical(self, wr:int, wc:int) -> None:
        self.v_walls[wr][wc] = False

    def is_blocked(self, r1:int, c1:int, r2:int, c2:int) -> bool:
        if not (self.inside(r1,c1) and self.inside(r2,c2)):
            return True
        dr = r2 - r1
        dc = c2 - c1
        if abs(dr) + abs(dc) != 1:
            return True  # non-adjacent
        # Moving down
        if dr == 1 and dc == 0:
            s = self.size - 1
            if 0 <= r1 < s and 0 <= c1 < s and self.h_walls[r1][c1]:
                return True
            if 0 <= r1 < s and 0 <= (c1-1) < s and self.h_walls[r1][c1-1]:
                return True
            return False
        # Moving up
        if dr == -1 and dc == 0:
            s = self.size - 1
            if 0 <= r2 < s and 0 <= c2 < s and self.h_walls[r2][c2]:
                return True
            if 0 <= r2 < s and 0 <= (c2-1) < s and self.h_walls[r2][c2-1]:
                return True
            return False
        # Moving right
        if dc == 1 and dr == 0:
            s = self.size - 1
            if 0 <= r1 < s and 0 <= c1 < s and self.v_walls[r1][c1]:
                return True
            if 0 <= (r1-1) < s and 0 <= c1 < s and self.v_walls[r1-1][c1]:
                return True
            return False
        # Moving left
        if dc == -1 and dr == 0:
            s = self.size - 1
            if 0 <= r2 < s and 0 <= c2 < s and self.v_walls[r2][c2]:
                return True
            if 0 <= (r2-1) < s and 0 <= c2 < s and self.v_walls[r2-1][c2]:
                return True
            return False
        return True
