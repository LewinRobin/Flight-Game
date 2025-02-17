import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
game_name = "Space Dodge"
pygame.display.set_caption(game_name)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Load sprites
# Make sure these files exist in the same directory as your script
try:
    plane_sprite = pygame.image.load(
        './assets/sprites/plane.png').convert_alpha()
    bomb_sprite = pygame.image.load(
        './assets/sprites/missile.png').convert_alpha()
    monster_sprite = pygame.image.load(
        './assets/sprites/monster.png').convert_alpha()
    big_missile_sprite = pygame.image.load(
        './assets/sprites/Big_missile.png').convert_alpha()
    life_sprite = pygame.image.load(
        './assets/sprites/life.png').convert_alpha()
except pygame.error:
    print("Warning: Could not load sprite images. Make sure plane.png and bomb.png exist.")

# Fonts
font = './assets/fonts/BigBlueTerm437NerdFont-Regular.ttf'
font_large = pygame.font.Font(font, 60)
font_medium = pygame.font.Font(font, 40)
font_small = pygame.font.Font(font, 25)

# Clock for controlling frame rate
clock = pygame.time.Clock()


class Player:
    def __init__(self):
        self.sprite = plane_sprite
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height - 100
        self.vel = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        screen.blit(self.sprite, (self.x, self.y))

    def move(self, keys):
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # Move right
            self.x = min(self.x + self.vel, screen_width - self.width)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # Move left
            self.x = max(self.x - self.vel, 0)


class Life:
    def __init__(self, x):
        self.sprite = life_sprite
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.x = x
        self.y = 25
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        screen.blit(self.sprite, (self.x, self.y))


class Monster:
    def __init__(self):
        self.sprite = monster_sprite
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.x = screen_width // 2 - self.width // 2
        self.y = 0
        self.vel = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        screen.blit(monster_sprite, (self.x, self.y))

    def move(self, x):
        if x > self.x:
            self.x = min(self.x + self.vel, x)
        else:
            self.x = max(self.x - self.vel, x)


class Missile:
    def __init__(self, speed):
        self.sprite = bomb_sprite
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.x = random.randint(0, screen_width - self.width)
        self.y = -self.height
        self.vel = speed
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        screen.blit(self.sprite, (self.x, self.y))

    def move(self):
        self.y += self.vel
        return self.y >= screen_height  # Return True if missile is off screen


class Big_Missile(Missile):
    def __init__(self, speed, x):
        super().__init__(speed)
        self.x = x
        self.sprite = big_missile_sprite


def load_sound(path):
    """because pygame can be compiled without mixer."""
    if not pygame.mixer:
        return None
    try:
        sound = pygame.mixer.Sound(path)
        return sound
    except pygame.error:
        print(f"Warning, unable to load, {path}")


def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


def draw_button(x, y, width, height, font_size,  color, text, func):
    button_rect = pygame.Rect(y, x, width, height)
    button_color = color
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    font_set = pygame.font.Font(font, font_size)
    text = font_set.render(text, True, BLACK)
    text_rect = text.get_rect(center=button_rect.center)
    # Change color on hover

    if button_rect.collidepoint(mouse_pos):
        button_color = WHITE
        if mouse_click[0]:  # Left mouse button is clicked
            func()
    else:
        button_color = color

    # Draw button
    pygame.draw.rect(screen, button_color,
                     button_rect, border_radius=10)
    screen.blit(text, text_rect)


