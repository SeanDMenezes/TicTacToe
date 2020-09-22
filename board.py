import pygame
from players import HumanText, HumanGraphical, AI
from elements import Button

# GRID CONSTANTS
WIDTH = 100
HEIGHT = 100

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# GAME CONSTANTS
SCREEN_SIZE = [500, 500]
SIZE = 3

# BLANK BOARD
BLANK ='''
+-+-+-+
| | | |
+-+-+-+
| | | |
+-+-+-+
| | | |
+-+-+-+
'''

def enable_constants():
    global CALIBRI
    global SCREEN
    global FONT
    global CLEAR
    
    CALIBRI = pygame.font.SysFont('calibri', 50)
    FONT = pygame.font.SysFont('calibri', 40)
    CLEAR = FONT.render("", True, BLACK)
    SCREEN = pygame.display.set_mode(SCREEN_SIZE)

def grid_to_str(grd):
    flatten = list(map(lambda line: "".join(line),grd))
    return ('\n'.join(flatten))      

def str_to_grid(s):
    rows = s.split('\n')
    grd = list(map(list,rows[1:-1]))
    return grd

def generate_grid(vals):
    rv = []
    ind = 0
    for _ in range(SIZE):
        new_row = []
        for _ in range(SIZE):
            new_row.append(Cell(vals[ind]))
        rv.append(new_row)
        ind += 1
    return rv

def default_grid():
    return generate_grid([" "] * 9)

class Cell:
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return str(self.val)

    def __eq__(self, other):
        return self.val == other.val

    def __ne__(self, other):
        return not self.__eq__(other)

class Grid:
    def __init__(self, cells=None):
        if cells == None:
            cells = default_grid()
        self.cells = cells
    
    def __eq__(self, other):
        for i in range(SIZE):
            for j in range(SIZE):
                if self.cells[i][j] != other.cells[i][j]:
                    return False
        return True
    
    def place_piece(self, pos, val):
        row = pos // SIZE
        col = pos % SIZE
        self.cells[row][col].val = val
    
    def clear(self):
        self.cells = default_grid()

    def is_empty(self, pos):
        row = pos // SIZE
        col = pos % SIZE
        return self.cells[row][col].val == " "

    def check_draw(self):
        for i in range(SIZE):
            for j in range(SIZE):
                if self.cells[i][j] == Cell(" "):
                    return False
        return True
    
    def check_win(self, player):
        ## row check
        for r in range(SIZE):
            if self.cells[r][0].val == self.cells[r][1].val == self.cells[r][2].val:
                if (self.cells[r][0].val == player):
                    return True

        ## col check
        for c in range(SIZE):
            if self.cells[0][c] == self.cells[1][c] == self.cells[2][c] and \
                self.cells[0][c].val == player:
                return True
        
        ## diagonal check
        if self.cells[0][0] == self.cells[1][1] == self.cells[2][2] or \
            self.cells[0][2] == self.cells[1][1] == self.cells[2][0]:
            if self.cells[1][1].val == player:
                return True
        return False

    def choose_mode(self):
        raise NotImplementedError
    
    def display(self):
        raise NotImplementedError

    def display_win(self, winner):
        raise NotImplementedError

    def display_draw(self):
        raise NotImplementedError

    def display_turn(self):
        raise NotImplementedError
    
    def exit_message(self):
        raise NotImplementedError

    def play_again(self):
        raise NotImplementedError

class Text(Grid):
    def __init__(self, cells=None):
        super().__init__(cells)

    def __repr__(self):
        grid = str_to_grid(BLANK)
        pos = 0
        for i in range(3):
            for j in range(3):
                row = 2*i + 1
                col = 2*j + 1
                grid[row][col] = repr(self.cells[i][j])
                pos += 1
        return grid_to_str(grid)

    def choose_mode(self):
        msg = "\nChoose 1 of the 3 options:\
            \nA - Human vs Human\
            \nB - AI vs Human\
            \nC - AI vs AI\n"
        while 1:
            response = input(msg)
            if response.lower() == "a":
                p1 = HumanText('X')
                p2 = HumanText('O')
                break
            elif response.lower() == "b":
                p1 = AI('X')
                p2 = HumanText('O')
                break
            elif response.lower() == "c":
                p1 = AI('X')
                p2 = AI('O')
                break
            else:
                print("Not a valid option!\n")

        return p1, p2 

    
    def play_again(self):
        while True:
            response = input("Do you want to play again? [Y/N]\n")
            if response.lower() == "y":
                return True
            elif response.lower() == "n":
                return False
            else:
                continue

    def exit_message(self):
        print("Exiting now...")
    
    def display(self):
        print(self)
    
    def display_turn(self, player):
        print("It's {0}'s turn.".format(player))
    
    def display_win(self, winner):
        print("{0} wins!".format(winner))

    def display_draw(self):
        print("It's a draw.")


