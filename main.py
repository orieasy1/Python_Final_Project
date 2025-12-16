import os
import random
import time

import pygame


# --- Config ---
WIDTH, HEIGHT = 800, 400
GROUND_Y = HEIGHT - 60
PLAYER_SIZE = (40, 50)
GRAVITY = 1800  # pixels per second^2
JUMP_VELOCITY = -750
BASE_SPEED = 260  # obstacle/player world speed (px/s)
SPEED_RAMP = 40   # added per 10s of survival
SPAWN_START = 1.2
SPAWN_MIN = 0.45
FPS = 60
HIGHSCORE_FILE = "highscore.txt"


class Player:
    def __init__(self) -> None:
        self.rect = pygame.Rect(120, GROUND_Y - PLAYER_SIZE[1], *PLAYER_SIZE)
        self.vel_y = 0.0
        self.on_ground = True

    def jump(self) -> None:
        if self.on_ground:
            self.vel_y = JUMP_VELOCITY
            self.on_ground = False

    def update(self, dt: float) -> None:
        self.vel_y += GRAVITY * dt
        self.rect.y += int(self.vel_y * dt)
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.vel_y = 0.0
            self.on_ground = True

    def draw(self, surface) -> None:
        pygame.draw.rect(surface, (52, 152, 219), self.rect, border_radius=6)


class Obstacle:
    def __init__(self, x: int, speed: float) -> None:
        width = random.randint(25, 45)
        height = random.randint(30, 65)
        self.rect = pygame.Rect(x, GROUND_Y - height, width, height)
        self.speed = speed

    def update(self, dt: float) -> None:
        self.rect.x -= int(self.speed * dt)

    def draw(self, surface) -> None:
        pygame.draw.rect(surface, (231, 76, 60), self.rect, border_radius=4)


class ObstacleManager:
    def __init__(self) -> None:
        self.obstacles: list[Obstacle] = []
        self.timer = 0.0
        self.next_spawn = SPAWN_START

    def reset(self) -> None:
        self.obstacles.clear()
        self.timer = 0.0
        self.next_spawn = SPAWN_START

    def update(self, dt: float, speed: float) -> None:
        self.timer += dt
        if self.timer >= self.next_spawn:
            self.spawn(speed)
            self.timer = 0.0
            self.next_spawn = max(SPAWN_MIN, self.next_spawn * 0.92)

        for obs in list(self.obstacles):
            obs.speed = speed
            obs.update(dt)
            if obs.rect.right < 0:
                self.obstacles.remove(obs)

    def spawn(self, speed: float) -> None:
        spawn_x = WIDTH + random.randint(0, 60)
        self.obstacles.append(Obstacle(spawn_x, speed))

    def draw(self, surface) -> None:
        for obs in self.obstacles:
            obs.draw(surface)


def load_high_score() -> int:
    try:
        with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f:
            return int(f.read().strip() or 0)
    except (FileNotFoundError, ValueError):
        return 0


def save_high_score(score: int) -> None:
    try:
        with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
            f.write(str(score))
    except OSError:
        pass


def main() -> None:
    pygame.init()
    pygame.display.set_caption("One-Key Endless Runner")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22)
    big_font = pygame.font.SysFont("arial", 32, bold=True)

    player = Player()
    obstacles = ObstacleManager()

    running = True
    playing = False
    start_time = 0.0
    elapsed = 0.0
    high_score = load_high_score()
    last_score = 0

    while running:
        dt_ms = clock.tick(FPS)
        dt = dt_ms / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not playing:
                    # Start or restart
                    playing = True
                    start_time = time.time()
                    elapsed = 0.0
                    last_score = 0
                    player = Player()
                    obstacles.reset()
                player.jump()

        if playing:
            elapsed = time.time() - start_time
            speed = BASE_SPEED + SPEED_RAMP * (elapsed / 10.0)
            player.update(dt)
            obstacles.update(dt, speed)

            # Collision detection
            for obs in obstacles.obstacles:
                if player.rect.colliderect(obs.rect):
                    playing = False
                    last_score = int(elapsed * 10)
                    if last_score > high_score:
                        high_score = last_score
                        save_high_score(high_score)
                    break
        else:
            speed = 0

        # Draw
        screen.fill((245, 245, 245))
        pygame.draw.rect(screen, (40, 40, 40), (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))

        player.draw(screen)
        obstacles.draw(screen)

        score_text = font.render(f"Score: {int(elapsed*10):05d}", True, (33, 33, 33))
        hi_text = font.render(f"Best: {high_score:05d}", True, (80, 80, 80))
        speed_text = font.render(f"Speed: {int(speed)}", True, (100, 100, 100))
        screen.blit(score_text, (20, 20))
        screen.blit(hi_text, (20, 50))
        screen.blit(speed_text, (20, 80))

        if not playing:
            title = big_font.render("Press SPACE to Start / Jump", True, (44, 62, 80))
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 30))
            if last_score:
                over = font.render(f"Last score: {last_score:05d}", True, (120, 30, 30))
                screen.blit(over, (WIDTH // 2 - over.get_width() // 2, HEIGHT // 2 + 10))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