def main_menu():
    global font
    while True:
        screen.fill(BLACK)
        draw_button(125, screen_width//2 - 175, 350, 50, 40,
                    GREEN, "Start(Space)", game_loop)
        draw_button(450, screen_width//2 - 175, 350, 50,
                    40, RED, "Quit(Q)", sys.exit)
        draw_text(game_name, font_large,
                  WHITE, screen_width // 2, screen_height // 2)
        draw_text("Use A/D or LEFT/RIGHT keys to move ",
                  font_small, YELLOW, screen_width // 2, 400)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def pause_screen():
    paused = True

    while paused:
        screen.fill((0, 0, 0), pygame.Rect(200, 200, 400, 200))
        pygame.draw.rect(screen, WHITE, (200, 200, 400, 200), 2)

        draw_text("PAUSED", font_medium, WHITE, screen_width // 2, 250)

        # making pause button manualy
        button_rect = pygame.Rect(screen_width // 2 - 150, 300, 300, 30)
        button_color = GREEN
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        font_set = pygame.font.Font(font, 25)
        text = font_set.render("Continue(P)", True, BLACK)
        text_rect = text.get_rect(center=button_rect.center)
        # Change color on hover

        if button_rect.collidepoint(mouse_pos):
            button_color = WHITE
            if mouse_click[0]:  # Left mouse button is clicked
                paused = False
        else:
            button_color = GREEN

        # Draw button
        pygame.draw.rect(screen, button_color,
                         button_rect, border_radius=10)
        screen.blit(text, text_rect)
        draw_button(350, screen_width // 2 - 150, 300,
                    30, 25,  YELLOW, "Main Menu(M)", main_menu)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                if event.key == pygame.K_m:
                    main_menu()


def game_over_screen(score):
    while True:
        screen.fill(BLACK)

        draw_text("GAME OVER", font_large, RED, screen_width // 2, 100)
        draw_text(f"Score: {score}", font_medium,
                  WHITE, screen_width // 2, 200)
        draw_button(275, screen_width // 2 - 175, 350,
                    50, 40,  GREEN, "Restart(R)", game_loop)
        draw_button(375, screen_width // 2 - 175, 350,
                    50, 40,  YELLOW, "Main Menu(M)", lambda: main_menu())

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                if event.key == pygame.K_m:
                    main_menu()


def game_loop():
    player = Player()
    monster = Monster()
    missiles = []
    score = 0
    missile_timer = 0
    missile_spawn_rate = 60  # Frames between missile spawns
    missile_speed = 5
    monster_timer = 0
    life = 5
    life_x_array = [30 * i for i in range(life)]

    boom_sound = load_sound("./assets/audiio/boom.wav")
    if pygame.mixer:
        pygame.mixer.music.load("./assets/audiio/house_lo.wav")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause_screen()

        # Get pressed keys
        keys = pygame.key.get_pressed()

        # Move player
        player.move(keys)

        # Spawn missiles
        missile_timer += 1
        if missile_timer >= missile_spawn_rate:
            missiles.append(Missile(missile_speed))
            missile_timer = 0

            # Increase difficulty over time
            if missile_spawn_rate > 20:
                missile_spawn_rate -= 1
            if score % 10 == 0 and score > 0:
                missile_speed += 0.5

        # Update missiles and check for collisions
        missiles_to_remove = []
        for i, missile in enumerate(missiles):
            if missile.move():  # Returns True if missile is off screen
                missiles_to_remove.append(i)
                score += 1

            # Check collision
            if player.rect.colliderect(missile.rect):
                # Add collided missile to removal list
                missiles_to_remove.append(i)
                life -= 1
                boom_sound.play()
                life_x_array.pop()
                if (life <= 0):
                    game_over_screen(score)

        # Remove missiles that went off screen
        for i in reversed(missiles_to_remove):
            missiles.pop(i)

        # Draw everything
        screen.fill(BLACK)

        # Draw background - simple stars
        for _ in range(20):
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            pygame.draw.circle(screen, WHITE, (x, y), 1)

        # Life
        for i in life_x_array:
            Life(i).draw()

        # Draw game objects
        player.draw()
        if (score > 10):
            monster_timer += 1
            monster.draw()
            if monster_timer % 4 == 0:
                monster.move(player.x)
            if monster_timer % 60 == 0:
                missiles.append(Big_Missile(missile_speed, monster.x))

        for missile in missiles:
            missile.draw()

        # Draw HUD
        draw_text(f"Score: {score}", font_small, WHITE, 90, 20)
        draw_text("Press P to Pause", font_small,
                  WHITE, screen_width - 150, 20)

        pygame.display.update()
        clock.tick(60)  # 60 FPS


# Start the game
if __name__ == "__main__":
    main_menu()
