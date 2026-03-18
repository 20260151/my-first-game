import pygame
import sys

# 초기화
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My First Pygame")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()
running = True

# 원 위치와 속도
x, y = 400, 300
speed = 10  # 이동 속도
radius = 50  # 원 반지름

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed

    # 화면 밖으로 나가지 않도록 제한
    x = max(radius, min(screen_width - radius, x))
    y = max(radius, min(screen_height - radius, y))

    # 화면 그리기
    screen.fill(WHITE)
    pygame.draw.circle(screen, BLUE, (x, y), radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()