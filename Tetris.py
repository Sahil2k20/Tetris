import pygame
import random

pygame.init()
pygame.font.init()

pygame.mixer.music.load("background.mp3")
clear = pygame.mixer.Sound("clear.wav")
fall = pygame.mixer.Sound("fall.wav")
line = pygame.mixer.Sound("line.wav")
lose = pygame.mixer.Sound("lose.wav")

# GLOBALS VARS
s_width = 1500
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 5
top_left_y = s_height - play_height

top_left_x1 = (s_width - play_width) // 2
top_left_y1 = s_height - play_height

top_left_x2 = (s_width - play_width) // 1.3
top_left_y2 = s_height - play_height

# SHAPE FORMATS

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
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

O = [['.....',
      '.....',
      '.00..',
      '.00..',
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

# shapes = [S, Z, I, O, J, L, T]
shapes = [I]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# index 0 - 6 represent shape


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


class Attributes:
    def __init__(self, locked_positions, change_piece, current_piece, next_piece, fall_time, fall_speed, level_time, score):
        self.locked_positions = locked_positions
        self.change_piece = change_piece
        self.current_piece = current_piece
        self.next_piece = next_piece
        self.fall_time = fall_time
        self.fall_speed = fall_speed
        self.level_time = level_time
        self.score = score


def create_grid(locked_positions):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    # finds current shape
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            # if 0 exists, add that to position
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        # fixes offset on screen so it can be displayed better
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    # converts above list: [[(0, 1)], [(2, 3)]] -> [(0, 1), (2, 3)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            # check if in grid
            if pos[1] > -1:
                return False
    return True


def valid_space2(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    # converts above list: [[(0, 1)], [(2, 3)]] -> [(0, 1), (2, 3)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            # check if in grid
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape(piece_type):
    return Piece(5, 0, shapes[piece_type])


def draw_text(surface, text, size, color):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (s_width / 2 - 110, 30))


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (
        top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))


def draw_text_middle2(surface, text, size, color):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (
        top_left_x2 + play_width / 2 - (label.get_width() / 2), top_left_y2 + play_height / 2 - label.get_height() / 2))


def draw_grid(surface, grid, sx, sy):
    for i in range(len(grid)):
        # draws horizontal lines
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            # draws vertical lines
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy),
                             (sx + j * block_size, sy + play_height))


def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        # checks if black squares on row
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            # gets every position in row
            for j in range(len(row)):
                try:
                    # removes color row from grid
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:
        # sorts list: [(0, 1), (0, 0)] -> [(0, 0), (0, 1)]
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            # everything above 'y' row will be moved down
            if y < ind:
                # shifts everything from above row to a new lower row
                new_key = (x, y + inc)
                locked[new_key] = locked.pop(key)

    return inc


