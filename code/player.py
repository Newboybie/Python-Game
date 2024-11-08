import pygame                      
from settings import *             
from pygame.math import Vector2 as vector 

# Định nghĩa lớp Player
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)    # Khởi tạo lớp cơ sở (Sprite) và thêm player vào nhóm sprite `group` được truyền vào

        self.image = pygame.Surface((40, 80))  # Tạo một bề mặt `Surface` cho nhân vật với kích thước (40x80) pixel
        self.image.fill('yellow')              # Đổ màu vàng cho bề mặt `image`, tạo màu sắc cho nhân vật

        self.rect = self.image.get_rect(topleft=pos)  # Tạo hình chữ nhật (rect) bao quanh `image` và đặt góc trên cùng bên trái tại vị trí `pos`

        self.z = LAYER['main']                 # Layer nhân vật sẽ tồn tại
        self.direction = vector()              # Tạo một vector để quản lý hướng di chuyển của nhân vật
        self.pos = vector(self.rect.topleft)   # Sao chép vị trí ban đầu của `rect` vào `pos` dưới dạng vector để xử lý di chuyển chính xác hơn
        self.speed = 400                       # Đặt tốc độ di chuyển của nhân vật (400 pixel mỗi giây)

    def input(self):
        # Nhận input người dùng để xác định hướng di chuyển
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:                  
            self.direction.x = 1
        elif keys[pygame.K_a]:                 
            self.direction.x = -1
        else:
            self.direction.x = 0              
        if keys[pygame.K_w]:                   
            self.direction.y = -1
        elif keys[pygame.K_s]:                 
            self.direction.y = 1
        else:
            self.direction.y = 0               

    def move(self, dt):
        # Tính toán vị trí mới dựa trên hướng di chuyển, tốc độ và thời gian giữa các khung hình
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)        # Cập nhật vị trí x của `rect` với giá trị x mới đã được làm tròn
        
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)        # Cập nhật vị trí y của `rect` với giá trị y mới đã được làm tròn

    def update(self, dt):
        self.input()                           
        self.move(dt)                         
