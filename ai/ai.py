from typing import List, Tuple, Optional
from math import inf
from game.game_state import GameState
from game.pathfinding import bfs_shortest_path_length
from game.player import Player
from game.board import Board

Action = Tuple  # ('M', r, c) or ('W', 'H'|'V', wr, wc)

class MinimaxAI:
    def __init__(self, max_depth: int = 3):
        self.max_depth = max_depth

    def choose_move(self, state: GameState, player_index: int, depth: Optional[int] = None) -> Optional[Action]:
        """
        Top-level API. Returns an action tuple or None if nothing found.
        """
        if depth is None:
            depth = self.max_depth
        score, action = self._minimax_root(state, player_index, depth)
        return action

    def _minimax_root(self, state: GameState, player_index: int, depth: int):
        best_score = -inf
        best_action = None
        alpha = -inf
        beta = inf

        actions = self._generate_actions(state, player_index)
        # Basic ordering: prioritize pawn moves first (often stronger and fewer)
        actions.sort(key=lambda a: 0 if a[0] == 'M' else 1)

        for a in actions:
            child = state.clone()
            success = self._apply_action(child, player_index, a)
            if not success:
                continue
            score = self._minimax(child, depth - 1, alpha, beta, maximizing=False, ai_index=player_index)
            if score > best_score:
                best_score = score
                best_action = a
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score, best_action

    def _minimax(self, state: GameState, depth: int, alpha: float, beta: float, maximizing: bool, ai_index: int) -> float:
        winner = state.get_winner()
        if winner is not None:
            if winner == ai_index:
                return 1e6
            else:
                return -1e6

        if depth == 0:
            return self._evaluate(state, ai_index)

        current = state.current
        actions = self._generate_actions(state, current)

        if maximizing:
            value = -inf
            for a in actions:
                child = state.clone()
                if not self._apply_action(child, current, a):
                    continue
                value = max(value, self._minimax(child, depth - 1, alpha, beta, False, ai_index))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = inf
            for a in actions:
                child = state.clone()
                if not self._apply_action(child, current, a):
                    continue
                value = min(value, self._minimax(child, depth - 1, alpha, beta, True, ai_index))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

    def _apply_action(self, state: GameState, player_index: int, action: Action) -> bool:
        """
        Apply an action to the provided (cloned) GameState.
        Returns True if action succeeded and modified the state, False otherwise.
        """
        if action[0] == 'M':
            # ('M', r, c)
            _, r, c = action
            return state.move_pawn(player_index, r, c)
        else:
            # ('W', orient, wr, wc)
            _, orient, wr, wc = action
            return state.try_place_wall(player_index, orient, wr, wc)

    def _generate_actions(self, state: GameState, player_index: int) -> List[Action]:
        """
        Generate pawn moves + candidate wall placements.
        Wall candidates are filtered to be near either pawn (manhattan <= 3) to reduce branching.
        """
        actions: List[Action] = []
        #pawn
        pawn_moves = state.legal_moves(player_index)
        for (r, c) in pawn_moves:
            actions.append(('M', r, c))

        # walls
        size = state.board.size
        s = size - 1
        p = state.players[player_index]
        opp = state.players[1 - player_index]

        # helper to test proximity
        def near_player(wr, wc):
            d1 = abs(wr - p.r) + abs(wc - p.c)
            d2 = abs(wr - opp.r) + abs(wc - opp.c)
            return (d1 <= 3) or (d2 <= 3)

        if p.walls <= 0:
            return actions

        # iterate possible intersections but filter by proximity and basic can_place
        for wr in range(s):
            for wc in range(s):
                if not near_player(wr, wc):
                    continue
                # Horizontal
                if state.can_place_wall('H', wr, wc):
                    # We don't run try_place here (path check) — try_place will be executed in simulation.
                    actions.append(('W', 'H', wr, wc))
                # Vertical
                if state.can_place_wall('V', wr, wc):
                    actions.append(('W', 'V', wr, wc))

        return actions

#Score (AI perspective) = (opd - myd) + 0.1*(my_walls - opp_walls)
    def _evaluate(self, state: GameState, ai_index: int) -> float:
        """
        Evaluate board from AI's perspective. Positive = good for AI.
        Uses shortest path lengths and remaining walls.
        """
        my = state.players[ai_index]
        opp = state.players[1 - ai_index]
        myd = bfs_shortest_path_length(state.board, (my.r, my.c), [state.board.size - 1] if ai_index == 0 else [0])
        opd = bfs_shortest_path_length(state.board, (opp.r, opp.c), [state.board.size - 1] if (1 - ai_index) == 0 else [0])

        INF_DIST = 1000
        if myd is None:
            myd = INF_DIST
        if opd is None:
            opd = INF_DIST

        score = float(opd - myd)
        score += 0.1 * (my.walls - opp.walls)

        return score
