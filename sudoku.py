import sys
import pygame
import random
import math


class Sudoku_Generator:
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0] * row_length] * row_length
        self.box_length = int(math.sqrt(row_length))

    def get_board(self):
        return self.board

    def print_board(self):
        for i in range(0, len(self.board)):
            print(self.board[i])

    def valid_in_row(self, row, num):
        in_row = False
        for i in range(0, len(self.board[row])):
            if self.board[row][i] == num:
                in_row = True
                break
        return not in_row

    def valid_in_col(self, col, num):
        in_col = False
        for i in range(0, len(self.board)):
            if self.board[i][col] == num:
                in_col = True
                break
        return not in_col

    def valid_in_box(self, row_start, col_start, num):
        in_box = False
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                if num == self.board[i][j]:
                    in_box = True
                    break
        return not in_box

    def is_valid(self, row, col, num):
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3
        if self.valid_in_box(row_start, col_start, num) == True and self.valid_in_row(row,
                                                                                      num) == True and self.valid_in_col(
            col, num) == True:
            return True
        else:
            return False

    def fill_box(self, row_start, col_start):
        l = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(l)
        self.board[row_start] = [0] * self.row_length
        self.board[row_start + 1] = [0] * self.row_length
        self.board[row_start + 2] = [0] * self.row_length
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                if self.is_valid(i, j, l[((i - row_start) * 3) + (j - col_start)]):
                    self.board[i][j] = l[((i - row_start) * 3) + (j - col_start)]
                else:
                    continue

    def fill_diagonal(self):
        self.fill_box(6, 6)
        self.fill_box(3, 3)
        self.fill_box(0, 0)

    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    def remove_cells(self):
        random_positions = []
        number_of_random_pos = 0
        while number_of_random_pos < self.removed_cells:
            random_position = (random.randint(0, 8), random.randint(0, 8))
            if random_position in random_positions:
                continue
            else:
                random_positions.append(random_position)
                number_of_random_pos += 1
        for i in range(0, len(random_positions)):
            x, y = random_positions[i][0], random_positions[i][1]
            self.board[x][y] = 0

    def generate_sudoku(self, removed):
        self.remove_cells()
        main_board = self.get_board()
        return main_board

    def generate_answer(self):
        self.fill_values()
        ans_board = self.get_board()
        return ans_board


class Cell:
    def __init__(self, value, row, col, screen):
        # Constructor for the Cell class
        self.value = value
        self.sketch_value = 0
        self.row = row
        self.col = col
        self.screen = screen

    def set_cell_value(self, value):
        # Setter for this cell’s value
        self.value = value

    def set_sketched_value(self, value):
        # Setter for this cell’s sketched value
        self.sketch_value = value

    def draw(self):
        if self.sketch_value == 0:
            sketch_value = ''
        if self.value == 0:
            value = ''  # manages displaying no value if the cell has a zero value
        if self.sketch_value != 0:
            sketch_value = str(self.sketch_value)
        if self.value != 0:
            value = str(self.value)
        square_size = 70  # sets size of square
        cell_font = pygame.font.Font(None, 30)
        sketch_font = pygame.font.Font(None, 30)
        sketch_rect = pygame.Rect((self.row * square_size) + 5, (self.col * square_size) + 5, square_size + 5,
                           square_size + 5)
        value_temp = pygame.Rect((self.row * square_size), (self.col * square_size), square_size,
                            square_size)
        # uses pygame function to create a rectangle object with arguments (row,col,
        # square_size,square_size) to draw the cell
        sketch_surf = sketch_font.render(sketch_value, True, (122, 122, 122))
        value_surf = cell_font.render(value, True, (0, 0, 0))  # draws value with
        # arguments for value, True and color
        value_rect = value_surf.get_rect(center=value_temp.center)  # defines rectangle center
        self.screen.blit(sketch_surf, sketch_rect)
        self.screen.blit(value_surf, value_rect)  # uses .blit function to add image to screen


