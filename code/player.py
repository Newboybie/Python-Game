import pygame                      # Nhập thư viện Pygame để phát triển các tính năng của game
from settings import *             # Nhập các thiết lập từ file settings, như thông tin về kích thước màn hình hoặc các thông số cấu hình khác

# Định nghĩa lớp Player, kế thừa từ pygame.sprite.Sprite để quản lý nhân vật người chơi
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)    # Khởi tạo lớp cơ sở (Sprite) và thêm player vào nhóm sprite `group` được truyền vào

        self.image = pygame.Surface((40, 80))  # Tạo một bề mặt `Surface` cho nhân vật với kích thước (40x80) pixel
        self.image.fill('yellow')              # Đổ màu vàng cho bề mặt `image`, tạo màu sắc cho nhân vật

        self.rect = self.image.get_rect(topleft=pos)  # Tạo hình chữ nhật (rect) bao quanh `image` và đặt góc trên cùng bên trái tại vị trí `pos`
