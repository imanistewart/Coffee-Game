# Coffee Maker Game - Development Log

# v1.0 - Initial Concept
# - Set up basic Pygame loop and window.
# - Created a start screen and game state management.
# - Defined six coffee recipes with associated key inputs (E, F, M, W).
# - Randomized customer orders and validated key inputs to match the recipe.

# v1.1 - Visual Enhancements
# - Designed and integrated six individual coffee images.
# - Coffee image source: https://www.homestratosphere.com/wp-content/uploads/2019/05/A-quick-guide-to-types-of-coffee-you-can-order-4-14-5.jpg
# - Displayed customer order with an associated image of the drink.
# - Created a static legend showing key mappings on the left side of the screen.

# v1.2 - Interactive Feedback
# - Implemented immediate feedback with colored text messages for correctness.
# - Made pressed keys glow pink in the key legend.
# - Used white, green, and red color cues to communicate results.

# v1.3 - Score and Combo System
# - Added a combo multiplier and score tracking system.
# - Score increases with each correct drink, and combo multiplies the score.
# - Game no longer ends after a correct drink; play continues until a mistake.

# v1.4 - Sound Integration
# - Added a 'ding' sound when a drink is made correctly.
# - Added a 'buzzer' sound for incorrect attempts.

# v1.5 - Timer Mechanic
# - Introduced a 5-second countdown timer for each drink.
# - If the timer reaches zero, the game ends with an "Incorrect!" message.

# v1.6 - UI Polish
# - Countdown timer is now visible in the top-right corner.
# - Adjusted the timer font size and position for a clean look.
# - Moved score and combo text to the bottom-left corner.
# - Changed background color to a cozy brown cafe tone.

# --- Game Code Starts Below ---

import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Coffee Maker Game")
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 32)
timer_font = pygame.font.Font(None, 28)
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BROWN = (73, 40, 21)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PINK = (255, 105, 180)

# Sounds
ding_sound = pygame.mixer.Sound("ding.wav")
buzz_sound = pygame.mixer.Sound("buzz.wav")

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

def get_random_order(last_order):
    options = list(drinks.items())
    if last_order:
        options = [drink for drink in options if drink[0] != last_order]
    return random.choice(options)

# Game variables
current_order = None
last_order_name = None
inputs = []
message = ""
message_color = WHITE
score = 0
combo = 0
start_time = 0

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
    screen.fill(BROWN)
    current_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == START:
            if event.type == pygame.KEYDOWN:
                score = 0
                combo = 0
                game_state = ORDER

        elif game_state == ORDER:
            current_order = get_random_order(last_order_name)
            last_order_name = current_order[0]
            inputs = []
            message = ""
            start_time = time.time()
            game_state = PLAYING

        elif game_state == PLAYING:
            if event.type == pygame.KEYDOWN:
                key = event.unicode.upper()
                if key in ['E', 'F', 'M', 'W']:
                    inputs.append(key)
                    if sorted(inputs) == sorted(current_order[1]):
                        message = "Correct!"
                        message_color = GREEN
                        combo += 1
                        score += 10 * combo
                        ding_sound.play()
                        game_state = ORDER
                    elif not all(k in current_order[1] for k in inputs):
                        message = "Incorrect!"
                        message_color = RED
                        combo = 0
                        buzz_sound.play()
                        game_state = END

        elif game_state == END:
            if event.type == pygame.KEYDOWN:
                game_state = START

    if game_state == START:
        text = font.render("Press any key to start", True, WHITE)
        screen.blit(text, (200, 250))

    elif game_state == ORDER:
        pass

    elif game_state == PLAYING:
        elapsed_time = current_time - start_time
        if elapsed_time > 5:
            message = "Incorrect!"
            message_color = RED
            combo = 0
            buzz_sound.play()
            game_state = END

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

        # Display score and combo at bottom left
        score_text = small_font.render(f"Score: {score}", True, WHITE)
        combo_text = small_font.render(f"Combo: x{combo}", True, WHITE)
        screen.blit(score_text, (30, 520))
        screen.blit(combo_text, (30, 560))

        # Display countdown timer (smaller and further right)
        time_left = max(0, 5 - int(elapsed_time))
        timer_text = timer_font.render(f"Time Left: {time_left}", True, WHITE)
        screen.blit(timer_text, (690, 10))

    elif game_state == END:
        result_text = font.render(message, True, message_color)
        screen.blit(result_text, (300, 250))
        restart_text = font.render("Restart? Press any key", True, WHITE)
        final_score = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(restart_text, (200, 320))
        screen.blit(final_score, (250, 380))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
