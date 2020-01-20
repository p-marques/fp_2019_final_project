import pygame

class Button:
  color = (160, 160, 0)

  def __init__(self, pos, width, height, text_in):
    self.rect = pygame.Rect(pos, (width, height))
    self.text = text_in

  def display(self, screen):
    if self.rect.collidepoint(pygame.mouse.get_pos()):
      self.color = (255, 255, 255)
    else:
      self.color = (160, 160, 0)

    pygame.draw.rect(screen, self.color, self.rect, 1)

  def display_text(self, screen, font):
    if self.rect.collidepoint(pygame.mouse.get_pos()):
      self.color = (255, 255, 255)
    else:
      self.color = (160, 160, 0)

    font.render_to(screen, (self.rect.x + 10, self.rect.y + 10), self.text, self.color)

  def player_clicked_btn(self, pos):
    if self.rect.collidepoint(pos):
      return True
    else:
      return False