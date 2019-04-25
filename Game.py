import pygame

from Shape import Shape
from Player import Player

class Game:

  def __init__(self):
    self.__is_running = False
    self.__players = []

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
    pygame.font.init()

    win = pygame.display.set_mode((self.s_width, self.s_height))
    pygame.display.set_caption('Tetris')

    max_score = self._max_score()
    last_score = max_score

    num_players = 2


    self.__players = [Player(id) for id in range(num_players)]


    self.__is_running = True
    while self.__is_running:
      # -------------------------------------------------
        # Begin Update Function
      for player in self.__players:
        player.update()

        # End Update function
        # -------------------------------------------------

      # Begin Draw function
      win.fill((0, 0, 0))

      for player in self.__players:
        player.draw(win)

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
