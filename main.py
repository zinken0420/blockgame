import pygame
import sys
from random import randint

# ゲームの設定
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 150, 20
BALL_RADIUS = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# パドルのクラス
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)

    def update(self):
        self.rect.x = pygame.mouse.get_pos()[0] - PADDLE_WIDTH // 2
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT - 50)

# ボールのクラス
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = 5 * randint(-1, 1)
        self.speed_y = -5

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 0:
            self.speed_y *= -1

    MAX_SPEED_X = 10
    MAX_SPEED_Y = 10

    def increase_speed(self):
        # ボールの速度を増加させる
        if self.speed_x > 0:
            self.speed_x += 1
            self.speed_x = min(self.speed_x, self.MAX_SPEED_X)  # 速度が上限を超えないように制限
        else:
            self.speed_x -= 1
            self.speed_x = max(self.speed_x, -self.MAX_SPEED_X)  # 速度が下限を超えないように制限

        if self.speed_y > 0:
            self.speed_y += 1
            self.speed_y = min(self.speed_y, self.MAX_SPEED_Y)  # 速度が上限を超えないように制限
        else:
            self.speed_y -= 1
            self.speed_y = max(self.speed_y, -self.MAX_SPEED_Y)  # 速度が下限を超えないように制限

# ブロックのクラス
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((75, 25))
        self.image.fill((randint(50, 255), randint(50, 255), randint(50, 255)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# スコアのクラス
class Score(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.image = self.font.render(f"Score: {self.score}", True, WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (10, 10)

    def update(self):
        self.image = self.font.render(f"Score: {self.score}", True, WHITE)

# メイン関数
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ブロック崩し")

    while True:  # ゲームのメインループを無限ループ化
        all_sprites = pygame.sprite.Group()
        bricks = pygame.sprite.Group()
        paddle = Paddle()
        ball = Ball()
        score = Score()

        all_sprites.add(paddle, ball, score)

        # ブロックの配置
        for row in range(5):
            for column in range(10):
                if column != 9:  # 10列目をスキップ
                    brick = Brick(column * 80 + 40, row * 30 + 60)
                    bricks.add(brick)
                    all_sprites.add(brick)

        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    # ループから抜ける代わりにゲームを終了
                    # running = False


            screen.fill(BLACK)
            all_sprites.update()

            # ボールとパドルの衝突
            if pygame.sprite.collide_rect(ball, paddle):
                ball.speed_y *= -1

            # ボールとブロックの衝突
            brick_collision = pygame.sprite.spritecollide(ball, bricks, True)
            if brick_collision:
                ball.speed_y *= -1
                score.score += 1
                ball.increase_speed()  # ボールの速度を増加

            # ブロックがすべて崩れた場合、新しいブロックを生成
                if not bricks:
                    for row in range(5):
                        for column in range(10):
                            if column != 9:
                                brick = Brick(column * 80 + 40, row * 30 + 60)
                                bricks.add(brick)
                                all_sprites.add(brick)

            # ゲームオーバー
            if ball.rect.bottom >= HEIGHT:
                running = False

            all_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(60)


if __name__ == "__main__":
    main()