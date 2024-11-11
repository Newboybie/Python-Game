import pygame
from pygame.math import Vector2 as vector
from settings import *
from entity import Entity

class Enemy(Entity):
    def __init__(self, pos, path, groups, shoot, player, collision_sprites):
        super().__init__(pos, path, groups, shoot)
        self.player = player
        
        for sprite in collision_sprites.sprites():           # Đảm bảo kẻ địch xuất hiện đúng vị trí
            if sprite.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = sprite.rect.top

    def get_status(self):                                    # Kẻ địch sẽ luôn quay mặt về hướng người chơi
        if self.player.rect.centerx < self.rect.centerx:
            self.status = 'left'
        else:
            self.status = 'right'

    def update(self,dt):
        self.get_status()
        self.animate(dt)
