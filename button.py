import pygame

class Button:
  color = (160, 160, 0)

  def __init__(self, pos, width, height, text_in):
    self.rect = pygame.Rect(pos, (width, height))
    self.text = text_in

  def player_clicked_btn(self, pos):
    return self.rect.collidepoint(pos)

  def display(self, screen, font):
    if self.rect.collidepoint(pygame.mouse.get_pos()):
      self.color = (255, 255, 255)
    else:
      self.color = (160, 160, 0)

    text_surface = font.render(self.text, True, self.color)
    text_rect = text_surface.get_rect()
    text_rect.center = self.rect.center
    screen.blit(text_surface, text_rect)

    pygame.draw.rect(screen, self.color, self.rect, 1)