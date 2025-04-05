import pygame

# Khởi tạo Pygame
pygame.init()

# Cài đặt màn hình
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Animation")

# Màu sắc
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Thiết lập biến
x = 100  # Vị trí ban đầu
y = HEIGHT // 2
radius = 30  # Bán kính hình tròn
speed = 5  # Tốc độ di chuyển

direction = 1  # 1 là đi sang phải, -1 là đi sang trái

# Vòng lặp chính
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)  # Xóa màn hình
    
    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Cập nhật vị trí
    x += speed * direction
    
    # Đảo ngược hướng khi chạm mép màn hình
    if x + radius >= WIDTH or x - radius <= 0:
        direction *= -1
    
    # Vẽ hình tròn
    pygame.draw.circle(screen, RED, (x, y), radius)
    
    pygame.display.flip()  # Cập nhật màn hình
    clock.tick(60)  # Giữ tốc độ khung hình ổn định

pygame.quit()
