"""
Implement your AI here
Do not change the API signatures for _init_ or _call_
_call_ must return a valid action
"""
import numpy as np

class AdvancedGomokuAI:
    def __init__(self, board_size, win_size):
        self.board_size = board_size
        self.win_size = win_size

    def evaluate_board(self, state, player):
        """
        Enhanced evaluation of board state.
        """
        score = 0
        for r in range(self.board_size):
            for c in range(self.board_size):
                if state.board[player, r, c] == 1:
                    score += self.evaluate_position(state, player, r, c)
        return score

    def evaluate_position(self, state, player, r, c):
        """
        Evaluate the position for a player in all directions.
        """
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        total_score = 0
        for dr, dc in directions:
            line_score, open_ends = self.evaluate_direction(state, player, r, c, dr, dc)
            total_score += self.calculate_potential(line_score, open_ends)
        return total_score

    def evaluate_direction(self, state, player, r, c, dr, dc):
        """
        Evaluate a direction from a position.
        """
        line_score = 0
        open_ends = 0

        # Forward direction
        for i in range(1, self.win_size):
            nr, nc = r + i * dr, c + i * dc
            if not (0 <= nr < self.board_size and 0 <= nc < self.board_size):
                break
            if state.board[player, nr, nc] == 1:
                line_score += 1
            elif state.board[0, nr, nc] == 1:  # Check for empty space
                open_ends += 1
                break
            else:
                break

        # Backward direction
        for i in range(1, self.win_size):
            nr, nc = r - i * dr, c - i * dc
            if not (0 <= nr < self.board_size and 0 <= nc < self.board_size):
                break
            if state.board[player, nr, nc] == 1:
                line_score += 1
            elif state.board[0, nr, nc] == 1:  # Check for empty space
                open_ends += 1
                break
            else:
                break

        return line_score, open_ends

    def calculate_potential(self, line_score, open_ends):
        """
        Updated potential calculation with central focus.
        """
        # Winning move
        if line_score >= self.win_size - 1:
            return 200000

        # Imminent threat or opportunity
        if line_score == self.win_size - 2:
            if open_ends == 2:
                return 20000  # Double-open four
            if open_ends == 1:
                return 10000   # Single-open four

        # Central control enhancement
        central_bonus = 1
        if line_score >= 2:
            central_bonus = 2

        # Potential setup for future moves
        if line_score >= 2:
            score = 1000 * line_score * central_bonus
            if open_ends:
                score *= 2  # Open ends are more valuable
            return score

        return 10 * (open_ends + 1) * central_bonus  # Basic score for potential
    # 
    # def calculate_potential(self, line_score, open_ends, r, c):
    #     """
    #     Enhanced potential calculation considering various strategic factors.
    #     """
    #     score = 0

    #     # Winning move
    #     if line_score >= self.win_size - 1:
    #         return 200000

    #     # Imminent threat or opportunity
    #     if line_score == self.win_size - 2:
    #         if open_ends == 2:
    #             score = 20000  # Double-open four
    #         elif open_ends == 1:
    #             score = 10000  # Single-open four

    #     # Central control enhancement
    #     central_bonus = self.calculate_central_bonus(r, c)

    #     # Offensive and Defensive Scoring
    #     if line_score >= 2:
    #         score += 1000 * line_score * central_bonus
    #         if open_ends:
    #             score *= 2  # Open ends are more valuable

    #     # Additional scoring for strategic flexibility and mobility
    #     # Implement your logic here

    #     return max(score, 10 * (open_ends + 1) * central_bonus)
    # def evaluate_position(self, state, player, r, c):
    #     """
    #     Evaluate the position for a player in all directions.
    #     """
    #     directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    #     total_score = 0
    #     for dr, dc in directions:
    #         line_score, open_ends = self.evaluate_direction(state, player, r, c, dr, dc)
    #         total_score += self.calculate_potential(line_score, open_ends, r, c)
    #     return total_score

    # def calculate_central_bonus(self, r, c):
    #     """
    #     Calculate a dynamic central bonus based on the position's proximity to the center.
    #     """
    #     center = self.board_size // 2
    #     distance_to_center = max(abs(r - center), abs(c - center))
    #     # Adjust these values as needed
    #     max_distance = self.board_size // 2
    #     return 1 + (max_distance - distance_to_center) / max_distance

    
class Submission:
    def __init__(self, board_size, win_size):
        self.board_size = board_size
        self.win_size = win_size
        self.ai = AdvancedGomokuAI(board_size, win_size)

    def __call__(self, state):
        player = state.current_player()
        opponent = 3 - player

        best_score = -np.inf
        best_move = None

        # Enhanced move ordering with central focus
        move_candidates = self.get_prioritized_moves(state, central_focus=True)

        for r, c in move_candidates:
            if state.board[0, r, c] == 1:  # Check if the position is empty
                state.board[player, r, c] = 1
                score = self.ai.evaluate_board(state, player) - self.ai.evaluate_board(state, opponent)
                state.board[player, r, c] = 0  # Reset the board

                if score > best_score:
                    best_score = score
                    best_move = (r, c)

        return best_move

    def get_prioritized_moves(self, state, central_focus=False):
        """
        Generate move candidates with priority, focusing on central control.
        """
        center = self.board_size // 2
        center_range = self.board_size // 4  # Define a central area
        candidates = []
        for r in range(self.board_size):
            for c in range(self.board_size):
                if state.board[0, r, c] == 1:  # Empty cell
                    priority = 0
                    if central_focus and abs(r - center) <= center_range and abs(c - center) <= center_range:
                        priority += 10  # Higher priority for central positions

                    # Additional priority based on proximity to existing stones
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.board_size and 0 <= nc < self.board_size and state.board[0, nr, nc] != 1:
                                priority += 1
                    candidates.append(((r, c), priority))
        candidates.sort(key=lambda x: x[1], reverse=True)
        return [pos for pos, _ in candidates]