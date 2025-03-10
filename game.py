import pygame
import random

# Initialize Pygame
pygame.init()

# Game Window
WIDTH, HEIGHT = 800, 600
BG_COLOR = (10, 10, 30)  # Dark space-like background

SHIP_COLOR = (0, 255, 255)  # Neon cyan spaceship
SHIP_WIDTH, SHIP_HEIGHT = 40, 20
FPS = 60

# Ship movement variables
ship_x = (WIDTH // 2) - (SHIP_WIDTH // 2)
ship_y = HEIGHT - 80
ship_speed = 2
ship_direction = 1  # 1 = right, -1 = left
reaction_delay = 30  # Frames before reacting to danger
manual_move = False  # To check if ship is in manual mode (Play button pressed)

# Define Danger Zone (where the ship starts dodging)
DANGER_ZONE_Y = HEIGHT // 2  # Anything below this is a threat

# Bullets
BULLET_COLOR = (255, 255, 255)  # White bullets
BULLET_WIDTH, BULLET_HEIGHT = 5, 10
bullets = []
BULLET_SPEED = 5
BULLET_INTERVAL = 500  # Time in milliseconds between shots
last_shot_time = 0

PIERCING_SHOT = False  # Default: bullets disappear after 1 hit

# Asteroid list
ASTEROID_COLOR = (255, 0, 0)  # Red asteroids
ASTEROID_SIZE = 30
asteroids = []
ASTEROID_SPEED = 3
ASTEROID_SPAWN_RATE = 30  # In frames, higher = less frequent spawn
frame_count = 0  # Counter to control asteroid spawn rate

# Define Horizontal Line for Asteroids to spawn
ASTEROID_SPAWN_Y = 100  # Horizontal line where asteroids spawn

# Score and Lives
score = 0
lives = 3
HEART_COLOR = (255, 105, 180)  # Pink hearts color

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Breaker")

# Font for score and lives
font = pygame.font.SysFont('Arial', 24)

# Game loop
running = True
clock = pygame.time.Clock()

# Function to reset the game
def reset_game():
    global ship_x, ship_y, bullets, asteroids, score, lives
    ship_x = (WIDTH // 2) - (SHIP_WIDTH // 2)
    ship_y = HEIGHT - 80
    bullets = []
    asteroids = []
    score = 0
    lives = 3
    manual_move = True

# Initialize play button clicked flag
play_button_clicked = False

# Play button rectangle
play_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)

# Define a "Continue" button rectangle
continue_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 30, 150, 50)

