import pygame
import sys
import math

pygame.init()

# 1. 800x600 창 생성
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AABB + Circle + OBB + SAT Demo")

clock = pygame.time.Clock()

# 색상
GRAY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# 글꼴
font = pygame.font.SysFont(None, 30)

# 오브젝트
player = pygame.Rect(100, 100, 80, 80)
target = pygame.Rect(WIDTH//2 - 40, HEIGHT//2 - 40, 80, 80)

speed = 5

# 회전 관련
angle = 0
rotation_speed = 1  # 기본 속도

# -------------------
# OBB 계산 함수
# -------------------
def get_obb_corners(rect, angle):
    cx, cy = rect.center
    w, h = rect.width / 2, rect.height / 2

    corners = [
        (-w, -h),
        (w, -h),
        (w, h),
        (-w, h)
    ]

    rotated = []
    rad = math.radians(angle)

    for x, y in corners:
        rx = x * math.cos(rad) - y * math.sin(rad)
        ry = x * math.sin(rad) + y * math.cos(rad)
        rotated.append((cx + rx, cy + ry))

    return rotated

# -------------------
# SAT 충돌 함수
# -------------------
def dot(a, b):
    return a[0]*b[0] + a[1]*b[1]

def normalize(v):
    length = math.sqrt(v[0]**2 + v[1]**2)
    if length == 0:
        return (0, 0)
    return (v[0]/length, v[1]/length)

def get_axes(points):
    axes = []
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i+1) % len(points)]
        edge = (p2[0] - p1[0], p2[1] - p1[1])
        normal = (-edge[1], edge[0])
        axes.append(normalize(normal))
    return axes

def project(points, axis):
    min_p = dot(points[0], axis)
    max_p = min_p
    for p in points[1:]:
        proj = dot(p, axis)
        min_p = min(min_p, proj)
        max_p = max(max_p, proj)
    return min_p, max_p

def sat_collision(poly1, poly2):
    axes = get_axes(poly1) + get_axes(poly2)
    for axis in axes:
        min1, max1 = project(poly1, axis)
        min2, max2 = project(poly2, axis)
        if max1 < min2 or max2 < min1:
            return False
    return True

# -------------------
# 메인 루프
# -------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # 이동
    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed
    if keys[pygame.K_UP]:
        player.y -= speed
    if keys[pygame.K_DOWN]:
        player.y += speed

    # Z 키로 회전 속도 증가
    if keys[pygame.K_z]:
        current_speed = rotation_speed * 3
    else:
        current_speed = rotation_speed

    angle += current_speed

    # 중심
    player_center = player.center
    target_center = target.center

    # 반지름
    player_radius = player.width // 2
    target_radius = target.width // 2

    # -------------------
    # 충돌 계산
    # -------------------

    # 원형 충돌
    dx = player_center[0] - target_center[0]
    dy = player_center[1] - target_center[1]
    distance = math.sqrt(dx**2 + dy**2)
    circle_collision = distance < (player_radius + target_radius)

    # AABB 충돌
    aabb_collision = player.colliderect(target)

    # OBB 충돌
    player_obb = get_obb_corners(player, 0)  # player는 회전 없음
    target_obb = get_obb_corners(target, angle)
    obb_collision = sat_collision(player_obb, target_obb)

    # -------------------
    # 배경 색 결정 (OBB > Circle > 기본)
    # -------------------
    if obb_collision:
        screen.fill(RED)
    elif circle_collision:
        screen.fill(YELLOW)
    else:
        screen.fill(WHITE)

    # -------------------
    # 오브젝트 표시
    # -------------------
    pygame.draw.rect(screen, GRAY, player)
    pygame.draw.rect(screen, GRAY, target)

    # AABB
    pygame.draw.rect(screen, RED, player, 2)
    pygame.draw.rect(screen, RED, target, 2)

    # 원형
    pygame.draw.circle(screen, BLUE, player_center, player_radius, 2)
    pygame.draw.circle(screen, BLUE, target_center, target_radius, 2)

    # OBB
    pygame.draw.polygon(screen, GREEN, target_obb, 2)
    pygame.draw.polygon(screen, GREEN, player_obb, 2)

    # -------------------
    # 충돌 상태 표시
    # -------------------
    texts = []
    if circle_collision:
        texts.append("Circle: HIT")
    else:
        texts.append("Circle: ---")

    if aabb_collision:
        texts.append("AABB: HIT")
    else:
        texts.append("AABB: ---")

    if obb_collision:
        texts.append("OBB: HIT")
    else:
        texts.append("OBB: ---")

    # 왼쪽 상단에 순서대로 표시
    for i, t in enumerate(texts):
        img = font.render(t, True, BLACK)
        screen.blit(img, (10, 10 + i*30))

    pygame.display.flip()
    clock.tick(60)