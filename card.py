import pygame

class Card:
  show = True
  color = (0, 255, 0)

  def __init__(self, pos_x, pos_y, width, height):
    self.rect = pygame.Rect(pos_x, pos_y, width, height)
    pass

  def display(self, screen):
    if (self.show):
      pygame.draw.rect(screen, self.color, self.rect, 0)

  def handle_click(self, pos):
    if self.show and self.rect.collidepoint(pos):
      self.show = False
      self.tick = pygame.time.get_ticks()