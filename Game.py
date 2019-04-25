import pygame

class Game:

  def __init__(self):
    self.__is_running = False

    self.s_width = 1500
    self.s_height = 7000

    self.play_width = 300     # meaning 300 // 10 = 30 width per block
    self.play_height = 600     # meaning 600 // 20 = 20 height per block

    self.block_size = 30

    self.top_left_x = (self.s_width - self.play_width) // 5
    self.top_left_y = self.s_height - self.play_height

    self.top_left_x2 = (self.s_width - self.play_width) // 1.3
    self.top_left_y2 = self.s_height - self.play_height

    self.scores_fn = 'scores.txt'  # Highscores save file
    self.max_score = 0




  def run(self):
    win = pygame.display.set_mode((self.s_width, self.s_height))
    pygame.display.set_caption('Tetris')

    max_score = self._max_score()
    last_score = max_score
    run = True

    # -------------------------------------------------
    #  Class Instance 1

    locked_positions = {}
    change_piece = False
    current_piece = get_shape()
    next_piece = get_shape()

    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5
    level_time = 0
    score = 0
    game_over = False

    # -------------------------------------------------
    # Class Instance 2

    locked_positions2 = {}
    change_piece2 = False
    current_piece2 = get_shape()
    next_piece2 = get_shape()

    clock2 = pygame.time.Clock()
    fall_time2 = 0
    fall_speed2 = 0.5
    level_time2 = 0
    score2 = 0
    game_over2 = False


    while self.__is_running:
      # -------------------------------------------------
        # Begin Update Function

        # -------------------------------------------------
        # Class Instance 1

        grid = create_grid(locked_positions)
        game_over = check_lost(locked_positions)

        if not game_over:
            # checks how long while loop has run and adds that
            fall_time += clock.get_rawtime()
            level_time += clock.get_rawtime()
            clock.tick()

            if level_time / 1000 > 5:
                level_time = 0
                if fall_speed > 0.12:
                    fall_speed -= 0.0005

            if fall_time / 1000 > fall_speed:
                fall_time = 0
                current_piece.y += 1
                if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                    current_piece.y -= 1
                    # locks the piece in place
                    change_piece = True

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
                next_piece = get_shape()
                change_piece = False
                score += clear_rows(grid, locked_positions) * 10

        # -------------------------------------------------
        # Class Instance 2

        grid2 = create_grid(locked_positions2)
        game_over2 = check_lost(locked_positions2)

        if not game_over2:
            # checks how long while loop has run and adds that
            fall_time2 += clock.get_rawtime()
            level_time2 += clock.get_rawtime()
            clock2.tick()

            if level_time2 / 1000 > 5:
                level_time2 = 0
                if fall_speed2 > 0.12:
                    fall_speed2 -= 0.0005

            if fall_time2 / 1000 > fall_speed2:
                fall_time2 = 0
                current_piece2.y += 1
                if not (valid_space2(current_piece2, grid2)) and current_piece2.y > 0:
                    current_piece2.y -= 1
                    # locks the piece in place
                    change_piece2 = True

            for event in pygame.event.get():
                # Event polling should only be used for window or sigterm events
                if event.type == pygame.QUIT:
                    run = False

                # TODO: refactor all of the player controls
                # @link https://www.pygame.org/docs/ref/key.html
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

            shape_pos2 = convert_shape_format(current_piece2)

            for i in range(len(shape_pos2)):
                x, y = shape_pos2[i]
                if y > -1:
                    grid2[y][x] = current_piece2.color

            if change_piece2:
                for pos2 in shape_pos2:
                    p = (pos2[0], pos2[1])
                    locked_positions2[p] = current_piece2.color
                current_piece2 = next_piece2
                next_piece2 = get_shape()
                change_piece2 = False
                score2 += clear_rows2(grid2, locked_positions2) * 10

        # End Update function
        # -------------------------------------------------
        # Begin Draw function

        win.fill((0, 0, 0))

        # -------------------------------------------------
        # Class Instance 1

        draw_window(win, grid, top_left_x, top_left_y, last_score)
        draw_scores(win, score)
        draw_next_shape(next_piece, win)

        if game_over:
            draw_text_middle(win, "You Lost", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            # run = False
            update_score(score)

        # -------------------------------------------------
        # Class Instance 2

        draw_window(win, grid2, top_left_x2, top_left_y2, last_score)
        draw_scores2(win, score2)
        draw_next_shape2(next_piece2, win)

        if game_over2:
            draw_text_middle2(win, "You Lost", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            # run = False
            update_score(score2)

        # -------------------------------------------------
        # Render Screen
        pygame.display.update()

        # End Draw fucntion






  def draw_grid(self, surface, grid, sx, sy):
    for i in range(len(grid)):
      # draws horizontal lines
      pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * self.block_size), (sx + self.play_width, sy + i * self.block_size))
      for j in range(len(grid[i])):
        # draws vertical lines
        pygame.draw.line(surface, (128, 128, 128), (sx + j * self.block_size, sy), (sx + j * self.block_size, sy + self.play_height))

  def draw_window(self, surface, grid, tlx, tly, last_score=str(0)):
    pygame.font.init()

    font = pygame.font.SysFont('arial', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (tlx + self.play_width / 2 - (label.get_width() / 2), 30))

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
                             (tlx + j * self.block_size, tly + i * self.block_size, self.block_size, self.block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0),
                     (tlx, tly, self.play_width, self.play_height), 5)

    self.draw_grid(surface, grid, tlx, tly)






  def draw_text_middle(self, surface, text, size, color):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (
        self.top_left_x + self.play_width / 2 - (label.get_width() / 2), self.top_left_y + self.play_height / 2 - label.get_height() / 2))

  def draw_text_middle2(self, surface, text, size, color):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (
        self.top_left_x2 + self.play_width / 2 - (label.get_width() / 2), self.top_left_y2 + self.play_height / 2 - label.get_height() / 2))







  def draw_next_shape(self, shape, surface):
    font = pygame.font.SysFont('arial', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    # defining where the next shape box will be
    sx = self.top_left_x - self.play_width + 100
    sy = self.top_left_y + self.play_height / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color,
                                 (sx + j * self.block_size, sy + i * self.block_size, self.block_size, self.block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))

  def draw_next_shape2(self, shape, surface):
    font = pygame.font.SysFont('arial', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    # defining where the next shape box will be
    sx = self.top_left_x2 + self.play_width + 50
    sy = self.top_left_y2 + self.play_height / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color,
                                 (sx + j * self.block_size, sy + i * self.block_size, self.block_size, self.block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))





  def update_score(self, nscore):
    if nscore > self.max_score:
        with open(self.scores_fn, 'w') as f:
            f.write(nscore)

  def _max_score(self):
    try:
        with open(self.scores_fn, 'r') as f:
            lines = f.readlines()
            if len(lines) > 0:
                score = lines[0].strip()
                return score
    except IOError:
        # Create empty file
        open(self.scores_fn, 'w').close()
        return ""






  def draw_scores(self, surface, score=0):
    font = pygame.font.SysFont('arial', 30)

    label = font.render('Score: ' + str(score), 1, (255, 255, 255))

    # defining where the next shape box will be
    sx = self.top_left_x - self.play_width + 100
    sy = self.top_left_y + self.play_height / 2 - 100

    surface.blit(label, (sx + 10, sy + 160))

  def draw_scores2(self, surface, score=0):
    font = pygame.font.SysFont('arial', 30)

    label = font.render('Score: ' + str(score), 1, (255, 255, 255))

    # defining where the next shape box will be
    sx2 = self.top_left_x2 + self.play_width + 50
    sy2 = self.top_left_y2 + self.play_height / 2 - 100

    surface.blit(label, (sx2 + 10, sy2 + 160))
