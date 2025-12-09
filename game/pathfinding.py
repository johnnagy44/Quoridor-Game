from collections import deque
from typing import Tuple, List, Optional
from .board import Board

def bfs_has_path(board: Board, start: Tuple[int,int], goal_rows: List[int]) -> bool:
    """Return True if any cell in goal_rows is reachable from start (row in goal_rows)."""
    q = deque([start])
    visited = set()
    while q:
        r, c = q.popleft()
        if (r, c) in visited:
            continue
        visited.add((r, c))
        if r in goal_rows:
            return True
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            if not board.inside(nr, nc):
                continue
            if board.is_blocked(r, c, nr, nc):
                continue
            if (nr, nc) not in visited:
                q.append((nr, nc))
    return False

def bfs_shortest_path_length(board: Board, start: Tuple[int,int], goal_rows: List[int]) -> Optional[int]:
    """
    Return shortest number of steps to reach any cell with row in goal_rows.
    If no path, return None.
    """
    q = deque([(start, 0)])
    visited = set()
    while q:
        (r, c), d = q.popleft()
        if (r, c) in visited:
            continue
        visited.add((r, c))
        if r in goal_rows:
            return d
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            if not board.inside(nr, nc):
                continue
            if board.is_blocked(r, c, nr, nc):
                continue
            if (nr, nc) not in visited:
                q.append(((nr, nc), d+1))
    return None
