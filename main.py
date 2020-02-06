import pygame
import pygame.freetype
import math

from main_menu import Main_Menu
from game import Game

def main():
  playing = False
  splash_img_x = 800
  splash_img_y = 329

  # Initialize pygame, with the default parameters
  pygame.init()
  # Define the size/resolution of our window
  res = (1280, 720)

  # Create a window and a display surface
  # Caption and icon
  pygame.display.set_caption("Shuffle")
  pygame.display.set_icon(pygame.image.load("resources/shuffle_icon.png"))
  screen = pygame.display.set_mode(res)
  
  # Main Menu
  main_menu = Main_Menu(res)

  # Load Splash Image
  splash_img = pygame.image.load("resources/shuffle.png")

  font = pygame.font.Font("resources/NotoSans-Regular.ttf", 20)

  game = None
  action = None

  # Game loop, runs forever
  while (True):
    for event in pygame.event.get():
      if (event.type == pygame.QUIT):
        exit()
      if (event.type == pygame.MOUSEBUTTONDOWN):
        pos = pygame.mouse.get_pos()
        if (not playing):
          action = main_menu.handle_clicks(pos)
          if action == "EXIT":
            exit()
          elif (action != None):
            size = action.split('x')
            game = Game((int(size[0]), int(size[1])), res)
            playing = True
        else:
          playing = game.handle_click(pos)

    screen.fill((0, 0, 20))

    if (not playing):
      screen.blit(splash_img, (int(res[0] / 2) - int(splash_img_x / 2), int(res[1] / 3) - int(splash_img_y / 2))) # Display Splash Image
      main_menu.display(screen, font)
    else:
      game.display(screen, font, res)

    pygame.display.flip()

# RUN
main()