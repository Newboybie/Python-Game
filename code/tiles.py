import pygame                     
from settings import *      
from pygame.math import Vector2 as vector       

# Định nghĩa lớp Tile kế thừa từ pygame.sprite.Sprite, để tạo các ô (tile) trong trò chơi
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z):
        super().__init__(groups)    # Khởi tạo lớp cơ sở (Sprite) và thêm tile vào các nhóm sprite được truyền vào `groups`
        
        self.image = surf           # Gán bề mặt (surface) `surf` cho thuộc tính `image` của tile. `image` đại diện cho hình ảnh của tile
        self.rect = self.image.get_rect(topleft=pos)  
                                     # Tạo hình chữ nhật (rect) bao quanh hình ảnh, đặt vị trí topleft của nó tại `pos`
                                     # `rect` giúp xác định vị trí và cho phép dễ dàng kiểm tra va chạm, vẽ tile lên màn hình
        self.z = z                   # Thuộc tính chứa thứ tự layer

class CollisionTile(Tile):           # Tạo lớp Collisiontile từ Tile để quản lý các tile có thể collison
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups, LAYER['main'])
        self.old_rect = self.rect.copy()        # Biến theo dõi vị trí hiện tại của tile 


class MovingFlatform(CollisionTile):    #Tạo lớp Platfomt từ CollisonTile để quản lý các tile có thể di chuyen
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

        #Moving flatform
        self.direction = vector(0, -1)
        self.speed = 200
        self.pos = vector(self.rect.topleft)

    def update(self, dt):
        self.old_rect = self.rect.copy()     # Biến theo dõi vị trí hiện tại của tile 
        self.pos.y += self.direction.y * self.speed * dt   # Di chuyển lên với speed
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))  # Cập nhật vị trí của `rect` theo tọa độ hiện tại của `pos`, làm tròn giá trị `x` và `y` để đảm bảo vị trí là một số nguyên (pixel).
