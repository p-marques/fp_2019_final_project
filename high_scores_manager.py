import requests

from high_score import High_Score

class High_Scores_Manager:
    base_url = "https://pmark.pt/api/shufflehighscores"
    high_scores = None
    display = False

    def __init__(self):
        pass

    def get_high_scores(self):
        r = requests.get(self.base_url, verify=False)

        self.high_scores = []
        if r.status_code != 200:
            return

        data = r.json()
        for hs in data:
            s = High_Score()
            s.name = hs['name']
            s.gameMode = hs['gameMode']
            s.gameModeLiteral = hs['gameModeLiteral']
            s.score = hs['score']
            self.high_scores.append(s)

        self.high_scores.sort(key = lambda x : x.score, reverse = True)

    def post_high_score(self, score, game_size):
        headers = {'Content-type':'application/json', 'Accept':'application/json'}
        game_modes = ["4x3", "4x4", "5x4", "6x5", "6x6"]

        mode = game_modes.index(f"{game_size[0]}x{game_size[1]}")
        score *= game_size[0] * game_size[1]

        hs = {
            "name": "shuffle_god",
            "gameMode": mode,
            "score": score
        }

        r = requests.post(self.base_url, json=hs, verify=False, headers=headers)

        if r.status_code != 201:
            print(r.json())
            return False

        self.get_high_scores()
        return True

    # Checks if player is in top 10
    def is_player_in_top_10(self, game_size, score):
        if self.high_scores == None:
            self.get_high_scores()
        
        if len(self.high_scores) < 10:
            return True

        score *= game_size[0] * game_size[1]
        for hs in self.high_scores:
            if score  > hs.score:
                return True

        return False

    def toggle_display(self):
        self.display = not self.display

    def display_text(self, screen, font, text, y_multiplier):
        text_surface = font.render(text, True, (160, 160, 0))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (10, 50 + text_rect.bottom * y_multiplier)
        screen.blit(text_surface, text_rect)

    def display_high_scores(self, screen, font):
        if not self.display:
            return

        if self.high_scores == None:
            self.get_high_scores()

        if len(self.high_scores) == 0:
            self.display_text(screen, font, "No high scores...", 1)

        for i in range(0, len(self.high_scores)):
            if i == 9:
                break

            self.display_text(screen, font, f"{i + 1} - {self.high_scores[i].name} - {self.high_scores[i].score}", i + 1)


