import pygame

from Shape import Shape

class Player: 
  
  def __init__(self, id):
    self.__id = id

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


  def create_grid(self):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in self.locked_positions:
                c = self.locked_positions[(j, i)]
                grid[i][j] = c
    return grid


  def check_lost(self):
      return False


  def update(self):
    grid = self.create_grid()

    if not self.check_lost():
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
        if not (valid_space(self.current_piece, grid)) and self.current_piece.y > 0:
          self.current_piece.y -= 1
          self.change_piece = True

      shape_pos = convert_shape_format(self.current_piece)

      for i in range(len(shape_pos)):
        x, y = shape_pos[i]
        if y > -1:
          grid[y][x] = self.current_piece.color

      if self.change_piece:
        for pos in shape_pos:
          p = (pos[0], pos[1])
          self.locked_positions[p] = self.current_piece.color

        self.current_piece = self.next_piece
        self.next_piece = Shape.get_rand_shape()
        self.change_piece = False
        self.score += clear_rows(grid, self.locked_positions) * 10


  def draw(self, win):
    self._draw_window(win, grid, top_left_x, top_left_y, last_score)
    self._draw_scores(win, score)
    self._draw_next_shape(next_piece, win)

    if game_over:
      draw_text_middle(win, "You Lost", 80, (255, 255, 255))
      pygame.display.update()
      pygame.time.delay(1500)
      # run = False
      update_score(score)



  def _draw_window(self):
    pass

  def _draw_grid(self):
    pass

  def _draw_next_shape(self):
    pass

  def _draw_text_middle(self):
    pass