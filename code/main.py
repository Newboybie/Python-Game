import pygame, sys                # Nhập thư viện Pygame để phát triển game và sys để xử lý thoát chương trình
from settings import *             # Nhập các thiết lập từ file settings, như WINDOW_WIDTH và WINDOW_HEIGHT

# Định nghĩa lớp Main để quản lý toàn bộ trò chơi
class Main:
    def __init__(self):
        pygame.init()               # Khởi tạo Pygame, cần thiết trước khi sử dụng bất kỳ thành phần nào của Pygame
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  
                                     # Tạo cửa sổ hiển thị với kích thước lấy từ file settings
        pygame.display.set_caption('Contra')  
                                     # Đặt tiêu đề cửa sổ trò chơi là "Contra"
        self.clock = pygame.time.Clock()  
                                     # Thiết lập đồng hồ để điều khiển tốc độ khung hình cho trò chơi

    def run(self):                  # Phương thức run để chạy vòng lặp chính của trò chơi
        while True:                 # Vòng lặp chính của trò chơi, chạy liên tục đến khi người chơi thoát
            for event in pygame.event.get():  
                                     # Lấy tất cả sự kiện trong hàng đợi sự kiện của Pygame
                if event.type == pygame.QUIT:  
                                     # Nếu người chơi nhấn nút đóng cửa sổ
                    pygame.quit()    # Thoát khỏi Pygame
                    sys.exit()       # Thoát chương trình

            self.display_surface.fill((249, 131, 103))  
                                     # Đổ màu nền cho màn hình hiển thị, ở đây là màu cam nhạt (RGB)
            pygame.display.update()  # Cập nhật màn hình hiển thị với các thay đổi đã thực hiện

            dt = self.clock.tick() / 1000  
                                     # Điều chỉnh tốc độ khung hình và tính thời gian giữa các khung hình, đổi sang giây

# Điểm khởi đầu của chương trình
if __name__ == '__main__':          
    main = Main()                   # Tạo một đối tượng của lớp Main
    main.run()                      # Gọi phương thức run để bắt đầu vòng lặp chính của trò chơi
