import pygame
from pygame.math import Vector2 as vector
from settings import *
from entity import Entity

class Enemy(Entity):
    def __init__(self, pos, path, groups, shoot, player, collision_sprites):
        super().__init__(pos, path, groups, shoot)
        self.player = player
        self.cooldown = 1000                                 # Giảm tốc độ bắn của kẻ địch
        
        for sprite in collision_sprites.sprites():           # Đảm bảo kẻ địch xuất hiện đúng vị trí
            if sprite.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = sprite.rect.top

    def get_status(self):                                    # Kẻ địch sẽ luôn quay mặt về hướng người chơi
        if self.player.rect.centerx < self.rect.centerx:
            self.status = 'left'
        else:
            self.status = 'right'
        
    def check_fire(self):                                     # Hàm kiểm soát khả năng shooting của kẻ địch
        enemy_pos = vector(self.rect.center)
        player_pos = vector(self.player.rect.center)

        distance = (player_pos - enemy_pos).magnitude()
        same_y = True if self.rect.top - 20 < player_pos.y < self.rect.bottom + 20 else False     # Kiểm tra vị trí người chơi có nằm trong tầm bắn không

        if distance < 600 and same_y and self.can_shoot:                                           
            bullet_direction = vector(1, 0) if self.status == 'right' else vector(-1, 0)
            y_offset = vector(0, -15)
            pos = self.rect.center + bullet_direction * 80
            self.shoot(pos + y_offset, bullet_direction, self)
            self.shoot_sound.play()

            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def update(self,dt):
        self.get_status()
        self.animate(dt)

        self.shoot_timer()
        self.check_fire()

        # Death
        self.check_death()
