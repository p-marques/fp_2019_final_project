import pygame

class Card:
  show = True
  color = (0, 0, 0)
  id = 0
  symbol = 0

  def __init__(self, id, pos_x, pos_y, width, height, symbol, color):
    self.rect = pygame.Rect(pos_x, pos_y, width, height)
    self.symbol = symbol
    self.color = color
    self.id = id

  def handle_click(self, pos):
    if self.show and self.rect.collidepoint(pos):
      self.show = False
      return True

    return False

  def show_card(self):
    self.show = True

  def display(self, screen):
    if (self.show):
      pygame.draw.rect(screen, (0, 255, 0), self.rect, 0)
    else:
      pygame.draw.rect(screen, self.color, self.rect, 3)
      center = (int(self.rect.x + (self.rect.width / 2)), int(self.rect.y + (self.rect.height / 2)))
      radius = int(self.rect.width / 2)
      if self.symbol == 0:  # square
        square = pygame.Rect((center[0] - radius / 2), (center[1] - radius / 2), radius, radius)
        pygame.draw.rect(screen, self.color, square, 0)
      elif self.symbol == 1:  # triangle
        triangle = ( (center[0], center[1] - radius / 2), ( center[0] - radius / 2, center[1] + radius / 2), ( center[0] + radius / 2, center[1] + radius / 2) )
        pygame.draw.polygon(screen, self.color, triangle)
      elif self.symbol == 2:  # circle
        pygame.draw.circle(screen, self.color, center, int(radius / 2))

  def __str__(self):
    return f"Cards id:{self.id}"