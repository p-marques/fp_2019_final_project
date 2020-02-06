from button import Button

class Main_Menu:
  buttons = []
  buttons_width = 200
  buttons_height = 48

  def __init__(self, screen_res):
    self.create_buttons(screen_res)

  def create_buttons(self, screen_res):
    btns_txt = ["4x3", "4x4", "5x4", "6x5", "6x6", "EXIT"]
    pos_x = (screen_res[0] / 2) - (self.buttons_width / 2)
    pos_y = screen_res[1] / 2

    for i in range(0, len(btns_txt)):
      self.add_buttons((pos_x, pos_y + self.buttons_height * i + 10 * i), btns_txt[i])

  def add_buttons(self, pos, text):
    self.buttons.append(Button(pos, self.buttons_width, self.buttons_height, text))

  def handle_clicks(self, mouse_pos):
    for btn in self.buttons:
      if btn.player_clicked_btn(mouse_pos):
        return btn.text

  def display(self, screen, font):
    for i in range(0, len(self.buttons)):
      self.buttons[i].display(screen, font)