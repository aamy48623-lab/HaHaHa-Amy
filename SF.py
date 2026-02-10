import pygame
import random

# 初始化
pygame.init()

# 視窗設定
WIDTH, HEIGHT = 600, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("躲避障礙小車遊戲")

# 顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 玩家設定
player_width, player_height = 50, 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 7

# 障礙物設定
obstacle_width, obstacle_height = 50, 50
obstacle_speed = 5
obstacles = []

# 遊戲參數
clock = pygame.time.Clock()
score = 0
level = 1
font = pygame.font.SysFont(None, 36)
run = True

# 遊戲迴圈
while run:
    clock.tick(60)  # FPS
    win.fill(WHITE)

    # 事件偵測
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # 玩家移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x - player_speed > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x + player_width + player_speed < WIDTH:
        player_x += player_speed

    # 障礙物生成
    if len(obstacles) < level + 2:  # 關卡越高障礙物越多
        obs_x = random.randint(0, WIDTH - obstacle_width)
        obs_y = -obstacle_height
        obstacles.append([obs_x, obs_y])

    # 障礙物移動
    for obs in obstacles:
        obs[1] += obstacle_speed
        pygame.draw.rect(win, RED, (obs[0], obs[1], obstacle_width, obstacle_height))

    # 玩家畫面
    pygame.draw.rect(win, BLUE, (player_x, player_y, player_width, player_height))

    # 碰撞偵測
    for obs in obstacles:
        if (player_x < obs[0] + obstacle_width and
            player_x + player_width > obs[0] and
            player_y < obs[1] + obstacle_height and
            player_y + player_height > obs[1]):
            run = False  # 遊戲結束

    # 移除已掉出畫面的障礙物
    obstacles = [obs for obs in obstacles if obs[1] < HEIGHT]

    # 分數與關卡
    score += 1
    if score % 500 == 0:  # 每500分升一關
        level += 1
        obstacle_speed += 1

    # 顯示分數與關卡
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    win.blit(score_text, (10, 10))
    win.blit(level_text, (10, 40))

    pygame.display.update()

# 遊戲結束畫面
win.fill(WHITE)
end_text = font.render(f"遊戲結束! 分數: {score}", True, BLACK)
win.blit(end_text, (WIDTH//2 - end_text.get_width()//2, HEIGHT//2))
pygame.display.update()
pygame.time.delay(3000)

pygame.quit()
