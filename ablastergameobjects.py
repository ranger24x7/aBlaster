import pygame

# Global constants

# Screen constants
SCREENX = 1024
SCREENY = 768
FRAMERATE = 60

STANDING = "standing"
RUNNING = "running"
JUMPING = "jumping"
FALLING = "falling"
FLYING = "flying"
THRUSTING = "thrusting"


DEBUG = True    # enables inline debug and print messages
SOUND = True    # turns on or off sound


# Color Constants
BLACK = (0,0,0)
WHITE = (255, 255, 255)
TRANSPARENT = (255,255,254)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Environment
GRAVITY = .15


#Overall game state modes
STOPPED = 0
MAINMENU = 1
GAMERUNNING = 2
SCOREBOARD = 3
STATE = MAINMENU

#####################################
#########  End of Constants    ######
#####################################

# wall class
class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, size = (25, 200)):
        pygame.sprite.Sprite.__init__(self)
        


        self.image = pygame.Surface(size).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.image.fill(BLUE)        

    def update(self, screen):
        pass

    def notify(self, event):
        pass


# player class

### THE THING I FORGOT IN CLASS!!!!

# The thing I forgot was to pass the terrain sprite group to the player class.
# the player class needs to be able to see it so they can compare against it.
# another option would be to make the sprite groups global within gameobjects.py
# Your choice. I suggest just passing and remembering.  
class Player(pygame.sprite.Sprite):
    def __init__(self, terrain, pos, size = (25, 25)):    # pos = (100, 100)
        pygame.sprite.Sprite.__init__(self)

        # image, rect
        # x, y
        # dx, dy
        # speed, maxSpeed
        # jumpHeight

        # the terrain sprite group

        self.terrain = terrain  # <-------- This is needed for later so it can
                                #           compare itself against things it can hit
        
        self.image = pygame.Surface(size).convert()
        self.rect = self.image.get_rect()

        self.x = pos[0]
        self.y = pos[1]

        self.dx = 0
        self.dy = 0

        self.speed = .25
        self.maxSpeed = 5
        self.jumpHeight = 8
                

        # state (standing, running, jumping, falling)
        self.state = FALLING


    def update(self, screen):
        # move the player
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.dx -= self.speed
            if self.dx < -self.maxSpeed:
                self.dx = -self.maxSpeed
            if self.state == STANDING:
                self.state = RUNNING

        if keys[pygame.K_d]:
            self.dx += self.speed
            if self.dx > self.maxSpeed:
                self.dx = self.maxSpeed
            if self.state == STANDING:
                self.state = RUNNING

        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            if self.state == RUNNING:
                self.state = STANDING

                if self.dx < -.1:
                    self.dx += self.speed
                elif self.dx > .1:
                    self.dx -= self.speed
                else:
                    self.dx = 0

        if keys[pygame.K_SPACE]:
            if (self.state == STANDING or self.state == RUNNING):
                self.dy = - self.jumpHeight
                self.state = JUMPING


        self.dy += GRAVITY

        # move the player, check for collisions each step
        self.x += self.dx
        self.rect.centerx = self.x
        for terrain in self.terrain.sprites():
            if self.rect.colliderect(terrain.rect):
                if self.dx > 0:
                    self.rect.right = terrain.rect.left
                    self.x = float(self.rect.centerx)
                    self.dx = 0
                else:
                    self.rect.left = terrain.rect.right
                    self.x = float(self.rect.centerx)
                    self.dx = 0

                    
        self.y += self.dy
        self.rect.centery = self.y
        for terrain in self.terrain.sprites():
            if self.rect.colliderect(terrain.rect):
                if self.dy > 0:
                    self.rect.bottom = terrain.rect.top
                    self.y = float(self.rect.centery)
                    self.dy = 0
                    if self.state == FALLING:
                        self.state = STANDING
                else:
                    self.rect.top = terrain.rect.bottom
                    self.y = float(self.rect.centery)
                    self.dy = 0
                    
        if self.dy > 0:                 # this was a tricky one.  Collisions aren't detected until it's moved past .5
            if self.state == JUMPING:   # so the first two ticks you'll be falling with dy but not detect if 
                self.state = FALLING    # you were standing on the ground. Therefore, to prevent it screwing up the state
            if self.dy > .5:            # every 3 ticks (and thus the animation) it checks this in 2 ways.  If we were jumping
                self.state = FALLING    # and reached the apex of the jump then it flips immediately.  If we just walked off a
                                        # cliff it'll take a few frames to detect it
                            
                        


                
        # check for collisions
        

    def notify(self, event):
        pass
    






















             
