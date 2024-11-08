import pygame                       # Nhập thư viện Pygame để sử dụng các tính năng cần thiết cho phát triển game
from settings import *              # Nhập các thiết lập từ file settings

# Định nghĩa lớp Tile kế thừa từ pygame.sprite.Sprite, để tạo các ô (tile) trong trò chơi
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z):
        super().__init__(groups)    # Khởi tạo lớp cơ sở (Sprite) và thêm tile vào các nhóm sprite được truyền vào `groups`
        
        self.image = surf           # Gán bề mặt (surface) `surf` cho thuộc tính `image` của tile. `image` đại diện cho hình ảnh của tile
        self.rect = self.image.get_rect(topleft=pos)  
                                     # Tạo hình chữ nhật (rect) bao quanh hình ảnh, đặt vị trí topleft của nó tại `pos`
                                     # `rect` giúp xác định vị trí và cho phép dễ dàng kiểm tra va chạm, vẽ tile lên màn hình
        self.z = z                   # Thuộc tính chứa thứ tự layer
