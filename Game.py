import pygame

from Shape import Shape
from Player import Player

class Game:
  __is_running = False
  __players = []

  s_width = 1500
  s_height = 7000

  play_width = 300     # meaning 300 // 10 = 30 width per block
  play_height = 600     # meaning 600 // 20 = 20 height per block

  block_size = 30

  # top_left_x = (s_width - play_width) // 5
  # top_left_y = s_height - play_height

  # top_left_x2 = (s_width - play_width) // 1.3
  # top_left_y2 = s_height - play_height

  scores_fn = 'scores.txt'  # Highscores save file
  max_score = 0


  @classmethod
  def run(cls):
    pygame.font.init()

    win = pygame.display.set_mode((cls.s_width, cls.s_height))
    pygame.display.set_caption('Tetris')

    max_score = cls._max_score()
    last_score = max_score


    num_players = 2

    cls.__players = [Player(id, ((cls.s_width - cls.play_width) // 5 if id ==
                                  0 else 1.3, (cls.s_height, cls.play_height))) for id in range(num_players)]


    cls.__is_running = True
    while cls.__is_running:
      # -------------------------------------------------
        # Begin Update Function
      for player in cls.__players:
        player.update()

        # End Update function
        # -------------------------------------------------

      # Begin Draw function
      # NOTE: called once per frame
      win.fill((0, 0, 0))

      for player in cls.__players:
        player.draw(win)


      # -------------------------------------------------
      # Render Screen
      # NOTE: Called once per frame
      pygame.display.update()

      # End Draw fucntion


  @classmethod
  def stop(cls):
    cls.__is_running = False



  # def draw_grid(self, surface, grid, sx, sy):
  #   for i in range(len(grid)):
  #     # draws horizontal lines
  #     pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * self.block_size), (sx + self.play_width, sy + i * self.block_size))
  #     for j in range(len(grid[i])):
  #       # draws vertical lines
  #       pygame.draw.line(surface, (128, 128, 128), (sx + j * self.block_size, sy), (sx + j * self.block_size, sy + self.play_height))

  # def draw_window(self, surface, grid, tlx, tly, last_score=str(0)):
  #   pygame.font.init()

  #   font = pygame.font.SysFont('arial', 60)
  #   label = font.render('Tetris', 1, (255, 255, 255))

  #   surface.blit(label, (tlx + self.play_width / 2 - (label.get_width() / 2), 30))

  #   # current score
  #   font = pygame.font.SysFont('arial', 30)

  #   label = font.render('High Score: ' + str(last_score), 1, (255, 255, 255))

  #   # defining where the next shape box will be
  #   sx = 650
  #   sy = 20

  #   surface.blit(label, (sx + 10, sy + 160))

  #   for i in range(len(grid)):
  #       for j in range(len(grid[i])):
  #           pygame.draw.rect(surface, grid[i][j],
  #                            (tlx + j * self.block_size, tly + i * self.block_size, self.block_size, self.block_size), 0)

  #   pygame.draw.rect(surface, (255, 0, 0),
  #                    (tlx, tly, self.play_width, self.play_height), 5)

  #   self.draw_grid(surface, grid, tlx, tly)

 


  # def draw_text_middle(self, surface, text, size, color):
  #   font = pygame.font.SysFont("arial", size, bold=True)
  #   label = font.render(text, 1, color)

  #   surface.blit(label, (
  #       self.top_left_x + self.play_width / 2 - (label.get_width() / 2), self.top_left_y + self.play_height / 2 - label.get_height() / 2))

  # def draw_text_middle2(self, surface, text, size, color):
  #   font = pygame.font.SysFont("arial", size, bold=True)
  #   label = font.render(text, 1, color)

  #   surface.blit(label, (
  #       self.top_left_x2 + self.play_width / 2 - (label.get_width() / 2), self.top_left_y2 + self.play_height / 2 - label.get_height() / 2))







  # def draw_next_shape(self, shape, surface):
  #   font = pygame.font.SysFont('arial', 30)
  #   label = font.render('Next Shape', 1, (255, 255, 255))

  #   # defining where the next shape box will be
  #   sx = self.top_left_x - self.play_width + 100
  #   sy = self.top_left_y + self.play_height / 2 - 100
  #   format = shape.shape[shape.rotation % len(shape.shape)]

  #   for i, line in enumerate(format):
  #       row = list(line)
  #       for j, column in enumerate(row):
  #           if column == '0':
  #               pygame.draw.rect(surface, shape.color,
  #                                (sx + j * self.block_size, sy + i * self.block_size, self.block_size, self.block_size), 0)

  #   surface.blit(label, (sx + 10, sy - 30))

  # def draw_next_shape2(self, shape, surface):
  #   font = pygame.font.SysFont('arial', 30)
  #   label = font.render('Next Shape', 1, (255, 255, 255))

  #   # defining where the next shape box will be
  #   sx = self.top_left_x2 + self.play_width + 50
  #   sy = self.top_left_y2 + self.play_height / 2 - 100
  #   format = shape.shape[shape.rotation % len(shape.shape)]

  #   for i, line in enumerate(format):
  #       row = list(line)
  #       for j, column in enumerate(row):
  #           if column == '0':
  #               pygame.draw.rect(surface, shape.color,
  #                                (sx + j * self.block_size, sy + i * self.block_size, self.block_size, self.block_size), 0)

  #   surface.blit(label, (sx + 10, sy - 30))





  @classmethod
  def update_score(cls, nscore):
    if nscore > cls.max_score:
        with open(cls.scores_fn, 'w') as f:
            f.write(nscore)


  @classmethod
  def _max_score(cls):
    try:
        with open(cls.scores_fn, 'r') as f:
            lines = f.readlines()
            if len(lines) > 0:
                score = lines[0].strip()
                return score
    except IOError:
        # Create empty file
        open(cls.scores_fn, 'w').close()
        return ""






  # def draw_scores(self, surface, score=0):
  #   font = pygame.font.SysFont('arial', 30)

  #   label = font.render('Score: ' + str(score), 1, (255, 255, 255))

  #   # defining where the next shape box will be
  #   sx = self.top_left_x - self.play_width + 100
  #   sy = self.top_left_y + self.play_height / 2 - 100

  #   surface.blit(label, (sx + 10, sy + 160))

  # def draw_scores2(self, surface, score=0):
  #   font = pygame.font.SysFont('arial', 30)

  #   label = font.render('Score: ' + str(score), 1, (255, 255, 255))

  #   # defining where the next shape box will be
  #   sx2 = self.top_left_x2 + self.play_width + 50
  #   sy2 = self.top_left_y2 + self.play_height / 2 - 100

  #   surface.blit(label, (sx2 + 10, sy2 + 160))
