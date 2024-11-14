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
        
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        # Cập nhật vị trí của bullet dựa trên hướng di chuyển, tốc độ và thời gian giữa các khung hình
        self.pos += self.direction * self.speed * dt  # Thay đổi vị trí dựa trên hướng và tốc độ
        self.rect.center = (round(self.pos.x), round(self.pos.y))  # Cập nhật vị trí trung tâm của `rect` với giá trị x và y mới được làm tròn

        if pygame.time.get_ticks() - self.start_time > 1000:       # Xóa đạn sau 1s
            self.kill()

class FireAnimation(pygame.sprite.Sprite):
    def __init__(self, entity, surf_list, direction, groups):
        super().__init__(groups)                    
        self.entity = entity                         # Đối tượng (entity) mà animation này liên kết

        self.frames = surf_list                      # Danh sách các frame (bề mặt hình ảnh) cho animation
        if direction.x < 0:                         
            # Lật các frame trong `frames` theo chiều ngang để phù hợp với hướng bắn
            self.frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]
        # Image
        self.frame_index = 0                        
        self.image = self.frames[self.frame_index]   # Lấy hình ảnh của frame đầu tiên trong danh sách `frames`
        
        # Offset
        x_offset = 40 if direction.x > 0 else -40
        y_offset = 15 if entity.duck else 3
        self.offset = vector(x_offset, y_offset)

        # Position
        self.rect = self.image.get_rect(center=self.entity.rect.center + self.offset)   # Đặt `rect` (hình chữ nhật) của `image` tại vị trí `center` của `entity`
        self.z = LAYER['main']                       # Xác định layer của animation (cùng layer `main` của entity)

    def animate(self, dt):                           # Hàm tạo animation shooting
        self.frame_index += 15 * dt
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def move(self):                                  # Hàm đảm bảo animation đi liền với người chơi
        self.rect.center = self.entity.rect.center + self.offset
    
    def update(self, dt):
        self.animate(dt)
        self.move()
