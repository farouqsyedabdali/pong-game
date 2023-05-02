import pygame, sys
from button import Button
from title_screen import title_screen as ts
from pause_screen import pause_screen

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set the dimensions of the screen
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

# Define the Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.velocity = [5, 5]
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if self.rect.y > SCREEN_HEIGHT - 10 or self.rect.y < 0:
            self.velocity[1] = -self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]

# Define the Paddle class
class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x_pos):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = SCREEN_HEIGHT // 2 - height // 2

    def move_up(self, pixels):
        self.rect.y -= pixels
        if self.rect.y < 0:
            self.rect.y = 0

    def move_down(self, pixels):
        self.rect.y += pixels
        if self.rect.y > SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height

# Initialize Pygame
pygame.init()

# Set the screen dimensions
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Set the title of the window
pygame.display.set_caption('Pong')

# Title screen before the game starts
ts(screen)

# Create the sprites
player1_paddle = Paddle(WHITE, 10, 100, 20)
player2_paddle = Paddle(WHITE, 10, 100, SCREEN_WIDTH - 30)
ball = Ball(WHITE, 10, 10)
ball.rect.x = SCREEN_WIDTH // 2
ball.rect.y = SCREEN_HEIGHT // 2

# Add the sprites to the sprite list
all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(player1_paddle)
all_sprites_list.add(player2_paddle)
all_sprites_list.add(ball)

# Set the game loop
game_on = True
clock = pygame.time.Clock()

# Set the initial score
player1_score = 0
player2_score = 0

# Set the font for the score
font = pygame.font.Font(None, 50)

# Create the pause button
pause_button = Button("Pause", SCREEN_WIDTH - 100, 10, 80, 30, (0, 0, 0), (65, 65, 65))

# Main game loop
while game_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_on = False
            if event.key == pygame.K_p:
                pause_screen(screen)

        if event.type == pygame.MOUSEMOTION:
            if pause_button.is_mouse_over(event.pos):
                pause_button.current_color = pause_button.hover_color
            else:
                pause_button.current_color = pause_button.color

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pause_button.is_mouse_over(event.pos):
                pause_screen(screen)

    # Move the player 1 paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player1_paddle.move_up(5)
    if keys[pygame.K_s]:
        player1_paddle.move_down(5)

        # Move the player 2 paddle
    if keys[pygame.K_UP]:
        player2_paddle.move_up(5)
    if keys[pygame.K_DOWN]:
        player2_paddle.move_down(5)

    # Check if the ball goes off the screen
    if ball.rect.x > SCREEN_WIDTH:
        player1_score += 1
        ball.rect.x = SCREEN_WIDTH // 2
        ball.rect.y = SCREEN_HEIGHT // 2
        ball.velocity[0] = -ball.velocity[0]
    elif ball.rect.x < 0:
        player2_score += 1
        ball.rect.x = SCREEN_WIDTH // 2
        ball.rect.y = SCREEN_HEIGHT // 2
        ball.velocity[0] = -ball.velocity[0]

    # Check for collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, player1_paddle) or pygame.sprite.collide_mask(ball, player2_paddle):
        ball.bounce()

    # Update the ball's position
    ball.update()

    # Clear the screen
    screen.fill(BLACK)

    # Draw the sprites
    pygame.draw.line(screen, WHITE, [SCREEN_WIDTH // 2, 0], [SCREEN_WIDTH // 2, SCREEN_HEIGHT], 5)
    all_sprites_list.draw(screen)

    # Draw the pause button
    pause_button.draw(screen)

    # Draw the score
    player1_text = font.render(str(player1_score), True, WHITE)
    player2_text = font.render(str(player2_score), True, WHITE)
    screen.blit(player1_text, (SCREEN_WIDTH // 4, 10))
    screen.blit(player2_text, (SCREEN_WIDTH // 4 * 3, 10))

    # Update the screen
    pygame.display.flip()

    # Set the game's frame rate
    clock.tick(60)

# Close the window and quit Pygame
pygame.quit()
