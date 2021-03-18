import math
import sys

import pygame
from pygame.locals import *
import pygame_ai as pai

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Player(pai.gameobject.GameObject):
    
    def __init__(self, pos = (0, 0)):
        # First we create the image by filling a surface with blue color
        img = pygame.Surface( (10, 15) ).convert()
        img.fill(BLUE)
        # Call GameObject init with appropriate values
        super(Player, self).__init__(
            img_surf = img,
            pos = pos,
            max_speed = 15,
            max_accel = 40,
            max_rotation = 40,
            max_angular_accel = 30
        )
        
    def update(self, steering, tick):
        self.steer(steering, tick)
        self.rect.move_ip(self.velocity)
        
class CircleNPC(pai.gameobject.GameObject):
    
    def __init__(self, pos = (0, 0)):
        # First create the circle image with alpha channel to have transparency
        img = pygame.Surface( (10, 10) ).convert_alpha()
        img.fill( WHITE )
        # Draw the circle
        pygame.draw.circle(img, RED, (5, 5), 5)
        # Call GameObject init with appropiate values
        super(CircleNPC, self).__init__(
            img_surf = img,
            pos = pos,
            max_speed = 10,
            max_accel = 40,
            max_rotation = 40,
            max_angular_accel = 30
        )
        # Create a placeholder for the AI
        self.ai = pai.steering.kinematic.NullSteering()
        
    def update(self, tick):
        steering = self.ai.get_steering()
        self.steer(steering, tick)
        self.rect.move_ip(self.velocity)
        
class GravityCircleNPC(pai.gameobject.GameObject):
    
    def __init__(self, pos = (0, 0)):
        # First create the circle image with alpha channel to have transparency
        img = pygame.Surface( (10, 10) ).convert_alpha()
        img.fill( WHITE )
        # Draw the circle
        pygame.draw.circle(img, BLACK, (5, 5), 5)
        # Call GameObejct init with appropiate values
        super(GravityCircleNPC, self).__init__(
            img_surf = img,
            pos = pos,
            max_speed = 10,
            max_accel = 40,
            max_rotation = 40,
            max_angular_accel = 30
        )
        # Create a placeholder for the AI
        self.ai = pai.steering.kinematic.NullSteering()
        
    def update(self, tick):
        # Gravity steering
        gravity = pai.steering.kinematic.SteeringOutput()
        gravity.linear[1] = 300 # This value is arbitrary, it just works
        
        # Steer only along x axis
        steering = self.ai.get_steering()
        self.steer_x(steering, tick)
        
        # Get total velocity considering gravity
        velocity = self.velocity + gravity.linear * tick
        
        # Move with that velocity
        self.rect.move_ip(velocity)
        
class PathCosine(pai.steering.path.Path):
    
    def __init__(self, start, height, length):
        
        self.start = start
        self.height = height
        self.length = length
        
        def cosine_path(self, x):
            y = self.start[1] + math.cos(x) * self.height
            return x, y
        
        super(PathCosine, self).__init__(
            path_func = cosine_path,
            domain_start = int(self.start[0]),
            domain_end = int(self.start[0] + length),
            increment = 30
        )
        
    
def main():
    # Create screen
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('PyGame AI Guide')
    
    # Create white background
    background = pygame.Surface((screen_width, screen_height)).convert()
    background.fill((255, 255, 255))
    
    # Initialize clock
    clock = pygame.time.Clock()
    
    # Variables that you will use in your game loop
    # Create player steering
    player_steering = pai.steering.kinematic.SteeringOutput()
    
    # Entities afected by gravity
    gravity_entities = []
    
    # Instantiate game objects
    player = Player(pos = (screen_width//2, screen_height//2))
    circle = CircleNPC(pos = (screen_width//4, screen_height//2))
    circle2 = CircleNPC(pos = (screen_width//5, screen_height//2))
    circle3 = GravityCircleNPC(pos = (screen_width//6, screen_height//2))
    
    # Remember to add it to our gravity_entitites list for collision
    gravity_entities.append(circle3)
    
    # Set the NPC AI
    circle.ai = pai.steering.kinematic.Arrive(circle, player)
    path_cosine = PathCosine(
        start = circle2.position,
        height = 200,
        length = 500
    )
    circle2.ai = pai.steering.kinematic.FollowPath(circle2, path_cosine)
    circle3.ai = pai.steering.kinematic.Seek(circle3, player)
    
    # Create drag
    drag = pai.steering.kinematic.Drag(15)
    
    # Game loop
    while True:
        
        # Get loop time, convert milliseconds to seconds
        tick = clock.tick(60)/1000
        
        # Restart player steering
        player_steering.reset()
        
        # Handle input
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(2)
        
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            player_steering.linear[1] -= player.max_accel
        if keys[K_a]:
            player_steering.linear[0] -= player.max_accel
        if keys[K_s]:
            player_steering.linear[1] += player.max_accel
        if keys[K_d]:
            player_steering.linear[0] += player.max_accel
            
        
        # Erease previous frame by bliting background
        screen.blit(background, background.get_rect())
        
        # Update player and NPCs
        player.update(player_steering, tick)
        circle.update(tick)
        circle2.update(tick)
        circle3.update(tick)
        
        # Check if our gravity-affected entities are falling off-screen
        for gentity in gravity_entities:
            if gentity.rect.bottom > screen_height:
                gentity.rect.bottom = screen_height
        
        # Apply drag
        player.steer(drag.get_steering(player), tick)
        circle.steer(drag.get_steering(circle), tick)
        circle2.steer(drag.get_steering(circle2), tick)
        circle3.steer(drag.get_steering(circle3), tick)
        
        # Blit all your entities
        screen.blit(player.image, player.rect)
        screen.blit(circle.image, circle.rect)
        screen.blit(circle2.image, circle2.rect)
        screen.blit(circle3.image, circle3.rect)
        
        pygame.display.update()
                
if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()

    