while running:
    screen.fill(BG_COLOR)  # Fill background
    current_time = pygame.time.get_ticks()  # Get time in milliseconds
    frame_count += 1

    # Check if Play button is clicked
    if play_button.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0] and not play_button_clicked:
            play_button_clicked = True  # Set flag to true when button is clicked
            manual_move = True
            reset_game()  # Reset game when starting over

    # Draw play button if it hasn't been clicked yet
    if not play_button_clicked:
        pygame.draw.rect(screen, (0, 255, 0), play_button)
        play_text = font.render("Play", True, (255, 255, 255))
        screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, HEIGHT // 2 - play_text.get_height() // 2))

    # Define Edge Padding (prevents ship from touching screen edges)
    EDGE_PADDING = 100

    # Ship Movement
    if manual_move:
        EDGE_PADDING = 0
        ship_speed = 3.5  # Increase ship speed
        BULLET_INTERVAL = 350  # Increase bullet rate (shoot faster)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            ship_x -= ship_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            ship_x += ship_speed

    # Detect the closest asteroid in the danger zone (idle mode)
    if not manual_move:
        closest_asteroid = None
        for asteroid in asteroids:
            if asteroid[1] > DANGER_ZONE_Y and abs(asteroid[0] - ship_x) < ASTEROID_SIZE * 2:
                if closest_asteroid is None or asteroid[1] > closest_asteroid[1]:
                    closest_asteroid = asteroid

        # Move spaceship automatically (AI Avoidance)
        if closest_asteroid and reaction_delay <= 0:
            if closest_asteroid[0] < ship_x and ship_x + SHIP_WIDTH < WIDTH:
                ship_direction = 1  # Move right
            elif closest_asteroid[0] > ship_x and ship_x > 0:
                ship_direction = -1  # Move left
            reaction_delay = 15  # Reset reaction delay

        if reaction_delay > 0:
            reaction_delay -= 1  # Decrease delay to make dodging natural

        ship_x += ship_speed * ship_direction

    if ship_x <= EDGE_PADDING:
        ship_x = EDGE_PADDING
        ship_direction = 1  # Change direction
    elif ship_x + SHIP_WIDTH >= WIDTH - EDGE_PADDING:
        ship_x = WIDTH - EDGE_PADDING - SHIP_WIDTH
        ship_direction = -1  # Change direction

    # Auto-shoot bullets
    if current_time - last_shot_time > BULLET_INTERVAL:
        bullets.append([ship_x + SHIP_WIDTH // 2, ship_y])  # Spawn bullet at ship position
        last_shot_time = current_time

    # Move bullets
    for bullet in bullets[:]:
        bullet[1] -= BULLET_SPEED  # Move bullet upwards
        if bullet[1] < 0:  # Remove bullet if it leaves the screen
            bullets.remove(bullet)
    
    # Spawn asteroids horizontally from the defined line
    if frame_count % ASTEROID_SPAWN_RATE == 0:
        asteroid_x = random.randint(100, WIDTH - ASTEROID_SIZE)  # Horizontal random spawn
        asteroids.append([asteroid_x, ASTEROID_SPAWN_Y])

    # Move asteroids
    for asteroid in asteroids[:]:
        asteroid[1] += ASTEROID_SPEED  # Move asteroid downward
        if asteroid[1] > HEIGHT:  # Remove asteroid if it leaves the screen
            asteroids.remove(asteroid)

    # Detect collisions between bullets and asteroids
    for bullet in bullets[:]:  
        for asteroid in asteroids[:]:  
            if (bullet[0] > asteroid[0] and bullet[0] < asteroid[0] + ASTEROID_SIZE and
                bullet[1] > asteroid[1] and bullet[1] < asteroid[1] + ASTEROID_SIZE):
                asteroids.remove(asteroid)  # Destroy asteroid
                bullets.remove(bullet)  # Destroy bullet
                score += 10  # Increase score
                break  # Stop checking more asteroids

    # Check collisions between ship and asteroids (deduct life)
    for asteroid in asteroids[:]:
        if (ship_x + SHIP_WIDTH > asteroid[0] and ship_x < asteroid[0] + ASTEROID_SIZE and
            ship_y + SHIP_HEIGHT > asteroid[1] and ship_y < asteroid[1] + ASTEROID_SIZE):
            lives -= 1  # Deduct a life
            asteroids.remove(asteroid)  # Remove the asteroid on collision
            if lives <= 0:  # If lives are exhausted
                manual_move = False  # Disable manual movement
                break

    # Only check ship collisions if manual mode is active
    if manual_move:
        for asteroid in asteroids[:]:
            if (ship_x + SHIP_WIDTH > asteroid[0] and ship_x < asteroid[0] + ASTEROID_SIZE and
                ship_y + SHIP_HEIGHT > asteroid[1] and ship_y < asteroid[1] + ASTEROID_SIZE):
                lives -= 1
                asteroids.remove(asteroid)
                if lives <= 0:
                    manual_move = False
                    break

    # Draw spaceship (temporary rectangle, will replace with sprite later)
    pygame.draw.rect(screen, SHIP_COLOR, (ship_x, ship_y, SHIP_WIDTH, SHIP_HEIGHT))

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, BULLET_COLOR, (bullet[0], bullet[1], BULLET_WIDTH, BULLET_HEIGHT))

    # Draw asteroids
    for asteroid in asteroids:
        pygame.draw.rect(screen, ASTEROID_COLOR, (asteroid[0], asteroid[1], ASTEROID_SIZE, ASTEROID_SIZE))

    # Draw Score (top-left)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Draw Lives (top-right)
    if manual_move:
        for i in range(lives):
            pygame.draw.circle(screen, HEART_COLOR, (WIDTH - 30 - (i * 30), 30), 15)

    # Game over screen if no lives
    if lives <= 0:
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 30))

        # Draw the "Continue" button
        pygame.draw.rect(screen, (0, 255, 255), continue_button)  # Cyan button color
        continue_text = font.render("Continue...?", True, (255, 255, 255))
        screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 + 40))

        # Check if the "Continue" button is clicked
        if continue_button.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:  # Left-click to reset
                reset_game()  # Reset the game (similar to Play button click)
                lives = 3  # Reset lives to 3
                score = 0  # Reset score
                manual_move = True  # Return to idle movement

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()  # Update screen
    clock.tick(FPS)  # Control game speed

pygame.quit()
