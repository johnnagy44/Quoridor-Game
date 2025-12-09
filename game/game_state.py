from typing import List, Tuple, Optional
from copy import deepcopy
from .board import Board
from .player import Player
from .rules import legal_moves
from .pathfinding import bfs_has_path

class GameState:
    """
    High-level game state API to manage players, turns, moves, and wall placements.
    UI should call these methods. GameState is independent of PyQt.
    """
    def __init__(self, size: int = 9):
        self.board = Board(size)
        mid = size // 2
        self.players: List[Player] = [
            Player(0, mid, walls=10, is_ai=False, id=0),
            Player(size-1, mid, walls=10, is_ai=False, id=1)
        ]
        self.current: int = 0
        self.winner: Optional[int] = None
        self.history: List[dict] = []  # simple history for undo (shallow serializable snapshots)

    def clone(self) -> 'GameState':
        return deepcopy(self)

    def serialize(self) -> dict:
        return {
            'board': {
                'h': [row[:] for row in self.board.h_walls],
                'v': [row[:] for row in self.board.v_walls],
                'size': self.board.size
            },
            'players': [p.__dict__ for p in self.players],
            'current': self.current,
            'winner': self.winner
        }

    def save_snapshot(self):
        self.history.append(self.serialize())

    def undo(self) -> bool:
        if not self.history:
            return False
        snap = self.history.pop()
        # restore
        b = snap['board']
        self.board.h_walls = [row[:] for row in b['h']]
        self.board.v_walls = [row[:] for row in b['v']]
        self.board.size = b['size']
        for i, pdata in enumerate(snap['players']):
            self.players[i].r = pdata['r']
            self.players[i].c = pdata['c']
            self.players[i].walls = pdata['walls']
            self.players[i].is_ai = pdata.get('is_ai', False)
            self.players[i].id = pdata.get('id', i)
        self.current = snap['current']
        self.winner = snap['winner']
        return True

    def inside(self, r:int, c:int) -> bool:
        return self.board.inside(r, c)

    def legal_moves(self, player_index: int):
        return legal_moves(self.board, self.players, player_index)

    def move_pawn(self, player_index: int, r: int, c: int) -> bool:
        if self.winner is not None:
            return False
        if player_index != self.current:
            return False
        moves = self.legal_moves(player_index)
        if (r, c) not in moves:
            return False
        # snapshot for undo
        self.save_snapshot()
        p = self.players[player_index]
        p.r = r
        p.c = c
        # check win
        if player_index == 0 and r == self.board.size - 1:
            self.winner = 0
        if player_index == 1 and r == 0:
            self.winner = 1
        self.current = 1 - self.current
        return True

    def can_place_wall(self, orientation: str, wr: int, wc: int) -> bool:
        s = self.board.size - 1
        if not (0 <= wr < s and 0 <= wc < s):
            return False
        if orientation == 'H':
            if not self.board.can_place_horizontal(wr, wc):
                return False
        else:
            if not self.board.can_place_vertical(wr, wc):
                return False
        # also don't allow placement on top of existing wall
        if orientation == 'H' and self.board.h_walls[wr][wc]:
            return False
        if orientation == 'V' and self.board.v_walls[wr][wc]:
            return False
        return True

    def try_place_wall(self, player_index: int, orientation: str, wr: int, wc: int) -> bool:
        """
        Attempt to place a wall for player_index. This method performs:
        - basic bounds/overlap checks
        - tentative placement
        - BFS path check for all players
        - commit or revert, decrement walls, switch turn
        """
        if self.winner is not None:
            return False
        if player_index != self.current:
            return False
        p = self.players[player_index]
        if p.walls <= 0:
            return False
        if not self.can_place_wall(orientation, wr, wc):
            return False
        # tentative
        if orientation == 'H':
            self.board.place_horizontal(wr, wc)
        else:
            self.board.place_vertical(wr, wc)
        # path check for every player
        ok = True
        for pl in self.players:
            goal_rows = [self.board.size - 1] if pl is self.players[0] else [0]
            if not bfs_has_path(self.board, (pl.r, pl.c), goal_rows):
                ok = False
                break
        if not ok:
            # revert
            if orientation == 'H':
                self.board.remove_horizontal(wr, wc)
            else:
                self.board.remove_vertical(wr, wc)
            return False
        # commit
        self.save_snapshot()
        p.walls -= 1
        self.current = 1 - self.current
        return True

    def get_winner(self) -> Optional[int]:
        return self.winner
