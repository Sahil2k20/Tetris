import pygame

from Shape import Shape
from Player import Player


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


def run():
  pygame.font.init()

  win = pygame.display.set_mode((s_width, s_height))
  pygame.display.set_caption('Tetris')

  max_score = _max_score()
  last_score = max_score


  num_players = 2
  __players = [Player(id, ((s_width - play_width) // 5 if id ==
                                0 else 1.3, s_height - play_height)) for id in range(num_players)]


  __is_running = True
  while __is_running:
    # -------------------------------------------------
      # Begin Update Function
    for player in __players:
      player.update()

      # End Update function
      # -------------------------------------------------

    # Begin Draw function
    # NOTE: called once per frame
    win.fill((0, 0, 0))

    for player in __players:
      player.draw(win)


    # -------------------------------------------------
    # Render Screen
    # NOTE: Called once per frame
    pygame.display.update()

    # End Draw fucntion



def stop():
  __is_running = False




def update_score(nscore):
  if nscore > max_score:
      with open(scores_fn, 'w') as f:
          f.write(nscore)


def _max_score():
  try:
      with open(scores_fn, 'r') as f:
          lines = f.readlines()
          if len(lines) > 0:
              score = lines[0].strip()
              return score
  except IOError:
      # Create empty file
      open(scores_fn, 'w').close()
      return ""

