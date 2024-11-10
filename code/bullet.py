import pygame
from settings import *
from pygame.math import Vector2 as vector

import pygame
from pygame.math import Vector2 as vector

# Định nghĩa lớp Bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, surf, direction, groups):
        super().__init__(groups)  # Khởi tạo lớp cơ sở (Sprite) và thêm bullet vào nhóm `groups`

        self.image = surf  # Thiết lập hình ảnh của bullet
        if direction.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)    # In ra hình ảnh đạn theo hướng di chuyển
        self.rect = self.image.get_rect(center=pos)  # Tạo hình chữ nhật bao quanh bullet và đặt vị trí trung tâm của nó tại `pos`
        self.z = LAYER['main']  # Xác định layer hiển thị của bullet

        # Movement
        self.direction = direction 
        self.speed = 1200  # Tốc độ di chuyển của bullet
        self.pos = vector(self.rect.center)  # Lưu trữ vị trí của bullet dưới dạng vector để tính toán di chuyển

        # Destroy
        self.start_time = pygame.time.get_ticks()

    def update(self, dt):
        # Cập nhật vị trí của bullet dựa trên hướng di chuyển, tốc độ và thời gian giữa các khung hình
        self.pos += self.direction * self.speed * dt  # Thay đổi vị trí dựa trên hướng và tốc độ
        self.rect.center = (round(self.pos.x), round(self.pos.y))  # Cập nhật vị trí trung tâm của `rect` với giá trị x và y mới được làm tròn

        if pygame.time.get_ticks() - self.start_time > 1000:       # Xóa đạn sau 1s
            self.kill()
