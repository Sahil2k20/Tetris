import pygame
import random

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 1500
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 5
top_left_y = s_height - play_height

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

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# index 0 - 6 represent shape


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


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


def get_shape():
    return Piece(5, 0, random.choice(shapes))


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


# noinspection PyBroadException
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


# noinspection PyBroadException
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
    pygame.font.init()

    font = pygame.font.SysFont('arial', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (tlx + play_width / 2 - (label.get_width() / 2), 30))

    # current score
    font = pygame.font.SysFont('arial', 30)

    label = font.render('High Score: ' + str(last_score), 1, (255, 255, 255))

    # defining where the next shape box will be
    sx = 650
    sy = 20

    surface.blit(label, (sx + 10, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (tlx + j * block_size, tly + i * block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (tlx, tly, play_width, play_height), 5)

    draw_grid(surface, grid, tlx, tly)


def main(win):
    last_score = max_score()
    locked_positions = {}
    locked_positions2 = {}

    change_piece = False
    current_piece = get_shape()
    next_piece = get_shape()

    change_piece2 = False
    current_piece2 = get_shape()
    next_piece2 = get_shape()

    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5
    level_time = 0
    score = 0

    clock2 = pygame.time.Clock()
    fall_time2 = 0
    fall_speed2 = 0.5
    level_time2 = 0
    score2 = 0

    run = True

    while run:
        grid = create_grid(locked_positions)
        # checks how long while loop has run and adds that
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        grid2 = create_grid(locked_positions2)
        # checks how long while loop has run and adds that
        fall_time2 += clock.get_rawtime()
        level_time2 += clock.get_rawtime()
        clock2.tick()

        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.0005

        if level_time2 / 1000 > 5:
            level_time2 = 0
            if fall_speed2 > 0.12:
                fall_speed2 -= 0.0005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                # locks the piece in place
                change_piece = True

        if fall_time2 / 1000 > fall_speed2:
            fall_time2 = 0
            current_piece2.y += 1
            if not (valid_space2(current_piece2, grid2)) and current_piece2.y > 0:
                current_piece2.y -= 1
                # locks the piece in place
                change_piece2 = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    current_piece.x -= 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1

                if event.key == pygame.K_d:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1

                if event.key == pygame.K_s:
                    current_piece.y += 5
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 5

                if event.key == pygame.K_w:
                    current_piece.rotation += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

                if event.key == pygame.K_LEFT:
                    current_piece2.x -= 1
                    if not (valid_space2(current_piece2, grid2)):
                        current_piece2.x += 1

                if event.key == pygame.K_RIGHT:
                    current_piece2.x += 1
                    if not (valid_space2(current_piece2, grid2)):
                        current_piece2.x -= 1

                if event.key == pygame.K_DOWN:
                    current_piece2.y += 5
                    if not (valid_space2(current_piece2, grid2)):
                        current_piece2.y -= 5

                if event.key == pygame.K_UP:
                    current_piece2.rotation += 1
                    if not (valid_space2(current_piece2, grid2)):
                        current_piece2.rotation -= 1

        shape_pos = convert_shape_format(current_piece)
        shape_pos2 = convert_shape_format(current_piece2)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        for i in range(len(shape_pos2)):
            x, y = shape_pos2[i]
            if y > -1:
                grid2[y][x] = current_piece2.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        if change_piece2:
            for pos2 in shape_pos2:
                p = (pos2[0], pos2[1])
                locked_positions2[p] = current_piece2.color
            current_piece2 = next_piece2
            next_piece2 = get_shape()
            change_piece2 = False
            score2 += clear_rows2(grid2, locked_positions2) * 10

        win.fill((0, 0, 0))

        draw_window(win, grid, top_left_x, top_left_y, last_score)
        draw_window(win, grid2, top_left_x2, top_left_y2, last_score)

        draw_scores(win, score)
        draw_scores2(win, score2)

        draw_next_shape(next_piece, win)
        draw_next_shape2(next_piece2, win)

        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(win, "You Lost", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)

        if check_lost(locked_positions2):
            draw_text_middle2(win, "You Lost", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score2(score2)


window = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main(window)  # start game
