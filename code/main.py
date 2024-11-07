import pygame, sys                   # Nhập thư viện Pygame để phát triển game và sys để xử lý thoát chương trình
from settings import *               # Nhập các thiết lập từ file settings, như WINDOW_WIDTH và WINDOW_HEIGHT
from pytmx.util_pygame import load_pygame  # Nhập hàm load_pygame để tải bản đồ TMX
from tiles import Tile               # Nhập lớp Tile để tạo các ô (tile) trong game
from player import Player            # Nhập lớp Player

# Định nghĩa lớp Main để quản lý toàn bộ trò chơi
class Main:
    def __init__(self):
        pygame.init()                # Khởi tạo Pygame, cần thiết trước khi sử dụng bất kỳ thành phần nào của Pygame
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  
                                      # Tạo cửa sổ hiển thị với kích thước lấy từ file settings
        pygame.display.set_caption('Contra')  
                                      # Đặt tiêu đề cửa sổ trò chơi là "Contra"
        self.clock = pygame.time.Clock()  
                                      # Thiết lập đồng hồ để điều khiển tốc độ khung hình cho trò chơi

        self.all_sprites = pygame.sprite.Group()  # Tạo nhóm `all_sprites` để quản lý tất cả các sprite trong trò chơi
        self.setup()                  # Thiết lập trò chơi bằng cách tải bản đồ và tạo các tile

    def setup(self):
        tmx_map = load_pygame('D:/Python-Game/data/map.tmx')  # Tải bản đồ TMX từ đường dẫn chỉ định
        for x, y, sur in tmx_map.get_layer_by_name('Level').tiles():
            Tile((x * 0, y * 0), sur, self.all_sprites)  # Tạo tile tại (x * 16, y * 16) với hình ảnh `sur` và thêm vào `all_sprites`
        Player((100, 200), self.all_sprites)   #In ra player tại (100, 200)

    def run(self):                   # Phương thức run để chạy vòng lặp chính của trò chơi
        while True:                  # Vòng lặp chính của trò chơi, chạy liên tục đến khi người chơi thoát
            for event in pygame.event.get():  
                                      # Lấy tất cả sự kiện trong hàng đợi sự kiện của Pygame
                if event.type == pygame.QUIT:  
                                      # Nếu người chơi nhấn nút đóng cửa sổ
                    pygame.quit()     # Thoát khỏi Pygame
                    sys.exit()        # Thoát chương trình

            dt = self.clock.tick() / 1000  # Điều chỉnh tốc độ khung hình và tính thời gian giữa các khung hình, đổi sang giây
            self.display_surface.fill((249, 131, 103))  # Đổ màu nền cam nhạt cho màn hình

            self.all_sprites.update(dt)                 # Cập nhật trạng thái của tất cả sprite trong nhóm `all_sprites`
            self.all_sprites.draw(self.display_surface) # Vẽ tất cả sprite lên màn hình `display_surface`
            pygame.display.update()                     # Cập nhật màn hình với các thay đổi đã thực hiện

# Điểm khởi đầu của chương trình
if __name__ == '__main__':          
    main = Main()                    # Tạo một đối tượng của lớp Main
    main.run()                       # Gọi phương thức run để bắt đầu vòng lặp chính của trò chơi
