import pygame
import sys

from Shape import Shape
from Player import Player


is_running = False
players = []

s_width = 1500
s_height = 700

play_width = 300     # meaning 300 // 10 = 30 width per block
play_height = 600     # meaning 600 // 20 = 20 height per block

block_size = 30

scores_fn = 'scores.txt'  # Highscores save file
max_score = 0


def run():
  global is_running
  global players

  pygame.init()
  win = pygame.display.set_mode((s_width, s_height))
  pygame.display.set_caption('Tetris')

  # max_score = _max_score()
  # last_score = max_score


  num_players = 2
  players = [Player(id, (id * s_width / 2 + play_width, s_height - play_height)) for id in range(num_players)]
  # players = [Player(id, ((s_width - play_width) // 5 if id ==
  #                               0 else 1.3, s_height - play_height)) for id in range(num_players)]


  is_running = True
  while is_running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        stop()

    for player in players:
      player.update()

    win.fill((10, 10, 10))

    for player in players:
      player.draw(win)

    pygame.display.flip()

  pygame.display.quit()



def stop():
  global is_running
  is_running = False





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

