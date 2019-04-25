import random

class Shape:
  __S = [['.....',
          '......',
          '..00..',
          '.00...',
          '.....'],
         ['.....',
          '..0..',
          '..00.',
          '...0.',
          '.....']]

  __Z = [['.....',
          '.....',
          '.00..',
          '..00.',
          '.....'],
         ['.....',
          '..0..',
          '.00..',
          '.0...',
          '.....']]

  __I = [['..0..',
          '..0..',
          '..0..',
          '..0..',
          '.....'],
         ['.....',
          '0000.',
          '.....',
          '.....',
          '.....']]

  __O = [['.....',
          '.....',
          '.00..',
          '.00..',
          '.....']]

  __J = [['.....',
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

  __L = [['.....',
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

  __T = [['.....',
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

  __shapes = [__S, __Z, __I, __O, __J, __L, __T]
  __colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0),
            (255, 165, 0), (0, 0, 255), (128, 0, 128)]


  def __init__(self, x, y, shape):
    self.x = x
    self.y = y
    self.shape = shape
    self.color = self.__colors[self.__shapes.index(shape)]
    self.rotation = 0


  @classmethod
  def get_rand_shape(cls):
    return Shape(5, 0, random.choice(cls.__shapes))
