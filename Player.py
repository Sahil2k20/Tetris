import pygame

from Shape import Shape
import Game

class Player: 
  
  def __init__(self, id, origin):
    self.__id = id
    self._origin = origin
    self._grid = []

    self.locked_positions = {}
    self.change_piece = False
    self.current_piece = Shape.get_rand_shape()
    self.next_piece = Shape.get_rand_shape()
    self.clock = pygame.time.Clock()
    self.fall_time = 0
    self.fall_speed = 0.5
    self.level_time = 0
    self.score = 0
    self.game_over = False


  def _create_grid(self):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in self.locked_positions:
                c = self.locked_positions[(j, i)]
                grid[i][j] = c
    return grid


  def _is_game_over(self):
    for pos in self.locked_positions:
      x, y = pos
      if y < 1:
        return True

    return False


  def _valid_space(self, shape):
    accepted_pos = [[(j, i) for j in range(10) if self._grid[i]
                     [j] == (0, 0, 0)] for i in range(20)]
    # converts above list: [[(0, 1)], [(2, 3)]] -> [(0, 1), (2, 3)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = Shape.convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            # check if in grid
            if pos[1] > -1:
                return False
    return True


  def _clear_rows(self):
    inc = 0
    for i in range(len(self._grid) - 1, -1, -1):
        row = self._grid[i]
        # checks if black squares on row
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            # gets every position in row
            for j in range(len(row)):
                try:
                    # removes color row from grid
                    del self.locked_positions[(j, i)]
                except:
                    continue

    if inc > 0:
        # sorts list: [(0, 1), (0, 0)] -> [(0, 0), (0, 1)]
        for key in sorted(list(self.locked_positions), key=lambda x: x[1])[::-1]:
            x, y = key
            # everything above 'y' row will be moved down
            if y < ind:
                # shifts everything from above row to a new lower row
                new_key = (x, y + inc)
                self.locked_positions[new_key] = self.locked_positions.pop(key)

    return inc

  
  def _input(self):
    keys = pygame.key.get_pressed()
    if self.__id == 0:
      if keys[pygame.K_a]:
        self.current_piece.x -= 1
        if not self._valid_space(self.current_piece):
          self.current_piece.x += 1

      if keys[pygame.K_d]:
        self.current_piece.x += 1
        if not self._valid_space(self.current_piece):
          self.current_piece.x -= 1

      # if keys[pygame.K_s]
      # if keys[pygame.K_w]

    else: # id == 1
      if keys[pygame.K_LEFT]:
        # FIXME: duplicate code
        self.current_piece.x -= 1
        if not self._valid_space(self.current_piece):
          self.current_piece.x += 1

      if keys[pygame.K_RIGHT]:
        # FIXME: duplicate code
        self.current_piece.x += 1
        if not self._valid_space(self.current_piece):
          self.current_piece.x -= 1

      # if keys[pygame.K_DOWN]
      # if keys[pygame.K_UP]


  def update(self):
    self._grid = self._create_grid()

    if not self._is_game_over():
      self._input()

      self.fall_time += self.clock.get_rawtime()
      self.level_time += self.clock.get_rawtime()
      self.clock.tick()

      if self.level_time / 1000 > 5:
        self.level_time = 0
        if self.fall_time > 0.12:
          self.fall_speed -= 0.0005

      if self.fall_time / 1000 > self.fall_speed:
        self.fall_time = 0
        self.current_piece.y += 1
        if not (self._valid_space(self.current_piece)) and self.current_piece.y > 0:
          self.current_piece.y -= 1
          self.change_piece = True

      shape_pos = Shape.convert_shape_format(self.current_piece)

      for i in range(len(shape_pos)):
        x, y = shape_pos[i]
        if y > -1:
          self._grid[y][x] = self.current_piece.color

      if self.change_piece:
        for pos in shape_pos:
          p = (pos[0], pos[1])
          self.locked_positions[p] = self.current_piece.color

        self.current_piece = self.next_piece
        self.next_piece = Shape.get_rand_shape()
        self.change_piece = False
        self.score += self._clear_rows() * 10







  def draw(self, win):
    self._draw_window(win)
    self._draw_score(win)
    self._draw_next_shape(win)

    if self._is_game_over():
      self._draw_text_middle(win, "You Lost", 80, (255, 255, 255))
      # self._update_score(score)


  def _draw_window(self, surface):
    tlx, tly = self._origin
    grid = self._grid

    font = pygame.font.SysFont('arial', 60)

    label = font.render('Tetris', 1, (255, 255, 255))
    surface.blit(label, (tlx + Game.play_width /
                         2 - (label.get_width() / 2), 30))

    # current score
    font = pygame.font.SysFont('arial', 30)

    # label = font.render('High Score: ' + str(last_score), 1, (255, 255, 255))

    # defining where the next shape box will be
    # sx = 650
    # sy = 20

    # surface.blit(label, (sx + 10, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (tlx + j * Game.block_size, tly + i * Game.block_size, Game.block_size, Game.block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0),
                     (tlx, tly, Game.play_width, Game.play_height), 5)

    self._draw_grid(surface)


  def _draw_score(self, surface):
    pass
    # font = pygame.font.SysFont('arial', 30)

    # label = font.render('Score: ' + str(score), 1, (255, 255, 255))

    # # defining where the next shape box will be
    # sx = self.top_left_x - self.play_width + 100
    # sy = self.top_left_y + self.play_height / 2 - 100

    # surface.blit(label, (sx + 10, sy + 160))


  def _draw_grid(self, surface):
    grid = self._grid
    sx, sy = self._origin
    
    for i in range(len(grid)):
      for j in range(len(grid[i]) + 1):
        # draws horizontal lines
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * Game.block_size),
                        (sx + Game.play_width, sy + i * Game.block_size))
        
        # draws vertical lines
        pygame.draw.line(surface, (128, 128, 128), (sx + j * Game.block_size,
                                                    sy), (sx + j * Game.block_size, sy + Game.play_height))


  def _draw_next_shape(self, surface):
    shape = self.next_piece

    font = pygame.font.SysFont('arial', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    # defining where the next shape box will be
    sx = self._origin[0] - Game.play_width + 100
    sy = self._origin[1] + Game.play_height / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color,
                                 (sx + j * Game.block_size, sy + i * Game.block_size, Game.block_size, Game.block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


  def _draw_text_middle(self, surface, text, size, color):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (
        self._origin[0] + Game.play_width / 2 - (label.get_width() / 2), self._origin[1] + Game.play_height / 2 - label.get_height() / 2))