class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = 0
        self.selected_row = 0
        self.selected_col = 0
        self.mode = ''
        square_size = self.width // 9
        self.reset_rect = pygame.Rect(square_size * 3, self.height + 25, 75, 50)
        self.restart_rect = pygame.Rect(square_size * 4.5, self.height + 25, 80, 50)
        self.exit_rect = pygame.Rect(square_size * 6, self.height + 25, 75, 50)
        if difficulty == "Easy":
            self.difficulty = 30
        elif difficulty == "Medium":
            self.difficulty = 40
        elif difficulty == "Hard":
            self.difficulty = 50
        self.sudoku = Sudoku_Generator(9, self.difficulty)
        self.ans_board_temp = self.sudoku.generate_answer()
        self.ans_board = [[0 for i in range(9)] for i in range(9)]
        for i in range(0, len(self.ans_board_temp)):
            for j in range(0, len(self.ans_board_temp[i])):
                self.ans_board[i][j] = self.ans_board_temp[i][j]
        temp_board = self.sudoku.generate_sudoku(self.difficulty)
        self.board = [[0 for i in range(9)] for i in range(9)]
        for i in range(0, len(temp_board)):
            for j in range(0, len(temp_board[i])):
                if temp_board[i][j] == 0:
                    self.board[i][j] = Cell(0, i, j, self.screen)
                else:
                    self.board[i][j] = temp_board[i][j]

    def draw(self):
        cell_font = pygame.font.Font(None, 30)
        square_size = self.width // 9
        pygame.draw.line(self.screen, (0, 0, 0), (0, 0), (0, self.height), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (0, 0), (self.width, 0), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (0, self.height), (self.width, self.height), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (self.width, 0), (self.width, self.height), 3)
        pygame.draw.rect(self.screen, (0, 0, 0), self.reset_rect, 3)
        pygame.draw.rect(self.screen, (0, 0, 0), self.restart_rect, 3)
        pygame.draw.rect(self.screen, (0, 0, 0), self.exit_rect, 3)
        reset_surf = cell_font.render("Reset", True, (0, 0, 0))
        restart_surf = cell_font.render("Restart", True, (0, 0, 0))
        exit_surf = cell_font.render("Exit", True, (0, 0, 0))
        reset_rect = reset_surf.get_rect(center=self.reset_rect.center)
        restart_rect = restart_surf.get_rect(center=self.restart_rect.center)
        exit_rect = exit_surf.get_rect(center=self.exit_rect.center)
        self.screen.blit(reset_surf, reset_rect)
        self.screen.blit(restart_surf, restart_rect)
        self.screen.blit(exit_surf, exit_rect)
        for i in range(1, 9):
            line_width = 1
            if i % 3 == 0:
                line_width = 2
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * square_size), (self.width, i * square_size), line_width)
            pygame.draw.line(self.screen, (0, 0, 0), (i * square_size, 0), (i * square_size, self.height), line_width)
        for j in range(0, 9):
            for k in range(0, 9):
                if type(self.board[j][k]) != Cell:
                    cell_surf = cell_font.render(str(self.board[j][k]), True, (0, 0, 0))
                    rect = pygame.Rect((j) * square_size, (k) * square_size, square_size, square_size)
                    cell_rect = cell_surf.get_rect(center=rect.center)
                    self.screen.blit(cell_surf, cell_rect)
                elif type(self.board[j][k]) == Cell:
                    self.board[j][k].draw()

    def select(self, row, col):
        red = (255, 0, 0)
        square_size = (self.width // 9, self.height // 9)
        line_width = 3
        self.screen.fill((128, 170, 255))
        self.draw()
        self.selected_row = row - 1
        self.selected_col = col - 1
        rect = pygame.Rect((row - 1) * square_size[0], (col - 1) * square_size[1], square_size[0], square_size[1])
        pygame.draw.rect(self.screen, red, rect, line_width)

    def click(self, x, y, game_over):
        if game_over:
            square_size = self.width // 9
            row = x // square_size
            col = y // square_size
            self.selected_row = row
            self.selected_col = col
            if x < self.width - 3 and y < self.height - 3:
                self.select(row + 1, col + 1)
                return False
            elif self.reset_rect.collidepoint(x, y):
                self.reset_to_original()
                self.update_board()
                return False
            elif self.restart_rect.collidepoint(x, y):
                return True  # return to main menu
            elif self.exit_rect.collidepoint(x, y):
                sys.exit()

    def clear(self):
        self.board[self.selected_row][self.selected_col].set_cell_value(0)

    def sketch(self, value):
        self.board[self.selected_row][self.selected_col].set_sketched_value(value)

    def place_number(self, value):
        self.board[self.selected_row][self.selected_col].set_cell_value(value)

    def reset_to_original(self):
        self.selected_row = 0
        self.selected_col = 0
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[i])):
                if type(self.board[i][j]) == Cell:
                    self.board[i][j].set_cell_value(0)
                    self.board[i][j].set_sketched_value(0)

    def is_full(self):
        for i in range(9):
            for j in range(9):
                if type(self.board[i][j]) == Cell and self.board[i][j].value == 0:
                    return False
        return True

    def update_board(self):
        self.screen.fill((128, 170, 255))
        self.draw()
        pygame.display.update()

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if type(self.board[i][j]) == Cell and self.board[i][j].value == 0:
                    return i, j
        return None

    def check_board(self):
        win = False
        for i in range(9):
            for j in range(9):
                if type(self.board[i][j]) == Cell:
                    if int(self.board[i][j].value) == self.ans_board[i][j]:
                        win = True
                    elif int(self.board[i][j].value) != self.ans_board[i][j]:
                        return False
        return win


