import pygame, sys                   
from settings import *               # Nhập các thiết lập từ file settings, như WINDOW_WIDTH và WINDOW_HEIGHT
from pytmx.util_pygame import load_pygame  # Nhập hàm load_pygame để tải bản đồ TMX
from tiles import Tile, CollisionTile, MovingFlatform               # Nhập lớp Tile để tạo các ô (tile) trong game
from player import Player            # Nhập lớp Player
from bullet import Bullet, FireAnimation
from pygame.math import Vector2 as vector 

# Định nghĩa lớp AllSprites kế thừa từ pygame.sprite.Group, dùng để quản lý các sprite và vẽ chúng lên màn hình
class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()  # Lấy bề mặt hiển thị hiện tại của Pygame
        self.offset = vector()                              # Khởi tạo vector để điều chỉnh vị trí hiển thị của các sprite

        # Sky
        self.fg_sky = pygame.image.load('D:/Python-Game/graphics/sky/fg_sky.png').convert_alpha()
        self.bg_sky = pygame.image.load('D:/Python-Game/graphics/sky/bg_sky.png').convert_alpha()
        tmx_map = load_pygame('D:/Python-Game/data/map.tmx')

        self.sky_width = self.bg_sky.get_width()
        # Lấy chiều rộng của ảnh nền bầu trời xa, dùng để tính toán số lần lặp ảnh bầu trời để phủ hết bề rộng màn hình

        self.padding = WINDOW_WIDTH / 2
        # Thiết lập giá trị đệm, bằng một nửa chiều rộng của cửa sổ trò chơi, để hình ảnh bầu trời lặp lại liền mạch và cân đối

        map_width = tmx_map.tilewidth * tmx_map.width + (2 * self.padding)
        # Tính toán tổng chiều rộng của bản đồ, cộng thêm khoảng đệm ở hai bên để đảm bảo bầu trời phủ kín màn hình khi di chuyển

        self.sky_num = int(map_width // self.sky_width)
        # Tính số lần cần lặp lại ảnh bầu trời để đủ phủ kín bề ngang của bản đồ, làm tròn xuống số nguyên


    # Phương thức để vẽ các sprite với một khoảng bù (offset) để tạo hiệu ứng theo dõi
    def custom_draw(self, player):
        # Tính toán offset dựa trên vị trí của player
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        for x in range(self.sky_num):  # Lặp lại bầu trời đủ số lần để phủ kín chiều rộng bản đồ
            x_pos = -self.padding + (x * self.sky_width)  # Tính toán vị trí x của mỗi lần vẽ bầu trời
            # Vẽ nền trời xa (background sky) với vị trí đã điều chỉnh bằng offset chia 2.5
            self.display_surface.blit(self.bg_sky, (x_pos - self.offset.x / 2.5, 800 - self.offset.y / 2.5))
            # Vẽ nền trời gần (foreground sky) với vị trí đã điều chỉnh bằng offset chia 2
            self.display_surface.blit(self.fg_sky, (x_pos - self.offset.x / 2, 800 - self.offset.y / 2))


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
        self.bullet_sprites = pygame.sprite.Group()    #Tạo nhóm `bullet` để quản lý bullet
        self.setup()                  # Thiết lập trò chơi bằng cách tải bản đồ và tạo các tile

        # Bullet images
        self.bullet_surf = pygame.image.load('D:/Python-Game/graphics/bullet.png').convert_alpha()    # Tạo hình sprites của bullet
        self.fire_surfs = [
            pygame.image.load('D:/Python-Game/graphics/fire/0.png').convert_alpha(),
            pygame.image.load('D:/Python-Game/graphics/fire/1.png').convert_alpha()   ]

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
                self.player = Player((obj.x, obj.y), self.all_sprites, 'D:/Python-Game/graphics/player', self.collision_sprites, self.shoot)   #In ra player tại vị trí xuất phát(Entities có name = player)

        #Flatforms
        self.platform_border_rect = []
        for obj in tmx_map.get_layer_by_name('Platforms'):
            if obj.name == 'Platform':
                MovingFlatform((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.platform_sprites])
            else:
                border_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.platform_border_rect.append(border_rect)

    def bullet_collision(self):                      # Hàm phá hủy đạn khi va chạm vào sprites nhất định
        for obs in self.collision_sprites.sprites():
            pygame.sprite.spritecollide(obs, self.bullet_sprites, True)

    def plarform_collisions(self):                   # Hàm giới hạn khu vực di chuyển của platform
        for platform in self.platform_sprites.sprites():  
            for border in self.platform_border_rect:
                if platform.rect.colliderect(border):
                    if platform.direction.y < 0:     # Nếu platform chạm tới giới hạn trên(border up)
                        platform.rect.top = border.bottom
                        platform.pos.y = platform.rect.y
                        platform.direction.y = 1     # Thay đổi hướng di chuyển
                    else:                            # Nếu platform chạm tới giới hạn dưới(border down)
                        platform.rect.bottom = border.top
                        platform.pos.y = platform.rect.y
                        platform.direction.y = -1    # Thay đổi hướng di chuyển
            if platform.rect.colliderect(self.player.rect) and self.player.rect.centery > platform.rect.centery:  # Nếu đáy của platform chạm vào player, đổi hướng ngay lập tức
                platform.rect.bottom = self.player.rect.top
                platform.pos.y = platform.rect.y
                platform.direction.y = -1

    def shoot(self, pos, direction, entity):         # Hàm quản lý hành động bắn
        Bullet(pos, self.bullet_surf, direction, [self.all_sprites, self.bullet_sprites])
        FireAnimation(entity, self.fire_surfs, direction, self.all_sprites)

    def run(self):                   
        while True:                  # Vòng lặp chính của trò chơi, chạy liên tục đến khi người chơi thoát
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:  
                    pygame.quit()     
                    sys.exit()        # Thoát chương trình

            dt = self.clock.tick() / 1000  # Điều chỉnh tốc độ khung hình và tính thời gian giữa các khung hình, đổi sang giây
            self.display_surface.fill((249, 131, 103))  # Đổ màu nền cho màn hình

            self.plarform_collisions()
            self.all_sprites.update(dt)                 # Cập nhật trạng thái của tất cả sprite trong nhóm `all_sprites`
            self.bullet_collision()                     # Phá hủy đạn đã va chạm
            self.all_sprites.custom_draw(self.player)   # Vẽ tất cả sprite bằng custom_draw với vị trí của người chơi làm trung tâm
            pygame.display.update()                     # Cập nhật màn hình với các thay đổi đã thực hiện

# Điểm khởi đầu của chương trình
if __name__ == '__main__':          
    main = Main()                    
    main.run()                       
