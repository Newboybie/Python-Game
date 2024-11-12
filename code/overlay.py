import pygame

class Overlay:
    def __init__(self, player):
        self.player = player
        self.display_surface = pygame.display.get_surface()

    def display(self):
        self.display_surface.blit(self.player.image, (0, 0))