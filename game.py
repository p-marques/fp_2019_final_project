import pygame
import random

from button import Button
from card import Card
from nugget import Nugget

class Game:
  tick = 0
  naked_cards_index = []
  cards_removed_count = 0

  def __init__(self, size, high_scores_manager, in_screen=(1280, 720)):
    self.grats_font = pygame.font.Font("resources/fonts/NotoSans-Regular.ttf", 40)
    self.size = size
    self.hs_manager = high_scores_manager
    self.exit_btn = Button((10, in_screen[1] - 50), 140, 40, "EXIT GAME")
    self.board_size = self.calculate_board_size(in_screen)
    self.card_size = self.calculate_card_size()
    self.nuggets = self.generate_nuggets()
    self.cards = self.generate_cards(in_screen)
    self.score = 0
    self.picks_since_last_correct = 0
    self.upload_hs_btn = Button((-10, -10), 360, 60, "Upload High Score")

  def calculate_board_size(self, screen):
    return screen[0] / 2, screen[1] - 50

  def calculate_card_size(self):
    return self.board_size[0] / self.size[0], self.board_size[1] / self.size[1]

  # Generate the correct number of nuggets according to game size
  def generate_nuggets(self):
    n = []

    for i in range(0, self.size[0] * self.size[1]):
      if i % 2 == 0:
        symbol = self.get_rand_symbol()
        color = self.get_rand_color()

      n.append(Nugget(symbol, color))

    random.shuffle(n)

    return n

  def get_random_nugget(self):
    i = random.randint(0, len(self.nuggets) - 1)
    return self.nuggets.pop(i)

  # Generates cards
  # Calculates card positions relative to board size
  def generate_cards(self, screen):
    cards = []
    spacing = 4

    for i in range(0, self.size[1]):
      row = []
      for j in range(0, self.size[0]):
        pos_x = (screen[0] / 2) - (self.board_size[0] / 2) + (self.card_size[0] * j) + (spacing * j) - (spacing / self.card_size[0])
        pos_y = (screen[1] / 2) - (self.board_size[1] / 2) + (self.card_size[1] * i) + (spacing * i) - (spacing / self.card_size[1])
        c = Card(pos_x, pos_y, self.card_size[0], self.card_size[1], self.get_random_nugget())
        row.append(c)

      cards.append(row)

    return cards

  def get_rand_color(self):
    return random.randint(40, 255), random.randint(40, 255), random.randint(40, 255)

  def get_rand_symbol(self): # 0 -> Square, 1 -> Triangle, 2 -> Circle, 3 -> kite
    return random.randint(0, 3)

  # Returns answer to 'keep playing?'
  def handle_click(self, pos):
    if self.exit_btn.player_clicked_btn(pos):
      return False

    if self.upload_hs_btn.player_clicked_btn(pos):
      self.upload_high_score()
      return False

    # checks cards for clicks
    # saves current time if 2 cards are selected
    for i in range(0, len(self.cards)):
      for j in range(0, len(self.cards[i])):
        if len(self.naked_cards_index) < 2 and self.cards[i][j].handle_click(pos):
          index = (i, j)
          if index not in self.naked_cards_index:
            self.naked_cards_index.append((i, j))
          if len(self.naked_cards_index) == 2:
            self.tick = pygame.time.get_ticks()

    return True

  def update_score(self, score_to_add):
    if self.score + score_to_add < 0:
      self.score = 0
    else:
      self.score += score_to_add

  def deactivate_naked_cards(self):
    for card_index in self.naked_cards_index:
      self.cards[card_index[0]][card_index[1]].deactivate_card()

    self.cards_removed_count += 2

  def compare_cards(self):
    card_A = self.cards[self.naked_cards_index[0][0]][self.naked_cards_index[0][1]]
    card_B = self.cards[self.naked_cards_index[1][0]][self.naked_cards_index[1][1]]
    
    if card_A.nugget.symbol == card_B.nugget.symbol and card_A.nugget.color == card_B.nugget.color:
      self.picks_since_last_correct = 0
      return True

    self.picks_since_last_correct += 1
    if self.picks_since_last_correct >= 2:
      self.update_score(-20 * (self.picks_since_last_correct - 1))

    return False

  def track_naked_cards(self):
    if pygame.time.get_ticks() - self.tick > 1500:
      if self.compare_cards():
        self.update_score(100)
        self.deactivate_naked_cards()
    
      for card_index in self.naked_cards_index:
        self.cards[card_index[0]][card_index[1]].show_card()

      self.naked_cards_index = []

  def upload_high_score(self):
    self.hs_manager.post_high_score(self.score, self.size)

  def display_ranked_score(self, screen, res):
    score_surface = self.grats_font.render(f"A Ranked Score of {str(self.score * self.size[0] * self.size[1])} is in the Top 10!", True, (160, 160, 0))
    score_rect = score_surface.get_rect()
    score_rect.center = int(res[0] / 2), (int(res[1] / 2) + score_rect.height + 10)
    screen.blit(score_surface, score_rect)

    self.upload_hs_btn.rect.centerx = score_rect.centerx
    self.upload_hs_btn.rect.bottom = res[1] - 10
    self.upload_hs_btn.display(screen, self.grats_font)

  # Display game over screen. Centers text correctly according to screen size
  def display_game_over(self, screen, res):
    grats_surface = self.grats_font.render("Congratulations! You Win!", True, (160, 160, 0))
    grats_rect = grats_surface.get_rect()
    grats_rect.center = int(res[0] / 2), int(res[1] / 2) - grats_rect.height / 2
    screen.blit(grats_surface, grats_rect)

    self.display_score(screen, self.grats_font, res, True)

    # Check to see if player is on top 10
    if self.hs_manager.is_player_in_top_10(self.size, self.score):
      self.display_ranked_score(screen, res)

  # Display score. Position and font change when it's game over
  def display_score(self, screen, font, res, game_over = False):
    score_surface = font.render(f"Score: {str(self.score)}", True, (160, 160, 0))
    score_rect = score_surface.get_rect()

    if game_over:
      score_rect.center = int(res[0] / 2), int(res[1] / 2) + score_rect.height / 2
    else:
      score_rect.topleft = (10, 10)

    screen.blit(score_surface, score_rect)
    

  def display(self, screen, font, res):
    self.exit_btn.display(screen, font)

    if len(self.naked_cards_index) == 2:
      self.track_naked_cards()
    
    if self.cards_removed_count == self.size[0] * self.size[1]:
      self.display_game_over(screen, res)
    else:
      self.display_score(screen, font, res)

    # Display cards
    for i in range(0, len(self.cards)):
      for j in range(0, len(self.cards[i])):
        self.cards[i][j].display(screen)