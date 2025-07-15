import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 50
DINO_WIDTH = 40
DINO_HEIGHT = 60
OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 40
JUMP_VELOCITY = -15
GRAVITY = 0.8
GROUND_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)

class Dino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = DINO_WIDTH
        self.height = DINO_HEIGHT
        self.velocity_y = 0
        self.on_ground = True
        self.ground_y = y
        
    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_VELOCITY
            self.on_ground = False
    
    def update(self):
        # Apply gravity
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        
        # Check if dino landed on ground
        if self.y >= self.ground_y:
            self.y = self.ground_y
            self.velocity_y = 0
            self.on_ground = True
    
    def draw(self, screen):
        # Draw dino as a simple rectangle with some details
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))
        # Draw eye
        pygame.draw.circle(screen, BLACK, (self.x + 10, self.y + 10), 3)
        # Draw legs
        pygame.draw.rect(screen, GREEN, (self.x + 5, self.y + self.height, 8, 10))
        pygame.draw.rect(screen, GREEN, (self.x + 25, self.y + self.height, 8, 10))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = OBSTACLE_WIDTH
        self.height = OBSTACLE_HEIGHT
        
    def update(self):
        self.x -= GROUND_SPEED
        
    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, self.height))
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def is_off_screen(self):
        return self.x + self.width < 0

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dino Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()
        
    def reset_game(self):
        self.dino = Dino(100, SCREEN_HEIGHT - GROUND_HEIGHT - DINO_HEIGHT)
        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.obstacle_timer = 0
        self.obstacle_delay = 90  # frames between obstacles
        
    def spawn_obstacle(self):
        obstacle_y = SCREEN_HEIGHT - GROUND_HEIGHT - OBSTACLE_HEIGHT
        obstacle = Obstacle(SCREEN_WIDTH, obstacle_y)
        self.obstacles.append(obstacle)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset_game()
                    else:
                        self.dino.jump()
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True
    
    def update(self):
        if self.game_over:
            return
            
        # Update dino
        self.dino.update()
        
        # Spawn obstacles
        self.obstacle_timer += 1
        if self.obstacle_timer >= self.obstacle_delay:
            self.spawn_obstacle()
            self.obstacle_timer = 0
            # Gradually increase difficulty
            if self.obstacle_delay > 30:
                self.obstacle_delay -= 1
        
        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle.update()
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
                self.score += 10
        
        # Check collisions
        dino_rect = self.dino.get_rect()
        for obstacle in self.obstacles:
            if dino_rect.colliderect(obstacle.get_rect()):
                self.game_over = True
                break
    
    def draw(self):
        self.screen.fill(WHITE)
        
        # Draw ground
        pygame.draw.rect(self.screen, GRAY, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
        
        # Draw dino
        self.dino.draw(self.screen)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER!", True, RED)
            restart_text = self.font.render("Press SPACE to restart", True, BLACK)
            
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(restart_text, restart_rect)
        
        # Draw instructions
        if self.score == 0 and not self.game_over:
            instruction_text = self.font.render("Press SPACE to jump!", True, BLACK)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
            self.screen.blit(instruction_text, instruction_rect)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
