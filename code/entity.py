from math import sin
import os
import pygame
from pygame.math import Vector2 as vector
from settings import *


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, path, groups, shoot):
        super().__init__(groups)

        # Image setup
        self.import_assets(path)               # Lấy asset cho entity tại path(đường dẫn)
        self.frame_index = 0
        self.status = 'right'

        self.image = self.animations[self.status][self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)           
        self.rect = self.image.get_rect(topleft=pos)  # Tạo hình chữ nhật (rect) bao quanh `image` và đặt góc trên cùng bên trái tại vị trí `pos`
        self.old_rect = self.rect.copy()        # Lưu trữ vị trí hiện tại của player 
        
        self.z = LAYER['main']                 # Layer nhân vật sẽ tồn tại

        # Moving setup
        self.direction = vector()              # Vector2 để quản lý hướng di chuyển của nhân vật
        self.pos = vector(self.rect.topleft)   # Sao chép vị trí ban đầu của `rect` vào `pos` dưới dạng vector để xử lý di chuyển chính xác hơn      
        self.speed = 400                       # Đặt tốc độ di chuyển của nhân vật (400 pixel mỗi giây

        # Shooting setup
        self.shoot = shoot
        self.can_shoot = True    
        self.shoot_time = None           # Thời gian lần bắn cuối, ban đầu là None (chưa bắn)
        self.cooldown = 200              # Thời gian chờ (cooldown) giữa hai lần bắn, tính bằng milliseconds (200 ms)
        self.duck = False

        # Health
        self.health = 3

        # Audio
        self.hit_sound = pygame.mixer.Sound('D:/Python-Game/audio/hit.mp3')
        self.hit_sound.set_volume(0.2)
        self.shoot_sound = pygame.mixer.Sound('D:/Python-Game/audio/shoot.mp3')
        self.shoot_sound.set_volume(0.4)

    def animate(self, dt):                      # Hàm tạo animate
        self.frame_index += 7 * dt              # Tốc độ lặp animation            
        current_animations = self.animations[self.status]   
        if self.frame_index >= len(current_animations):   # Lặp lại từ đầu nếu đã tới frame cuối
            self.frame_index = 0
        
        self.image = current_animations[int(self.frame_index)]  # Lấy image của frame hiện tại
        self.mask = pygame.mask.from_surface(self.image)

    def blink(self):  # Nháy trắng
        mask = pygame.mask.from_surface(self.image)
        white_surf = mask.to_surface()
        white_surf.set_colorkey((0, 0, 0))
        self.image = white_surf

    def shoot_timer(self):
        if not self.can_shoot:                  # Nếu player chưa thể bắn (can_shoot là False)
            current_time = pygame.time.get_ticks()  # Lấy thời gian hiện tại (tính từ khi chương trình bắt đầu chạy)
            if current_time - self.shoot_time > self.cooldown:   # Nếu thời gian chờ đã kết thúc
                self.can_shoot = True           # Cho phép bắn (can_shoot là True)
  
    def damage(self):                           # Hàm nhận sát thương khi bị bắn trúng
        self.blink()
        self.hit_sound.play()
        self.health -= 1

    def check_death(self):                      # Hàm tiêu diệt khi hết máu
        if self.health <= 0:
            self.kill()

    def import_assets(self, path):
        self.animations = {}  # Tạo một từ điển trống để lưu các animation theo từng tên thư mục.
    
        # Duyệt qua tất cả các thư mục con và tệp trong thư mục 'path' bằng os.walk
        for index, (root, dirs, files) in enumerate(os.walk(path)):
            # Nếu là vòng lặp đầu tiên (index == 0), ta đang ở thư mục gốc
            if index == 0:
                # Thêm mỗi thư mục con trong 'dirs' làm một khóa trong từ điển animations và khởi tạo một danh sách trống để chứa các bề mặt (Surface) tương ứng
                for name in dirs:
                    self.animations[name] = []
            else:
                # Lấy tên thư mục hiện tại từ biến root (tên thư mục chứa các tệp ảnh)
                key = os.path.basename(root)  
            
                # Sắp xếp danh sách các tệp ảnh trong thư mục hiện tại theo thứ tự số nếu có
                # (Dùng split('.')[0] để lấy phần trước dấu chấm)
                sorted_files = sorted(files, key=lambda string: int(string.split('.')[0]))
            
                # Duyệt qua từng tệp đã được sắp xếp trong thư mục hiện tại
                for file_name in sorted_files:
                    # Tạo đường dẫn đầy đủ đến tệp bằng os.path.join, sau đó chuẩn hóa dấu gạch chéo
                    full_path = os.path.join(root, file_name).replace('\\', '/')
                
                    # Tải tệp ảnh lên dưới dạng bề mặt (Surface) của pygame, sử dụng convert_alpha để hỗ trợ ảnh trong suốt
                    surf = pygame.image.load(full_path).convert_alpha()
                
                    # Thêm Surface đã tải vào danh sách của thư mục tương ứng trong self.animations
                    self.animations[key].append(surf)


