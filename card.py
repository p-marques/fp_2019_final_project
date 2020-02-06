import pygame

class Card:
  show = True
  active = True
  tick = 0

  def __init__(self, pos_x, pos_y, width, height, in_nugget):
    self.rect = pygame.Rect(pos_x, pos_y, width, height)
    self.rect_inner = self.get_inner_rect()
    self.nugget = in_nugget

  # Aesthetic reasons
  def get_inner_rect(self):
    rect = self.rect.copy()
    rect.width -= rect.width * 0.12
    rect.height -= rect.height * 0.12
    rect.center = self.rect.center

    return rect

  # Player clicked the card?
  def handle_click(self, pos):
    if not self.active:
      return False
    elif self.rect.collidepoint(pos):
      self.show = False
      return True

  def show_card(self):
    self.show = True

  def deactivate_card(self):
    self.active = False

  def display(self, screen):
    if not self.active: # If card is not active it doesn't get displayed
      return

    if (self.show):
      color = (0, 150, 80)
      color_2 = (0, 190, 0)
      if self.rect.collidepoint(pygame.mouse.get_pos()): # Hover color change
        color = (255, 255, 255)
        color_2 = (200, 200, 200)

      pygame.draw.rect(screen, color, self.rect, 0)
      pygame.draw.rect(screen, color_2, self.rect_inner, 0)

    else:
      self.nugget.display(screen, self.rect)