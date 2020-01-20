import pygame
import random
import numpy

from button import Button
from card import Card

class Game:
  tick = 0
  naked_cards = []
  symbols = ["square", "triangle", "circle"]

  def __init__(self, size, screen=(1280, 720)):
    self.size = size
    self.exit_btn = Button((10, screen[1] - 50), 140, 40, "EXIT GAME")
    self.board_size = self.get_board_size(screen)
    self.card_size = self.get_cards_size()
    self.cards = self.get_cards(screen)
    self.score = 0
    self.picks_since_last_correct = 0

  def get_board_size(self, screen):
    return (screen[0] / 2, screen[1] - 50)

  def get_cards_size(self):
    return ( ((self.board_size[0] / self.size[0])), ((self.board_size[1] / self.size[1])) )

  def get_cards(self, screen):
    r = 0
    cards = []
    spacing = 4
    counter = 0

    color = self.get_rand_color()
    symbol = self.get_rand_symbol()

    for i in range(0, self.size[1]):
      row = []
      for j in range(0, self.size[0]):
        if (counter == 2):
          color = self.get_rand_color()
          symbol = self.get_rand_symbol()
          counter = 0

        pos_x = (screen[0] / 2) - (self.board_size[0] / 2) + (self.card_size[0] * j) + (spacing * j) - (spacing / self.card_size[0])
        pos_y = (screen[1] / 2) - (self.board_size[1] / 2) + (self.card_size[1] * i) + (spacing * i) - (spacing / self.card_size[1])
        c = Card(r + 1, pos_x, pos_y, self.card_size[0], self.card_size[1], symbol, color)
        row.append(c)
        counter += 1
        r += 1

      cards.append(row)

    return cards

  def get_rand_color(self):
    return (random.randint(40, 255), random.randint(40, 255), random.randint(40, 255))

  def get_rand_symbol(self):
    return random.randint(0, 2)

  # Returns answer to 'keep playing?'
  def handle_click(self, pos):
    if self.exit_btn.player_clicked_btn(pos):
      return False

    for i in range(0, len(self.cards)):
      for j in range(0, len(self.cards[i])):
        if len(self.naked_cards) < 2 and self.cards[i][j].handle_click(pos):
          self.naked_cards.append(self.cards[i][j])
          if len(self.naked_cards) == 2:
            self.tick = pygame.time.get_ticks()

    return True

  def get_card_index(self, id):
    for i in range(0, len(self.cards)):
      for j in range(0, len(self.cards[i])):
        if self.cards[i][j].id == id:
          return (i, j)

  def remove_naked_cards(self):
    for card in self.naked_cards:
      i = self.get_card_index(card.id)
      self.cards[i[0]].pop(i[1])

  def update_score(self, score_to_add):
    if score_to_add < 0 and self.score - score_to_add < 0:
      self.score = 0
      return

    self.score += score_to_add

  def compare_cards(self):
    if self.naked_cards[0].symbol == self.naked_cards[1].symbol and self.naked_cards[0].color == self.naked_cards[1].color:
      self.picks_since_last_correct = 0
      return True

    self.picks_since_last_correct += 1
    if self.picks_since_last_correct >= 2:
      self.update_score(-20 * self.picks_since_last_correct)
    return False

  def track_naked_cards(self):
    if pygame.time.get_ticks() - self.tick > 1500:
      if self.compare_cards():
        self.picks_since_last_correct = 0
        self.update_score(100)
        self.remove_naked_cards()

      for card in self.naked_cards:
        card.show_card()

      self.naked_cards = []

  def display(self, screen, font):
    font.render_to(screen, (10, 10), str(self.score), (160, 160, 0))
    self.exit_btn.display(screen, font)

    if len(self.naked_cards) == 2:
      self.track_naked_cards()

    # Display cards
    for i in range(0, len(self.cards)):
      for j in range(0, len(self.cards[i])):
        self.cards[i][j].display(screen)