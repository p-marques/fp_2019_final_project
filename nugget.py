import pygame

# A Nugget is what's hidden behind the card
class Nugget:
    def __init__(self, in_symbol, in_color):
        self.symbol = in_symbol
        self.color = in_color
        self.coordinates = None
        self.border_rect = None

    def generate_coordinates(self, card_rect):
        c = None
        center = card_rect.center
        radius = int(card_rect.width / 2)

        if self.symbol == 0:
            c = self.get_square_coordinates(center, radius)
        elif self.symbol == 1:
            c = self.get_triangle_coordinates(center, radius)
        elif self.symbol == 3:
            c = self.get_kite_coordinates(center, radius)

        self.coordinates = c

    # Creates square out of position and then moves it to center of card.
    # A rect is converted to polygon coordinates to allow for a cleaner display function.
    # This way everything but circles are polygons.
    def get_square_coordinates(self, center, radius):
        square = pygame.Rect((-10, -10), (radius, radius))
        square.center = center

        return square.topleft, square.topright, square.bottomright, square.bottomleft

    def get_triangle_coordinates(self, center, radius):
        half_radius = int(radius / 2)
        return (center[0] - half_radius, center[1] + half_radius), (center[0], center[1] - half_radius), (center[0] + half_radius, center[1] + half_radius)

    def get_kite_coordinates(self, center, radius):
        starter = list(self.get_triangle_coordinates(center, radius)) # Get a tringle to start. -> list, to make it mutable
        kite = [starter[0], starter[1], starter[2], (center[0], center[1] + radius)]

        # Center fix
        for i in range(0, len(kite)):
            kite[i] = kite[i][0], kite[i][1] - int(radius / 4)

        return tuple(kite) # back to tuple for consistency

    def display(self, screen, card_rect):
        if self.border_rect == None: # Border rect is created only once
            self.border_rect = card_rect.copy()
            self.border_rect.width -= 2
            self.border_rect.height -= 2
            self.border_rect.center = card_rect.center

        pygame.draw.rect(screen, self.color, self.border_rect, 2) # border

        if self.symbol == 0 or self.symbol == 1 or self.symbol == 3:  # polygon based
            if self.coordinates == None: # Polygon math happens only once
                self.generate_coordinates(card_rect)

            pygame.draw.polygon(screen, self.color, self.coordinates)
        elif self.symbol == 2:  # circle
            pygame.draw.circle(screen, self.color, card_rect.center, int(card_rect.width / 4))
            
