import pygame, sys                   
from settings import *               # Nhập các thiết lập từ file settings, như WINDOW_WIDTH và WINDOW_HEIGHT
from pytmx.util_pygame import load_pygame  # Nhập hàm load_pygame để tải bản đồ TMX
from tiles import Tile, CollisionTile, MovingFlatform               # Nhập lớp Tile để tạo các ô (tile) trong game
from player import Player            # Nhập lớp Player
from pygame.math import Vector2 as vector 

# Định nghĩa lớp AllSprites kế thừa từ pygame.sprite.Group, dùng để quản lý các sprite và vẽ chúng lên màn hình
class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()  # Lấy bề mặt hiển thị hiện tại của Pygame
        self.offset = vector()                              # Khởi tạo vector để điều chỉnh vị trí hiển thị của các sprite

    # Phương thức để vẽ các sprite với một khoảng bù (offset) để tạo hiệu ứng theo dõi
    def custom_draw(self, player):
        # Tính toán offset dựa trên vị trí của player
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        # Vẽ từng sprite với offset
        for sprite in sorted(self.sprites(), key= lambda sprite: sprite.z): # In ra từng sprite ứng với thứ tự của layer chứa sprite
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)  # Lấy rect cho vị trí offset của sprite
            offset_rect.center -= self.offset                               # Trừ offset để điều chỉnh vị trí
            self.display_surface.blit(sprite.image, offset_rect)            # Vẽ sprite lên màn hình


# Định nghĩa lớp Main để quản lý toàn bộ trò chơi
class Main:
    def __init__(self): 
        pygame.init()                # Khởi tạo Pygame
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  
                                      
        pygame.display.set_caption('Contra')  
                                      
        self.clock = pygame.time.Clock()  
                                      # Thiết lập đồng hồ để điều khiển tốc độ khung hình cho trò chơi

        self.all_sprites = AllSprites()  # Tạo nhóm `all_sprites` để quản lý tất cả các sprite trong trò chơi
        self.collision_sprites = pygame.sprite.Group() #Tạo nhóm `collision tile` để quản lý các tile có thể collision
        self.platform_sprites = pygame.sprite.Group()  #Tạo nhóm `platform` để quản lý các tile có thể di chuyen
        self.setup()                  # Thiết lập trò chơi bằng cách tải bản đồ và tạo các tile

    def setup(self):
        tmx_map = load_pygame('D:/Python-Game/data/map.tmx')  # Tải bản đồ TMX

        #Main Layer
        for x, y, surf in tmx_map.get_layer_by_name('Level').tiles():
            CollisionTile((x * 64, y * 64), surf, [self.all_sprites,self.collision_sprites])  # Tạo collision tile có diện tích (x * 64, y * 64) 

        #Layer
        for layer in ['BG', 'BG Detail', 'FG Detail Bottom', 'FG Detail Top']:  #In ra tất cả các layer trong map
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Tile((x * 64, y * 64), surf, self.all_sprites, LAYER[layer]) 
            
        
        #Objects
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, 'D:/Python-Game/graphics/player', self.collision_sprites)   #In ra player tại vị trí xuất phát(Entities có name = player)

        #Flatforms
        for obj in tmx_map.get_layer_by_name('Platforms'):
            if obj.name == 'Platform':
                MovingFlatform((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.platform_sprites])
            else:
                pass

    def run(self):                   
        while True:                  # Vòng lặp chính của trò chơi, chạy liên tục đến khi người chơi thoát
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:  
                    pygame.quit()     
                    sys.exit()        # Thoát chương trình

            dt = self.clock.tick() / 1000  # Điều chỉnh tốc độ khung hình và tính thời gian giữa các khung hình, đổi sang giây
            self.display_surface.fill((249, 131, 103))  # Đổ màu nền cho màn hình

            self.all_sprites.update(dt)                 # Cập nhật trạng thái của tất cả sprite trong nhóm `all_sprites`
            #self.all_sprites.draw(self.display_surface) # Vẽ tất cả sprite lên màn hình `display_surface`
            self.all_sprites.custom_draw(self.player)   # Vẽ tất cả sprite bằng custom_draw với vị trí của người chơi làm trung tâm
            pygame.display.update()                     # Cập nhật màn hình với các thay đổi đã thực hiện

# Điểm khởi đầu của chương trình
if __name__ == '__main__':          
    main = Main()                    
    main.run()                       