class Graphical(Grid):
    def __init__(self, cells=None):
        super().__init__(cells)
        pygame.init()
        enable_constants()
        pygame.display.set_caption("Tic-Tac-Toe")
    
    def exit(self):
        pygame.quit()

    def boardPos(self, mouseX, mouseY):
        if 100 <= mouseX <= 200:
            col = 0
        elif 200 < mouseX <= 300:
            col = 1
        elif 300 < mouseX <= 400:
            col = 2
        else:
            col = -1
        
        if 100 <= mouseY <= 200:
            row = 0
        elif 200 < mouseY <= 300:
            row = 1
        elif 300 < mouseY <= 400:
            row = 2
        else:
            row = -1

        return (row, col)

    def get_move(self):
        while 1:
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    return -1
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    (row, col) = self.boardPos(mouseX, mouseY)
                    if row == -1 or col == -1:
                        continue
                    elif self.cells[row][col].val != " ":
                        continue
                    return SIZE * row + col
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return -1
                    else:
                        continue
    
    def choose_mode(self):
        hvh = Button(BLUE, 100, 110, 375, 75, 'Human vs Human')
        avh = Button(BLUE, 140, 260, 250, 75, 'AI vs Human')
        ava = Button(BLUE, 140, 410, 250, 75, 'AI vs AI')

        SCREEN.fill(WHITE)
        hvh.draw(SCREEN)
        avh.draw(SCREEN)
        ava.draw(SCREEN)
        pygame.display.flip()

        while 1:
            for event in pygame.event.get():  # User did something
                pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:  # If user clicked close
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if hvh.isOver(pos):
                        p1 = HumanGraphical('X')
                        p2 = HumanGraphical('O')
                        return p1, p2
                    elif avh.isOver(pos):
                        p1 = AI('X')
                        p2 = HumanGraphical('O')
                        return p1, p2
                    elif ava.isOver(pos):
                        p1 = AI('X')
                        p2 = AI('O')
                        return p1, p2
        

    def display(self):
        SCREEN.fill(WHITE)
        # vertical lines
        pygame.draw.line(SCREEN, BLACK, (200, 100), (200, 400), 2)
        pygame.draw.line (SCREEN, BLACK, (300, 100), (300, 400), 2)

        # horizontal lines...
        pygame.draw.line (SCREEN, BLACK, (100, 200), (400, 200), 2)
        pygame.draw.line (SCREEN, BLACK, (100, 300), (400, 300), 2)

        for i in range(SIZE):
            for j in range(SIZE):
                centerX = ((i) * 100) + 150
                centerY = ((j) * 100) + 150
                if self.cells[j][i].val == "X":
                    pygame.draw.line (SCREEN, RED, (centerX - 22, centerY - 22), \
                         (centerX + 22, centerY + 22), 2)
                    pygame.draw.line (SCREEN, RED, (centerX + 22, centerY - 22), \
                                    (centerX - 22, centerY + 22), 2)
                elif self.cells[j][i].val == "O":
                    pygame.draw.circle(SCREEN, BLUE, (centerX, centerY), 30, 2)
        pygame.display.flip()
    
    def display_text(self, text, position):
        msg = FONT.render(text, True, BLACK)
        SCREEN.blit(msg, position)
        pygame.display.flip()

    def display_win(self, winner):
        self.display_text("{0} wins!".format(winner), [175, 430])
        pygame.time.delay(1000)
        self.display()

    def display_draw(self):
        self.display_text("It's a draw!", [175, 430])
        pygame.time.delay(1000)
        self.display()

    def display_turn(self, symbol):
        self.display_text("It's {0}'s turn.".format(symbol), [175, 20])
    
    def exit_message(self):
        SCREEN.fill(WHITE)
        self.display_text("Exiting game...", [130, 430])
        pygame.time.delay(1000)
        #self.display()

    def play_again(self):
        rematch = Button(BLUE, 140, 410, 250, 75, 'Play again?')
        rematch.draw(SCREEN)
        pygame.display.flip()

        while 1:
            for event in pygame.event.get():  # User did something
                pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:  # If user clicked close
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if rematch.isOver(pos):
                        return True
