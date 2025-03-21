import pygame
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 15

# Colors
BLACK = (30, 30, 30)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (50, 50, 50)
RED = (255, 0, 0)

# Add this variable at the beginning of your game loop
rotation_angle = 0
speed = 10

food_pos = [0, 0]

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock to control game speed
clock = pygame.time.Clock()

# Snake and food setup
def initialize_game():
    snake_pos = [[WIDTH // 2, HEIGHT // 2], [WIDTH // 2 - CELL_SIZE, HEIGHT // 2], [WIDTH // 2 - 2 * CELL_SIZE, HEIGHT // 2]]  # Initial snake position
    direction = "RIGHT"
    food_pos = [
        random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE,
        random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE
    ]
    food_spawn = True
    return snake_pos, direction, food_pos, food_spawn

# Menu screen
def menu_screen():
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont("arial", 50)
        title_text = font.render("Snake Game", True, GREEN)
        start_text = font.render("Press SPACE to Start", True, WHITE)
        quit_text = font.render("Press Q to Quit", True, WHITE)

        screen.blit(title_text, [WIDTH // 2 - 150, HEIGHT // 2 - 100])
        screen.blit(start_text, [WIDTH // 2 - 200, HEIGHT // 2])
        screen.blit(quit_text, [WIDTH // 2 - 200, HEIGHT // 2 + 50])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

target_animation_length = 5
target_animation_frame = - target_animation_length
target_animation_speed = 1
def draw_target(color = RED, background_color = BLACK):
    # Draw a circle in the same size as base_ball in the food position, it will pulsate in size
    global target_animation_frame, target_animation_length, target_animation_speed

    # Calculate the size of the ball
    ball_size = (CELL_SIZE + target_animation_frame) // 2 

    # Draw the ball
    food_ball = pygame.draw.circle(screen, color, food_pos, ball_size)

    # Draw small static white dot in the center of the ball
    dot_size = max(ball_size // 5, 2)
    pygame.draw.circle(screen, WHITE, food_pos, dot_size)

    # Update the animation frame
    target_animation_frame += target_animation_speed
    if target_animation_frame >= target_animation_length or target_animation_frame <= -target_animation_length:
        # target_animation_frame = -target_animation_length
        target_animation_speed *= -1

# Main game loop
def game_loop():
    global CELL_SIZE, rotation_angle, speed, food_pos

    snake_pos, direction, food_pos, food_spawn = initialize_game()
    score = 0

    # Add a few extra cells to the snake
    for _ in range(50):
        snake_pos.append(list(snake_pos[-1]))

    while True:
        rotation_angle += 5
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        def draw_aim_arrow(color = GRAY, background_color = BLACK):
            # Get the centroid of the snake's head
            centroid = (snake_pos[0][0] + CELL_SIZE // 2, snake_pos[0][1] + CELL_SIZE // 2)
            
            base_ball_size = max(CELL_SIZE / 3 , 10)

            # Draw the base ball
            base_ball = pygame.draw.circle(screen, color, centroid, base_ball_size)

            # Draw the shaft
            # shaft = pygame.draw.line(screen, color, centroid, food_pos, 2)

            # Draw dashes on the shaft
            # Calculate the distance between the snake head and the food
            distance = ((food_pos[0] - centroid[0]) ** 2 + (food_pos[1] - centroid[1]) ** 2) ** 0.5
            # Calculate the number of dashes
            num_dashes = max(int(distance / 5),10)
            # Calculate the step size for each dash
            step_size = (food_pos[0] - centroid[0]) / num_dashes, (food_pos[1] - centroid[1]) / num_dashes
            # Draw the dashes
            for i in range(num_dashes):
                if i % 2 == 0:
                    pygame.draw.line(screen, color, (centroid[0] + i * step_size[0], centroid[1] + i * step_size[1]), (centroid[0] + (i + 1) * step_size[0], centroid[1] + (i + 1) * step_size[1]), 2)

           # Draw a circle in the same size as base_ball in the food position
            food_ball = pygame.draw.circle(screen, color, food_pos, base_ball_size)





            # food_ball = pygame.draw.circle(screen, color, food_pos, CELL_SIZE // 2)


        # Control direction with arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != "DOWN":
            direction = "UP"
        if keys[pygame.K_DOWN] and direction != "UP":
            direction = "DOWN"
        if keys[pygame.K_LEFT] and direction != "RIGHT":
            direction = "LEFT"
        if keys[pygame.K_RIGHT] and direction != "LEFT":
            direction = "RIGHT"

        # Other specific animation 

        # Move snake
        if direction == "UP":
            snake_pos[0][1] -= CELL_SIZE
            # Loop the snake from one end of the screen to the other
            if snake_pos[0][1] < 0:
                snake_pos[0][1] = HEIGHT
        if direction == "DOWN":
            snake_pos[0][1] += CELL_SIZE
            # Loop the snake from one end of the screen to the other
            if snake_pos[0][1] > HEIGHT:
                snake_pos[0][1] = 0
        if direction == "LEFT":
            snake_pos[0][0] -= CELL_SIZE
            # Loop the snake from one end of the screen to the other
            if snake_pos[0][0] < 0:
                snake_pos[0][0] = WIDTH
        if direction == "RIGHT":
            snake_pos[0][0] += CELL_SIZE
            # Loop the snake from one end of the screen to the other
            if snake_pos[0][0] > WIDTH:
                snake_pos[0][0] = 0

        # Grow snake when eating food
        # Test if the distance between the snake head and the food is less than the size of the cell
        if abs(snake_pos[0][0] - food_pos[0]) < CELL_SIZE and abs(snake_pos[0][1] - food_pos[1]) < CELL_SIZE:
        # if snake_pos[0] == food_pos:
            score += 1
            food_spawn = False
        else:
            snake_pos.pop()

        if not food_spawn:
            food_pos = [
                random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE,
                random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE
            ]

            food_spawn = True
            CELL_SIZE -= 1
            speed += 0.5


        # Add new head to snake
        snake_pos.insert(0, list(snake_pos[0]))

        # Check for collisions
        # if (
        #     snake_pos[0][0] < 0 or snake_pos[0][0] >= WIDTH or
        #     snake_pos[0][1] < 0 or snake_pos[0][1] >= HEIGHT or
        #     snake_pos[0] in snake_pos[1:]
        # ):
        #     game_over(score)

        # Draw everything
        screen.fill(BLACK)
        for indx, pos in enumerate(snake_pos):
            # Instead of pure Green, lets put a gradient color, respecting the limit of 255
            if 255 - indx * 5 < 0:
                color = (0, 0, 100)
            else:
                color = (0, 255 - indx * 5, 150)
            pygame.draw.rect(screen, color, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))
        # Draw food rotating on the screen
        # pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))
        # Draw food rotating on the screen
        # food_rect = pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE)

        # Draw this line thing to show the direction of the food
        draw_aim_arrow()

        # Draw a circle instead of a rectangle
        draw_target()

        # pygame.draw.circle(screen, RED, (food_pos[0], food_pos[1]), CELL_SIZE // 2)


        # rotated_food = pygame.transform.rotate(pygame.Surface((CELL_SIZE, CELL_SIZE)), rotation_angle)
        # rotated_food.fill(RED)
        # screen.blit(food_ball, food_ball.topleft)


        # Display score
        font = pygame.font.SysFont("arial", 25)
        # score_text = font.render(f"Score: {score}", True, WHITE)
        score_text = font.render(f"Size: {CELL_SIZE}", True, WHITE)
        screen.blit(score_text, [10, 10])

        pygame.display.update()
        clock.tick(speed)  # Control game speed

def game_over(score):
    font = pygame.font.SysFont("arial", 50)
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render(f"Your Score: {score}", True, WHITE)
    screen.fill(BLACK)
    screen.blit(game_over_text, [WIDTH // 2 - 100, HEIGHT // 2 - 50])
    screen.blit(score_text, [WIDTH // 2 - 150, HEIGHT // 2])
    pygame.display.update()
    time.sleep(3)
    pygame.quit()
    quit()

if __name__ == "__main__":
    menu_screen()
    game_loop()