if __name__ == '__main__':
    pygame.init()
    height = 730
    width = 630
    rect_height = 50
    rect_width = 125
    rect_x = 100
    rect_y = 425
    original_pos = pygame.Rect((height + 100, width + 100, 1, 1))
    ending_rect = original_pos
    rect_easy = original_pos
    rect_medium = original_pos
    rect_hard = original_pos
    restarting_rect = original_pos
    finished = False
    in_main_menu = True
    game_over_loose = False
    game_over_win = False
    screen = pygame.display.set_mode((width, height), flags=pygame.SCALED)
    pygame.display.set_caption('Sudoku')
    text_f = pygame.font.Font(None, 70)
    option_font = pygame.font.Font(None, 35)
    icon = pygame.image.load(
        'image.png').convert()  # image comes from https://www.lite.games/sudoku-now-as-good-as-new-update/
    screen.blit(icon, (0, 0))
    board = None
    random.seed(random.randint(0, 100000000))


    def draw_rect(pos, color='red', width=0):
        pygame.draw.rect(screen, color, pos, width)

        return pygame.Rect(pos)


    def write_text(text, pos, color='red', text_font=text_f):
        text_surf = text_font.render(text, 0, color)
        text_rect = text_surf.get_rect(center=pos)
        screen.blit(text_surf, text_rect)


    def draw_starting_screen():
        icon = pygame.image.load('image.png').convert()
        screen.blit(icon, (0, 0))
        draw_rect((50, (height // 2 - 225), 500, 50), 'black')
        draw_rect((50, (height // 2 - 125), 500, 50), 'black')
        write_text('Welcome To Sudoku', (width // 2, height // 2 - 200))
        write_text('Select Game Mode', (width // 2, height // 2 - 100))
        rect_easy = draw_rect((rect_x, rect_y + 50, rect_width, rect_height))
        rect_medium = draw_rect((rect_x + 150, rect_y + 50, rect_width, rect_height))
        rect_hard = draw_rect((rect_x + 300, rect_y + 50, rect_width, rect_height))
        write_text('Easy', (rect_x + 60, rect_y + 75), 'Black', text_font=option_font)
        write_text('Medium', (rect_x + 210, rect_y + 75), 'Black', text_font=option_font)
        write_text('Hard', (rect_x + 360, rect_y + 75), 'Black', text_font=option_font)
        return rect_easy, rect_medium, rect_hard


    def draw_ending_screen_win():
        icon = pygame.image.load('image.png').convert()
        screen.blit(icon, (0, 0))
        draw_rect(((width // 2 - 57.5), (height // 2 - 225), rect_width, 50), 'red')
        write_text('You Won!', (width // 2, height // 2 - 200), 'black', text_font=option_font)
        rect = draw_rect((width // 2 - 50, height // 2, rect_width, rect_height))
        write_text('Exit', (width // 2 + 10, height // 2 + 25), 'black', text_font=option_font)
        return rect


    def draw_ending_screen_loose():
        icon = pygame.image.load('image.png').convert()
        screen.blit(icon, (0, 0))
        draw_rect(((width // 2 - 57.5), (height // 2 - 225), rect_width, 50), 'red')
        write_text('You lost!', (width // 2, height // 2 - 200), 'black', text_font=option_font)
        rect = draw_rect((width // 2 - 50, height // 2, rect_width, rect_height))
        write_text('Restart', (width // 2 + 10, height // 2 + 25), 'black', text_font=option_font)
        return rect


    def return_to_original(*args):
        for i in args:
            kwargs = original_pos


    rect_easy, rect_medium, rect_hard = draw_starting_screen()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_over_win:
                ending_rect = draw_ending_screen_win()
                if ending_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, (0, 0, 0), ending_rect, 3)
                else:
                    ending_rect = draw_ending_screen_win()
            if game_over_loose:
                board.reset_to_original()

                if restarting_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, (0, 0, 0), restarting_rect, 3)
                else:
                    restarting_rect = draw_ending_screen_loose()
            if event.type == pygame.TEXTINPUT:
                if not in_main_menu and not game_over_win and not game_over_loose:
                    if type(board.board[board.selected_row][board.selected_col]) == Cell:
                        try:
                            value = int(event.text)
                        except:
                            value = 0
                        board.draw()
                        temp_rect = pygame.Rect((board.selected_row * 70) + 5, (board.selected_col * 70) + 5, 62, 62)
                        board.select(board.selected_row + 1, board.selected_col + 1)
                        pygame.draw.rect(screen, (128, 170, 255), temp_rect, 0)
                        value_font = pygame.font.Font(None, 30)
                        value_temp = pygame.Rect((board.selected_row * 70), (board.selected_col * 70), 70, 70)
                        temp_value = ' '
                        if board.board[board.selected_row][board.selected_col].value != 0:
                            temp_value = str(board.board[board.selected_row][board.selected_col].value)
                        value_surf = value_font.render(temp_value, True, (0, 0, 0))
                        value_rect = value_surf.get_rect(center=value_temp.center)
                        screen.blit(value_surf, value_rect)
                        sketch_font = pygame.font.Font(None, 30)
                        sketch_rect = pygame.Rect((board.selected_row * 70) + 5, (board.selected_col * 70) + 5, 75, 75)
                        sketch_surf = sketch_font.render(str(value), True, (122, 122, 122))
                        screen.blit(sketch_surf, sketch_rect)
                        board.board[board.selected_row][board.selected_col].set_sketched_value(str(value))
            if event.type == pygame.KEYDOWN:
                if not in_main_menu:
                    if not game_over_loose and not game_over_win:
                        if event.key == pygame.K_UP:
                            if board.selected_col > 0:
                                board.selected_col -= 1
                                board.select(board.selected_row + 1, board.selected_col + 1)
                                pygame.display.update()
                        if event.key == pygame.K_DOWN:
                            if board.selected_col < 8:
                                board.selected_col += 1
                                board.select(board.selected_row + 1, board.selected_col + 1)
                                pygame.display.update()
                        if event.key == pygame.K_LEFT:
                            if board.selected_row > 0:
                                board.selected_row -= 1
                                board.select(board.selected_row + 1, board.selected_col + 1)
                                pygame.display.update()
                        if event.key == pygame.K_RIGHT:
                            if board.selected_row < 8:
                                board.selected_row += 1
                                board.select(board.selected_row + 1, board.selected_col + 1)
                                pygame.display.update()
                    if event.key == pygame.K_RETURN:
                        if type(board.board[board.selected_row][board.selected_col]) == Cell:
                            if board.board[board.selected_row][board.selected_col].sketch_value != 0:
                                board.place_number(board.board[board.selected_row][board.selected_col].sketch_value)
                                board.sketch(0)
                                board.select(board.selected_row + 1, board.selected_col + 1)
                    if event.key == pygame.K_BACKSPACE:
                        if type(board.board[board.selected_row][board.selected_col]) == Cell:
                            value = 0
                            board.sketch(value)
                            board.update_board()
                            board.select(board.selected_row + 1, board.selected_col + 1)
                    if board.is_full():
                        if not board.check_board():
                            game_over_loose = True
                            continue
                        if board.check_board():
                            game_over_win = True
                            continue

            if in_main_menu:
                if rect_easy.collidepoint(pygame.mouse.get_pos()):
                    draw_starting_screen()
                    pygame.draw.rect(screen, (0, 0, 0), rect_easy, 3)
                elif rect_medium.collidepoint(pygame.mouse.get_pos()):
                    draw_starting_screen()
                    pygame.draw.rect(screen, (0, 0, 0), rect_medium, 3)
                elif rect_hard.collidepoint(pygame.mouse.get_pos()):
                    draw_starting_screen()
                    pygame.draw.rect(screen, (0, 0, 0), rect_hard, 3)
                else:
                    draw_starting_screen()

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if ending_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
                if restarting_rect.collidepoint(pygame.mouse.get_pos()):
                    game_over_loose = False
                    return_to_original(restarting_rect)
                    restarting_rect = draw_ending_screen_loose()
                if in_main_menu:
                    if rect_easy.collidepoint(pygame.mouse.get_pos()):
                        board = Board(630, 630, screen, 'Easy')
                        board.update_board()
                        in_main_menu = False
                        continue
                    if rect_medium.collidepoint(pygame.mouse.get_pos()):
                        board = Board(630, 630, screen, 'Medium')
                        board.update_board()
                        in_main_menu = False
                        continue
                    if rect_hard.collidepoint(pygame.mouse.get_pos()):
                        board = Board(630, 630, screen, 'Hard')
                        board.update_board()
                        in_main_menu = False
                        continue

                if not in_main_menu:
                    if not game_over_win and not game_over_loose:
                        mousepos = pygame.mouse.get_pos()
                        if board.click(mousepos[0], mousepos[1], not game_over_win or not game_over_loose):
                            in_main_menu = True
                            rect_easy, rect_medium, rect_hard = draw_starting_screen()
                            continue
                    if board.is_full():
                        if not board.check_board():
                            game_over_loose = True
                            continue
                        if board.check_board():
                            game_over_win = True
                            continue
            if not in_main_menu:
                if not game_over_loose and not game_over_win:
                    if board.reset_rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(screen, (0, 0, 0), board.restart_rect, 3)
                        pygame.draw.rect(screen, (255, 0, 0), board.reset_rect, 3)
                        pygame.draw.rect(screen, (0, 0, 0), board.exit_rect, 3)
                    elif board.restart_rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(screen, (255, 0, 0), board.restart_rect, 3)
                        pygame.draw.rect(screen, (0, 0, 0), board.reset_rect, 3)
                        pygame.draw.rect(screen, (0, 0, 0), board.exit_rect, 3)
                    elif board.exit_rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(screen, (0, 0, 0), board.restart_rect, 3)
                        pygame.draw.rect(screen, (0, 0, 0), board.reset_rect, 3)
                        pygame.draw.rect(screen, (255, 0, 0), board.exit_rect, 3)
                    else:
                        pygame.draw.rect(screen, (0, 0, 0), board.restart_rect, 3)
                        pygame.draw.rect(screen, (0, 0, 0), board.reset_rect, 3)
                        pygame.draw.rect(screen, (0, 0, 0), board.exit_rect, 3)
        pygame.display.update()