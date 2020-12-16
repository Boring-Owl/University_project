import pygame
import random

# Window settings.
win_width = 800
win_height = 700
game_resolution = (win_width, win_height)
play_width = 300
play_height = 600
block_size = 30
left_indent_x = (win_width - play_width) // 2
left_indent_y = win_height - play_height
left_indent_x = 100
left_indent_y = 100

# Shape form.
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

# Shape options.
shapes = [T, I, S, O, Z, L, J]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Shape(object):
    rows = 20
    columns = 10 

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0 


def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid

# Share convert.
def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

# Check for free space. 
def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 2:
            return True
    return False


def draw_menu(text, window):
    window.fill((75, 0, 130))
    font = pygame.font.SysFont('arial', 60)
    label = text.splitlines()
    
    for i, symbol in enumerate(label):
        window.blit(font.render(symbol, 1, (240, 240, 240)), (win_width / 3, win_height/3 + 70*i))
    
    pygame.display.update()


def draw_lose(text, window):
    font = pygame.font.SysFont('arial', 60)
    label = font.render(str(text), 1, (100, 100, 100))
    window.blit(label, (100, win_height // 2))
    pygame.display.update()    


def draw_grid(window, row, col):
    x = left_indent_x
    y = left_indent_y
    for i in range(row):
        pygame.draw.line(window, (128,128,128), (x, y + i*30), (x + play_width, y + i*30))
        for j in range(col):
            pygame.draw.line(window, (128,128,128), (x + j*30, y), (x + j*30, y + play_height))


def get_shape():
    global shapes, shape_colors

    return Shape(5, 0, random.choice(shapes))


def clear_rows(grid, locked):
    inc = 0
    score = 0

    # Take block.
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        # Block check for filling.
        if (0, 0, 0) not in row:
            # Have many line are filling.
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                    score += 10
                except:
                    continue
    
    # Falling blocks.
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return score

def draw_next_shape_and_score(shape, score, window):
    font = pygame.font.SysFont('arial', 30)

    x = left_indent_x + play_width + 50
    y = left_indent_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    # Draw next shape.
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(window, shape.color, (x + j*30, y + i*30, 30, 30), 0)

    label = font.render('Next Shape', 1, (255,255,255))
    window.blit(label, (x + 10, y - 30))

    # Draw Score.
    label = font.render('Score', 1, (255,255,255))
    window.blit(label, (x, y - 140)) 
    label = font.render(str(score), 1, (100, 100, 100))
    window.blit(label, (x, y - 100)) 


def draw_window(score, next_shape, window):
    window.fill((75, 0, 130))
    font = pygame.font.SysFont('arial', 60)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(window, grid[i][j], (left_indent_x + j*30, left_indent_y + i*30, 30, 30), 0)

    # Draw grid and border.
    draw_grid(window, 20, 10)
    pygame.draw.rect(window, (255, 250, 250), (left_indent_x, left_indent_y, play_width, play_height), 5)

    # Draw title.
    label = font.render('Tetris', 1, (240, 240, 240))
    window.blit(label, (left_indent_x + play_width//4, 30))

    # Draw next shape and score.
    draw_next_shape_and_score(next_shape, score, window)
    pygame.display.update()


def game(start_speed):
    global grid

    change_shape = False
    game_running = True

    locked_positions = {}
    grid = create_grid(locked_positions)
    current_shape = get_shape()
    next_shape = get_shape()
    clock = pygame.time.Clock()
    
    speed = start_speed
    level = 1
    tick = 0
    score = 0
    fps = 30
    
    while game_running:
        grid = create_grid(locked_positions)
        tick += 1
        clock.tick(fps)

        # Level up.
        if score / level >= 200 and speed > 0.1:
            if level <= 5:
                level += 1
                speed -= 0.1
                print(speed)
            elif level < 15 and speed > 0.5:
                level +=1
                speed -= 0.05
                print(speed)

        # Shape fall.
        if tick/fps >= speed:
            tick = 0
            current_shape.y += 1
            if not (valid_space(current_shape, grid)) and current_shape.y > 0:
                current_shape.y -= 1
                change_shape = True

        # Key handling.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                pygame.display.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_shape.x -= 1
                    if not valid_space(current_shape, grid):
                        current_shape.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_shape.x += 1
                    if not valid_space(current_shape, grid):
                        current_shape.x -= 1

                elif event.key == pygame.K_UP:
                    current_shape.rotation = current_shape.rotation + 1 % len(current_shape.shape)
                    if not valid_space(current_shape, grid):
                        current_shape.rotation = current_shape.rotation - 1 % len(current_shape.shape)

                if event.key == pygame.K_DOWN:
                    current_shape.y += 1
                    if not valid_space(current_shape, grid):
                        current_shape.y -= 1
                
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    game_running = False
                    pause_menu(score)
                    game_running = True

                if event.key == pygame.K_SPACE:
                    while valid_space(current_shape, grid):
                        current_shape.y += 1
                        score += 1
                    current_shape.y -= 1

        # Getting occupied places.
        shape_pos = convert_shape_format(current_shape)

        # Painting grid.
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_shape.color

        # Change of shape
        if change_shape:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_shape.color
            current_shape = next_shape
            next_shape = get_shape()
            change_shape = False

            # Check for filled lines
            score += clear_rows(grid, locked_positions)
            

        # Check for loss.
        if check_lost(locked_positions):
            game_running = False

        draw_window(score, next_shape, window)

    lose_menu(score, window)

def pause_menu(score):
    pause_running = True

    while pause_running:
            window.fill((60,60,60))
            draw_menu('1.Resume. \n2.Exit to menu. \n3.Exit. ', window)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()   
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        pause_running = False
                    if event.key == pygame.K_2:
                        main_menu(window)
                    if event.key == pygame.K_3:
                        sys.exit()
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()


def lose_menu(score, window):
    game_running = False
    draw_lose('You Losе', window)
    pygame.time.delay(5000)
    main_menu(window)

def level_menu(window):
    level_menu_running = True

    while level_menu_running:
        draw_menu('1. Level - 1 \n2. Level - 5 \n3. Level - 10 \n4. Menu', window)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()   
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        game(1.00)
                    if event.key == pygame.K_2:
                        game(0.50)
                    if event.key == pygame.K_3:
                        game(0.25)
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_4:
                        level_menu_running = False


def main_menu(window):
    
    while True:
        draw_menu('1.Start. \n2.Level. \n3.Exit. ', window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()   
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game(1.00)
                if event.key == pygame.K_2:
                    level_menu(window)
                if event.key == pygame.K_3:
                    sys.exit()
                if event.key == pygame.K_ESCAPE:
                    sys.exit()


if __name__ == '__main__':
    pygame.font.init()
    window = pygame.display.set_mode(game_resolution)
    pygame.display.set_caption('Tetris')
    main_menu(window)
