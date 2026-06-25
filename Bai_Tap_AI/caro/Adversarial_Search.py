import math
import random

class AIPlayer:
    def check_winner(self, b, p):
        win_states = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        return any(b[i] == b[j] == b[k] == p for i, j, k in win_states)

    def is_full(self, b):
        return ' ' not in b

    def utility(self, b):
        if self.check_winner(b, 'O'): return 1
        if self.check_winner(b, 'X'): return -1
        return 0

    # --- MINIMAX ---
    def max_value(self, state):
        if self.check_winner(state, 'X') or self.check_winner(state, 'O') or self.is_full(state):
            return self.utility(state)
        v = -math.inf
        for i in range(9):
            if state[i] == ' ':
                state[i] = 'O'
                v = max(v, self.min_value(state))
                state[i] = ' '
        return v

    def min_value(self, state):
        if self.check_winner(state, 'X') or self.check_winner(state, 'O') or self.is_full(state):
            return self.utility(state)
        v = math.inf
        for i in range(9):
            if state[i] == ' ':
                state[i] = 'X'
                v = min(v, self.max_value(state))
                state[i] = ' '
        return v

    # --- ALPHA-BETA ---
    def ab_max(self, state, alpha, beta):
        if self.check_winner(state, 'X') or self.check_winner(state, 'O') or self.is_full(state):
            return self.utility(state)
        v = -math.inf
        for i in range(9):
            if state[i] == ' ':
                state[i] = 'O'
                v = max(v, self.ab_min(state, alpha, beta))
                state[i] = ' '
                if v >= beta: return v
                alpha = max(alpha, v)
        return v

    def ab_min(self, state, alpha, beta):
        if self.check_winner(state, 'X') or self.check_winner(state, 'O') or self.is_full(state):
            return self.utility(state)
        v = math.inf
        for i in range(9):
            if state[i] == ' ':
                state[i] = 'X'
                v = min(v, self.ab_max(state, alpha, beta))
                state[i] = ' '
                if v <= alpha: return v
                beta = min(beta, v)
        return v

    # --- EXPECTIMAX ---
    def ex_max(self, state):
        if self.check_winner(state, 'X') or self.check_winner(state, 'O') or self.is_full(state):
            return self.utility(state)
        v = -math.inf
        for i in range(9):
            if state[i] == ' ':
                state[i] = 'O'
                v = max(v, self.ex_chance(state))
                state[i] = ' '
        return v

    def ex_chance(self, state):
        if self.check_winner(state, 'X') or self.check_winner(state, 'O') or self.is_full(state):
            return self.utility(state)
        moves = [i for i, x in enumerate(state) if x == ' ']
        expected_val = 0
        prob = 1.0 / len(moves)
        for i in moves:
            state[i] = 'X'
            expected_val += prob * self.ex_max(state)
            state[i] = ' '
        return expected_val