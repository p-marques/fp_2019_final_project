from button import Button
from card import Card

class Game:

  def __init__(self, size, screen=(1280, 720)):
    self.size = size
    self.exit_btn = Button((10, screen[1] - 50), 140, 40, "EXIT GAME")
    self.board_size = self.get_board_size(screen)
    self.card_size = self.get_cards_size()
    self.cards = self.get_cards(screen)
    self.score = 0

  def get_board_size(self, screen):
    return (screen[0] / 2, screen[1] - 50)

  def get_cards_size(self):
    return ( ((self.board_size[0] / self.size[0])), ((self.board_size[1] / self.size[1])) )

  def get_cards(self, screen):
    cards = []
    spacing = 4
    for i in range(0, self.size[1]):
      row = []
      for j in range(0, self.size[0]):
        pos_x = (screen[0] / 2) - (self.board_size[0] / 2) + (self.card_size[0] * j) + (spacing * j) - (spacing / self.card_size[0])
        pos_y = (screen[1] / 2) - (self.board_size[1] / 2) + (self.card_size[1] * i) + (spacing * i) - (spacing / self.card_size[1])
        c = Card(pos_x, pos_y, self.card_size[0], self.card_size[1])
        row.append(c)

      cards.append(row)

    return cards

  # Returns answer to 'keep playing?'
  def handle_click(self, pos):
    if self.exit_btn.player_clicked_btn(pos):
      return False

    for i in range(0, len(self.cards)):
      for j in range(0, len(self.cards[i])):
        self.cards[i][j].handle_click(pos)

    return True

  def display(self, screen, font):
    font.render_to(screen, (10, 10), str(self.score), (160, 160, 0))
    self.exit_btn.display(screen, font)
    for i in range(0, len(self.cards)):
      for j in range(0, len(self.cards[i])):
        self.cards[i][j].display(screen)