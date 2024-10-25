import streamlit as st

st.title("Flappy Bird Game")

# Display an informational message
st.write("This app demonstrates the Flappy Bird game developed with Python and Pygame.")

# Embed the GIF (replace 'flappy_bird_demo.gif' with your file path or URL)
st.image("https://raw.githubusercontent.com/yourusername/yourrepository/main/flappy_bird_demo.gif", caption="Flappy Bird Gameplay", use_column_width=True)

st.write("The game was developed using Python's Pygame library. To play it interactively, clone the GitHub repository and run it locally.")

import pygame
import random

# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game settings
GRAVITY = 0.5
BIRD_JUMP = -10
PIPE_SPEED = 3
PIPE_GAP = 150

# Bird class
class Bird:
    def __init__(self):
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(50, SCREEN_HEIGHT // 2))
        self.velocity = 0

    def jump(self):
        self.velocity = BIRD_JUMP

    def move(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

# Pipe class
class Pipe:
    def __init__(self, x, y, is_top=False):
        self.image = pygame.Surface((60, SCREEN_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(midtop=(x, y))
        if is_top:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottom = y - PIPE_GAP // 2
        else:
            self.rect.top = y + PIPE_GAP // 2

    def move(self):
        self.rect.x -= PIPE_SPEED

# Function to create pipe pair
def create_pipes():
    y_pos = random.randint(200, SCREEN_HEIGHT - 200)
    top_pipe = Pipe(SCREEN_WIDTH, y_pos, True)
    bottom_pipe = Pipe(SCREEN_WIDTH, y_pos)
    return top_pipe, bottom_pipe

# Main game function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    bird = Bird()
    pipes = [create_pipes()]
    score = 0
    game_over = False

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        # Game Logic
        if not game_over:
            bird.move()

            # Move pipes and add new pipes
            for pipe_pair in pipes:
                for pipe in pipe_pair:
                    pipe.move()
            
            # Check for collision
            for pipe_pair in pipes:
                for pipe in pipe_pair:
                    if bird.rect.colliderect(pipe.rect):
                        game_over = True
                        break

            # Remove pipes that have moved off-screen and add new ones
            if pipes[0][0].rect.right < 0:
                pipes.pop(0)
                pipes.append(create_pipes())
                score += 1

            # Check if bird hits the ground
            if bird.rect.top <= 0 or bird.rect.bottom >= SCREEN_HEIGHT:
                game_over = True

        # Drawing on screen
        screen.fill(BLACK)
        screen.blit(bird.image, bird.rect)
        for pipe_pair in pipes:
            for pipe in pipe_pair:
                screen.blit(pipe.image, pipe.rect)

        # Update Display
        pygame.display.flip()
        clock.tick(30)

# Run the game
if __name__ == "__main__":
    main()
