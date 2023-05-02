import pygame
import sys
from button import Button

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

def title_screen(screen):
    start_button = Button("Start", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50, (50, 150, 50), (100, 200, 100))
    quit_button = Button("Quit", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50, (150, 50, 50), (200, 100, 100))

    waiting = True
    while waiting:
        screen.fill(BLACK)
        start_button.draw(screen)
        quit_button.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                if start_button.is_mouse_over(event.pos):
                    start_button.current_color = start_button.hover_color
                else:
                    start_button.current_color = start_button.color

                if quit_button.is_mouse_over(event.pos):
                    quit_button.current_color = quit_button.hover_color
                else:
                    quit_button.current_color = quit_button.color

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_mouse_over(event.pos):
                    waiting = False
                if quit_button.is_mouse_over(event.pos):
                    pygame.quit()
                    sys.exit()