def clear_rows2(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        # checks if black squares on row
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            # gets every position in row
            for j in range(len(row)):
                try:
                    # removes color row from grid
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:
        # sorts list: [(0, 1), (0, 0)] -> [(0, 0), (0, 1)]
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            # everything above 'y' row will be moved down
            if y < ind:
                # shifts everything from above row to a new lower row
                new_key = (x, y + inc)
                locked[new_key] = locked.pop(key)

    return inc


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('arial', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    # defining where the next shape box will be
    sx = top_left_x - play_width + 100
    sy = top_left_y + play_height / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color,
                                 (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def draw_next_shape2(shape, surface):
    font = pygame.font.SysFont('arial', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    # defining where the next shape box will be
    sx = top_left_x2 + play_width + 50
    sy = top_left_y2 + play_height / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color,
                                 (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def update_score(nscore):
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def update_score2(nscore):
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


def draw_scores(surface, score=0):
    font = pygame.font.SysFont('arial', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (660, 30))

    font = pygame.font.SysFont('arial', 30)

    label = font.render('Score: ' + str(score), 1, (255, 255, 255))

    # defining where the next shape box will be
    sx = top_left_x - play_width + 100
    sy = top_left_y + play_height / 2 - 100

    surface.blit(label, (sx + 10, sy + 160))


def draw_scores2(surface, score=0):
    font = pygame.font.SysFont('arial', 30)

    label = font.render('Score: ' + str(score), 1, (255, 255, 255))

    # defining where the next shape box will be
    sx2 = top_left_x2 + play_width + 50
    sy2 = top_left_y2 + play_height / 2 - 100

    surface.blit(label, (sx2 + 10, sy2 + 160))


def draw_window(surface, grid, tlx, tly, last_score=str(0)):

    font = pygame.font.SysFont('arial', 30)

    label = font.render('High Score: ' + str(last_score), 1, (255, 255, 255))

    # defining where the next shape box will be
    sx = 650
    sy = 20

    surface.blit(label, (sx - 10, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (tlx + j * block_size, tly + i * block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (tlx, tly, play_width, play_height), 5)

    draw_grid(surface, grid, tlx, tly)


def main(win):
    pygame.mixer.music.play(20)
    last_score = max_score()

    current_index = random.randint(0, len(shapes) - 1)
    next_index = random.randint(0, len(shapes) - 1)

    pieces1 = get_shape(current_index)
    pieces2 = get_shape(current_index)

    queue1 = []
    queue2 = []

    piece1 = Attributes({}, False, pieces1, get_shape(next_index), 0, 0.5, 0, 0)
    piece2 = Attributes({}, False, pieces2, get_shape(next_index), 0, 0.5, 0, 0)

    clock = pygame.time.Clock()

    run = True
    lost1 = True
    lost2 = True

    while run:
        grid = create_grid(piece1.locked_positions)
        # checks how long while loop has run and adds that
        piece1.fall_time += clock.get_rawtime()
        piece1.level_time += clock.get_rawtime()

        if piece1.level_time / 1000 > 5:
            piece1.level_time = 0
            if piece1.fall_speed > 0.12:
                piece1.fall_speed -= 0.0005

        if piece1.fall_time / 1000 > piece1.fall_speed:
            piece1.fall_time = 0
            piece1.current_piece.y += 1
            if not (valid_space(piece1.current_piece, grid)) and piece1.current_piece.y > 0:
                piece1.current_piece.y -= 1
                # locks the piece in place
                piece1.change_piece = True

        grid2 = create_grid(piece2.locked_positions)
        # checks how long while loop has run and adds that
        piece2.fall_time += clock.get_rawtime()
        piece2.level_time += clock.get_rawtime()

        clock.tick()

        if piece2.level_time / 1000 > 5:
            piece2.level_time = 0
            if piece2.fall_speed > 0.12:
                piece2.fall_speed -= 0.0005

        if piece2.fall_time / 1000 > piece2.fall_speed:
            piece2.fall_time = 0
            piece2.current_piece.y += 1
            if not (valid_space2(piece2.current_piece, grid2)) and piece2.current_piece.y > 0:
                piece2.current_piece.y -= 1
                # locks the piece in place
                piece2.change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    piece1.current_piece.x -= 1
                    if not (valid_space(piece1.current_piece, grid)):
                        piece1.current_piece.x += 1

                if event.key == pygame.K_d:
                    piece1.current_piece.x += 1
                    if not (valid_space(piece1.current_piece, grid)):
                        piece1.current_piece.x -= 1

                if event.key == pygame.K_s:
                    piece1.current_piece.y += 5
                    if not (valid_space(piece1.current_piece, grid)):
                        piece1.current_piece.y -= 5

                if event.key == pygame.K_w:
                    piece1.current_piece.rotation += 1
                    if not (valid_space(piece1.current_piece, grid)):
                        piece1.current_piece.rotation -= 1

                if event.key == pygame.K_LEFT:
                    piece2.current_piece.x -= 1
                    if not (valid_space2(piece2.current_piece, grid2)):
                        piece2.current_piece.x += 1

                if event.key == pygame.K_RIGHT:
                    piece2.current_piece.x += 1
                    if not (valid_space2(piece2.current_piece, grid2)):
                        piece2.current_piece.x -= 1

                if event.key == pygame.K_DOWN:
                    piece2.current_piece.y += 5
                    if not (valid_space2(piece2.current_piece, grid2)):
                        piece2.current_piece.y -= 5

                if event.key == pygame.K_UP:
                    piece2.current_piece.rotation += 1
                    if not (valid_space2(piece2.current_piece, grid2)):
                        piece2.current_piece.rotation -= 1

        shape_pos = convert_shape_format(piece1.current_piece)
        shape_pos2 = convert_shape_format(piece2.current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = piece1.current_piece.color

        for i in range(len(shape_pos2)):
            x, y = shape_pos2[i]
            if y > -1:
                grid2[y][x] = piece2.current_piece.color

        if piece1.change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                piece1.locked_positions[p] = piece1.current_piece.color
            piece1.current_piece = piece1.next_piece

            if queue1 == []:
                if not check_lost(piece1.locked_positions):
                    next1 = random.randint(0, len(shapes) - 1)
                    if not check_lost(piece2.locked_positions):
                        queue2.append(next1)
                    piece1.next_piece = get_shape(next1)
            else:
                piece1.next_piece = get_shape(queue1.pop(0))

            piece1.change_piece = False
            cleared_rows1 = clear_rows(grid, piece1.locked_positions)
            if cleared_rows1 == 4:
                pygame.mixer.Sound.play(clear)
                piece1.score += 80
            elif 0 < cleared_rows1 < 4:
                pygame.mixer.Sound.play(line)
                piece1.score += cleared_rows1 * 10
            else:
                pygame.mixer.Sound.play(fall)

        if piece2.change_piece:
            for pos2 in shape_pos2:
                p = (pos2[0], pos2[1])
                piece2.locked_positions[p] = piece2.current_piece.color
            piece2.current_piece = piece2.next_piece

            if queue2 == []:
                if not check_lost(piece2.locked_positions):
                    next2 = random.randint(0, len(shapes) - 1)
                    if not check_lost(piece1.locked_positions):
                        queue1.append(next2)
                    piece2.next_piece = get_shape(next2)
            else:
                piece2.next_piece = get_shape(queue2.pop(0))

            piece2.change_piece = False
            cleared_rows2 = clear_rows2(grid2, piece2.locked_positions)
            if cleared_rows2 == 4:
                pygame.mixer.Sound.play(clear)
                piece2.score += 80
            elif 0 < cleared_rows2 < 4:
                pygame.mixer.Sound.play(line)
                piece2.score += cleared_rows2 * 10
            else:
                pygame.mixer.Sound.play(fall)

        win.fill((0, 0, 0))

        draw_window(win, grid, top_left_x, top_left_y, last_score)
        draw_window(win, grid2, top_left_x2, top_left_y2, last_score)

        draw_scores(win, piece1.score)
        draw_scores2(win, piece2.score)

        draw_next_shape(piece1.next_piece, win)
        draw_next_shape2(piece2.next_piece, win)

        pygame.display.update()

        if check_lost(piece1.locked_positions):
            while lost1:
                pygame.mixer.Sound.play(lose)
                lost1 = False
            draw_text_middle(win, "You Lost", 80, (255, 255, 255))
            pygame.display.update()
            update_score(piece1.score)

        if check_lost(piece2.locked_positions):
            while lost2:
                pygame.mixer.Sound.play(lose)
                lost2 = False
            draw_text_middle2(win, "You Lost", 80, (255, 255, 255))
            pygame.display.update()
            update_score2(piece2.score)

        if check_lost(piece2.locked_positions) and check_lost(piece1.locked_positions):
            pygame.mixer.music.stop()
            pygame.time.delay(1500)
            run = False

# ------------------------------------------------------------------------------------------------------------------


def valid_space1(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def get_shape1():
    return Piece(5, 0, random.choice(shapes))


def clear_rows1(grid, locked):

    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                new_key = (x, y + inc)
                locked[new_key] = locked.pop(key)

    return inc


def draw_next_shape1(shape, surface):
    font = pygame.font.SysFont('arial', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    sx = top_left_x1 + play_width + 50
    sy = top_left_y1 + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color,
                                 (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def update_score1(nscore):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def draw_window1(surface, grid, score=0, last_score=str(0)):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('arial', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x1 + play_width / 2 - (label.get_width() / 2), 30))

    # current score
    font = pygame.font.SysFont('arial', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))

    sx = top_left_x1 + play_width + 50
    sy = top_left_y1 + play_height/2 - 100

    surface.blit(label, (sx + 20, sy + 160))
    # last score
    label = font.render('High Score: ' + last_score, 1, (255, 255, 255))

    sx = top_left_x1 - 250
    sy = top_left_y1 + 200

    surface.blit(label, (sx + 20, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x1 + j*block_size, top_left_y1 + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x1, top_left_y1, play_width, play_height), 5)

    draw_grid(surface, grid, top_left_x1, top_left_y1)


def draw_text_middle1(surface, text, size, color):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (
        top_left_x1 + play_width / 2 - (label.get_width() / 2), top_left_y1 + play_height / 2 - label.get_height() / 2))


def main1(win):
    pygame.mixer.music.play(20)
    last_score = max_score()
    locked_positions = {}

    change_piece = False
    run = True
    current_piece = get_shape1()
    next_piece = get_shape1()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.0005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space1(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space1(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space1(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 5
                    if not(valid_space1(current_piece, grid)):
                        current_piece.y -= 5
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space1(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape1()
            change_piece = False
            cleared_rows1 = clear_rows1(grid, locked_positions)
            if cleared_rows1 == 4:
                pygame.mixer.Sound.play(clear)
                score += 80
            elif 0 < cleared_rows1 < 4:
                pygame.mixer.Sound.play(line)
                score += cleared_rows1 * 10
            else:
                pygame.mixer.Sound.play(fall)

        draw_window1(win, grid, score, last_score)
        draw_next_shape1(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(lose)
            draw_text_middle1(win, "You Lost", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score1(score)


def main_menu(win):
    run = True

    while run:
        win.fill((0, 0, 0))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if 750 + 200 - 110 > mouse[0] > 750 - 110 and 300 + 50 > mouse[1] > 300:
            pygame.draw.rect(win, (200, 200, 200), (750 - 110, 300, 200, 50))
            if click[0] == 1:
                main1(win)
        else:
            pygame.draw.rect(win, (255, 255, 255), (750 - 110, 300, 200, 50))

        if 750 + 200 - 110 > mouse[0] > 750 - 110 and 450 + 50 > mouse[1] > 450:
            pygame.draw.rect(win, (200, 200, 200), (750 - 110, 450, 200, 50))
            if click[0] == 1:
                main(win)
        else:
            pygame.draw.rect(win, (255, 255, 255), (750 - 110, 450, 200, 50))

        font = pygame.font.SysFont('arial', 30)
        label = font.render('One Player', 1, (0, 0, 0))

        win.blit(label, (790 - 110, 305))

        font = pygame.font.SysFont('arial', 30)
        label = font.render('Two Player', 1, (0, 0, 0))

        win.blit(label, (790 - 110, 455))

        draw_text(win, "Tetris", 90, (255, 255, 255))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


window = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(window)  # start game
