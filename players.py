SIZE = 3

def other_player(symbol):
    if symbol == "X":
        return "O"
    else:
        return "X"

def minimax(game, depth, alpha, beta, max_player, player_symbol):
    if depth == 0 or (game.check_win("X") or game.check_win("O") or game.check_draw()):
        if game.check_win(player_symbol):
            return 1
        if game.check_win(other_player(player_symbol)):
            return -1
        if game.check_draw():
            return 0
    
    if max_player:
        max_eval = -100
        for i in range(SIZE):
            for j in range(SIZE):
                if game.cells[i][j].val == " ":
                    game.cells[i][j].val = player_symbol
                    ev = minimax(game, depth-1, alpha, beta, False, player_symbol)
                    game.cells[i][j].val = " "
                    max_eval = max(ev, max_eval)
                    alpha = max(alpha, ev)
                    if beta <= alpha:
                        break
        return max_eval
    
    else:
        min_eval = 100
        for i in range(SIZE):
            for j in range(SIZE):
                if game.cells[i][j].val == " ":
                    game.cells[i][j].val = other_player(player_symbol)
                    ev = minimax(game, depth-1, alpha, beta, True, player_symbol)
                    game.cells[i][j].val = " "
                    min_eval = min(ev, min_eval)
                    beta = min(beta, ev)
                    if alpha >= beta:
                        break
        return min_eval

class Player:
    def __init__(self, symbol):
        self.symbol = symbol
    
    def __eq__(self, other):
        return self.symbol == other.symbol

    def get_move(self, game, symbol):
        raise NotImplementedError

    def lose(self):
        raise NotImplementedError

class HumanText(Player):
    def __init__(self, symbol):
        super().__init__(symbol)

    def get_move(self, game, symbol):
        while (1):
            move = input()
            try:
                move = int(move) - 1
                if move not in range(0,9):
                    print("Please enter an integer between 1 and 9.")
                    continue
                elif game.cells[move // SIZE][move % SIZE].val != " ":
                    print("That cell is already taken!")
                    continue
            except Exception:
                print("Please enter an integer between 1 and 9.")
                continue
            return move

class HumanGraphical(Player):
    def __init__(self, symbol):
        super().__init__(symbol)

    def get_move(self, game, symbol):
        return game.get_move()

class AI(Player):
    def __init__(self, symbol):
        super().__init__(symbol)
    
    def get_move(self, game, symbol):
        max_eval = -100
        for i in range(SIZE):
            for j in range(SIZE):
                if game.cells[i][j].val == " ":
                    game.cells[i][j].val = symbol
                    ev = minimax(game, 9, -100, 100, False, symbol)
                    game.cells[i][j].val = " "
                    if ev > max_eval:
                        max_eval = ev
                        move = 3*i + j
        return move