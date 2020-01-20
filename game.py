class Game:
  score = 0
  cards = []

  def __init__(self, size_txt):
    size_l = size_txt.split('x')
    self.size = (int(size_l[0]), int(size_l[1]))


  def display(self, screen, font):
    font.render_to(screen, (10, 10), str(self.score), (160, 160, 0))