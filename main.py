import pygame
import random
import sys

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Coffee Maker Game")
font = pygame.font.Font(None, 48)
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PINK = (255, 105, 180)

# Game states
START, ORDER, PLAYING, RESULT, END = range(5)
game_state = START

# Drinks and their recipes
drinks = {
    "Espresso": ['E'],
    "Espresso Macchiato": ['E', 'F'],
    "Latte": ['E', 'M', 'F'],
    "Flat White": ['E', 'M'],
    "Cappuccino": ['E', 'M', 'F'],
    "Americano": ['E', 'W']
}

# Random order
def get_random_order():
    return random.choice(list(drinks.items()))

# Game variables
current_order = None
inputs = []
message = ""
message_color = WHITE
fade_out = False
fade_alpha = 0

# Load coffee images
coffee_images = {
    "Espresso": pygame.image.load("espresso.png"),
    "Espresso Macchiato": pygame.image.load("espresso_macchiato.png"),
    "Latte": pygame.image.load("latte.png"),
    "Flat White": pygame.image.load("flat_white.png"),
    "Cappuccino": pygame.image.load("cappuccino.png"),
    "Americano": pygame.image.load("americano.png")
}

# Main game loop
running = True
while running:
    screen.fill((73, 40, 22))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == START:
            if event.type == pygame.KEYDOWN:
                game_state = ORDER

        elif game_state == ORDER:
            current_order = get_random_order()
            inputs = []
            message = ""
            game_state = PLAYING

        elif game_state == PLAYING:
            if event.type == pygame.KEYDOWN:
                key = event.unicode.upper()
                if key in ['E', 'F', 'M', 'W']:
                    inputs.append(key)
                    if sorted(inputs) == sorted(current_order[1]):
                        message = "Correct!"
                        message_color = GREEN
                        game_state = RESULT
                    elif not all(k in current_order[1] for k in inputs):
                        message = "Incorrect!"
                        message_color = RED
                        game_state = RESULT

        elif game_state == RESULT:
            if not fade_out:
                fade_out = True

        elif game_state == END:
            if event.type == pygame.KEYDOWN:
                game_state = START
                fade_out = False
                fade_alpha = 0

    if game_state == START:
        text = font.render("Press any key to start", True, WHITE)
        screen.blit(text, (200, 250))

    elif game_state == ORDER:
        pass

    elif game_state == PLAYING:
        order_text = font.render(f"Customer: I'd like a {current_order[0]}", True, WHITE)
        screen.blit(order_text, (100, 50))
        coffee_image = coffee_images[current_order[0]]
        screen.blit(coffee_image, (400, 150))

        # Draw key legend
        keys = [('E', 'Espresso'), ('F', 'Milk Foam'), ('M', 'Steamed Milk'), ('W', 'Water')]
        for idx, (key, label) in enumerate(keys):
            color = PINK if key in inputs else WHITE
            legend = font.render(f"{key}: {label}", True, color)
            screen.blit(legend, (50, 150 + idx * 40))

    elif game_state == RESULT:
        result_text = font.render(message, True, message_color)
        screen.blit(result_text, (300, 250))
        if fade_out:
            fade_surface = pygame.Surface((800, 600))
            fade_surface.fill(BLACK)
            fade_alpha += 5
            if fade_alpha >= 255:
                fade_alpha = 255
                game_state = END
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))

    elif game_state == END:
        restart_text = font.render("Restart? Press any key", True, WHITE)
        screen.blit(restart_text, (200, 250))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
