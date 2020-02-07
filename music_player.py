import pygame
from os import walk
from math import ceil as round_up

from button import Button

class Music_Player:
    path = "resources/music/"
    paused_by_player = False
    music_files = []
    current_music_index = -1
    buttons = []
    font = None

    def __init__(self, res):
        self.check_music_files()
        self.create_player_buttons(res)
        self.set_volume(0.2) # Default volume -> 20%
        
        # print(self.get_volume()) # Used for testing. Even thou I set the volume above to exactly 0.2, the actually value returned is 0.1953125

    def check_music_files(self):
        # loads .ogg file names. Maximum of 10
        for (_, _, files) in walk(self.path):
            for f in files:
                if len(self.music_files) == 10: break
                if f.endswith(".ogg"):
                    self.music_files.append(f)
            break

    # Returns success of load
    def load_next_song(self):
        if len(self.music_files) == 0:
            return False

        #pygame.mixer.music.unload()

        if self.current_music_index < len(self.music_files) - 1:
            self.current_music_index += 1
        else:
            self.current_music_index = 0

        pygame.mixer.music.load(f"{self.path}{self.music_files[self.current_music_index]}")

        return True

    # I've chosen to elevate the volume to a 0 to 100 scale for rounding issues.
    # For some reason pygame's value for the current volume always seems a bit off. See comment line on init
    def increase_volume(self, value):
        current = round_up(self.get_volume() * 100)
        new_volume = current + value
        if new_volume > 100: 
            new_volume = 100

        pygame.mixer.music.set_volume(new_volume / 100)

    # See comment on increase_volume
    def lower_volume(self, value):
        current = round_up(self.get_volume() * 100)
        new_volume = current - value
        if new_volume < 0: 
            new_volume = 0

        pygame.mixer.music.set_volume(new_volume / 100)

    def set_volume(self, new_volume_lvl):
        pygame.mixer.music.set_volume(new_volume_lvl)

    def toggle_play(self):
        if self.paused_by_player:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

        self.paused_by_player = not self.paused_by_player

    def play(self):
        pygame.mixer.music.play()

    def is_busy(self):
        return pygame.mixer.music.get_busy()

    def create_player_buttons(self, res):
        self.buttons.append(Button((-10, 10), 31, 31, "\u2B89", "sound_up")) # Sound up
        self.buttons.append(Button((-10, 10), 31, 31, "\u2B8B", "sound_down")) # Sound Down
        self.buttons.append(Button((-10, 10), 31, 31, "\u23ED", "next_song")) # Next
        self.buttons.append(Button((-10, 10), 31, 31, "\u23EF", "play_song")) # Play / Pause

        # Sets position of rightmost button and all other are placed to it's left
        self.buttons[0].rect.topright = ( res[0] - 10, 10)
        for i in range(1, len(self.buttons)):
            self.buttons[i].rect.topright = self.buttons[i - 1].rect.topleft

    def handle_btn_action(self, btn_clicked):
        if btn_clicked.action == "sound_up": # Sound up
            self.increase_volume(1) # Increase by 1%
        elif btn_clicked.action == "sound_down": # Sound down
            self.lower_volume(1) # Decrease by 1%
        elif btn_clicked.action == "next_song": # Next
            self.load_next_song()
            self.play()
        elif btn_clicked.action == "play_song": # Play / Pause
            self.toggle_play()

    def handle_clicks(self, pos):
        for btn in self.buttons:
            if btn.player_clicked_btn(pos):
                self.handle_btn_action(btn)

    # Between 0.0 and 1.0
    def get_volume(self):
        return pygame.mixer.music.get_volume()

    def display_volume(self, screen):
        txt = f"{str(round_up(self.get_volume() * 100))}%"
        text_surface = self.font.render(txt, True, self.buttons[0].color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = self.buttons[0].rect.left
        text_rect.centery = self.buttons[0].rect.bottom + 10
        screen.blit(text_surface, text_rect)

    def display(self, screen):
        if self.font == None: 
            self.font = pygame.font.Font("resources/fonts/seguisym.ttf", 16) # Font loaded once

        for i in range(0, len(self.buttons)):
            self.buttons[i].display(screen, self.font)

        self.display_volume(screen)