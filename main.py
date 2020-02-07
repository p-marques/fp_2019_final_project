import pygame
import pygame.freetype
import math

from music_player import Music_Player
from main_menu import Main_Menu
from game import Game
from high_scores_manager import High_Scores_Manager

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

  # Start Music Player
  music_player = Music_Player(res)

  # Load Splash Image
  splash_img = pygame.image.load("resources/shuffle.png")

  font = pygame.font.Font("resources/fonts/NotoSans-Regular.ttf", 20)

  # Start High Scores Manager
  hs_manager = High_Scores_Manager()

  game = None
  action = None

  # Game loop, runs forever
  while (True):
    for event in pygame.event.get():
      if (event.type == pygame.QUIT):
        exit()
      if (event.type == pygame.MOUSEBUTTONDOWN):
        pos = pygame.mouse.get_pos()
        music_player.handle_clicks(pos)
        if (not playing):
          action = main_menu.handle_clicks(pos)
          if action == "exit":
            exit()
          elif action == "high_scores":
            hs_manager.toggle_display()
          elif (action != None):
            size = action.split('x')
            game = Game((int(size[0]), int(size[1])), hs_manager, res)
            playing = True
        else:
          playing = game.handle_click(pos)

    screen.fill((0, 0, 20))

    # Music
    if not music_player.is_busy():
      music_player.load_next_song()
      music_player.play()

    music_player.display(screen)

    if (not playing):
      screen.blit(splash_img, (int(res[0] / 2) - int(splash_img_x / 2), int(res[1] / 4) - int(splash_img_y / 2))) # Display Splash Image
      main_menu.display(screen, font)
      hs_manager.display_high_scores(screen, font)
    else:
      game.display(screen, font, res)

    pygame.display.flip()

# RUN
main()