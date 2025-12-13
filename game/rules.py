from typing import List, Tuple
from .board import Board
from .player import Player

def legal_moves(board: Board, players: List[Player], player_index: int) -> List[Tuple[int,int]]:

    p = players[player_index]
    opp = players[1 - player_index]
    r, c = p.r, p.c
    moves = []
    for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
        nr, nc = r+dr, c+dc
        if not board.inside(nr, nc):
            continue
        if board.is_blocked(r, c, nr, nc):
            continue
        # neighbor occupied by opponent?
        if (nr, nc) == (opp.r, opp.c):
            # attempt to jump straight
            jr, jc = nr+dr, nc+dc
            if board.inside(jr, jc) and not board.is_blocked(nr, nc, jr, jc):
                moves.append((jr, jc))
            else:
                # add reachable diagonals around opponent
                for odr, odc in [(0,1),(0,-1),(1,0),(-1,0)]:
                    if (odr, odc) == (dr, dc) or (odr, odc) == (-dr, -dc):
                        continue
                    ar, ac = nr+odr, nc+odc
                    if board.inside(ar, ac) and not board.is_blocked(nr, nc, ar, ac):
                        moves.append((ar, ac))
        else:
            moves.append((nr, nc))
    # deduplicate
    uniq = []
    for m in moves:
        if m not in uniq:
            uniq.append(m)
    return uniq
