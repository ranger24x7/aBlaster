"""
    Program:        Asteroid Blaster
    Description:    Gather points as you fly and shoot!
    Name:           David Baker
    Class:          CIS151
    Date:           2014-12-14
    Credits:        framework from Game Programming, Andy Harris
    Credits:        based on in-class examples and homework framework by Prof. Woodward-Roth
    Files:          astroidblaster-r34c-dwbaker.py

"""
#   r35

"""
Asteroid Blaster is a programming project associated with CIS 151 programming class in the fall of 2014.  As our
final project and to build on some of the concepts demonstrated in class, I wanted to explore a number of techniques in Python and Pygame:

collision processing - we've used this in several previous games, but I wanted to explore this further with ships, bullets, and asteroids.
Game-level considerations come into play here... should bullets trigger explosions, or the objects they collide with?  (I did a bit of both!)

list processing - Python has a number of facilities built in for parsing lists and dealing with tuples. I used a list of typed
objects to pass a payload of various items from the powerUps to the ships who sucessfully collide with them

sprite animation - I used my handdrawn ship sprite animations from a previous assignment and tied it to fuel level in this game.

Side scrolling - I worked out the basics of how to slide a background (currently) an image over a background to achieve a sense of sideways motion.

default parameters - we saw this in class, so I wanted to try it out.  Implemented in the "dLable" class, I learned how to use defaults to allow the original
calls to create labels remain unchanged, but newer ones to provide additional values and gain control over text size, color and font if desired.  Nice feature.

The program currently has a ship that moves with keyboard controls, correctly maintains and consumes an inventory of weapons, properly accepts
a number of benefits from powerUps, correctly consumes fuel and bullets, delivers and receives damage, decrements lives, and changes animation based on fuel level.
powerUps come at fixed speeds, but asteroids have variable speeds.   There is, of course, a lot of cool stuff yet to do, but I had fun with
a good start on this game.


coming up: (implementation plan)
        [done] implement the ship
        [done] get one kind of bullet in flight forever
        [done] modify the bullet to self destruct at edges
        [done] get restricted ship motion going
        [done] get initial power ups coming across screen
        [done] add bullet/powerup collision and destruction
        [done] add powerup collision with ship and deliver value
        [done] start sending points up
        [done] create NPC generator
        [done] create random powerUps in the game
        [done] get the background scrolling
        [done] modify weapon use to consume from the weapons rack and use consumables
        [done] basic asteroids generate and deliver wallop
        [done] asteroids that can be destroyed and/or damage the ship
        [done] add a welcome splashscreen
        [done] scoreboard that shows what's going on
        [done] ship that can be destroyed and lives decremented,
        [done] ship that has some type of explosion, regenerated,
        some type of game over detect logic... lives related
        
        
        

Game objectives
1.  [done] implement the ship, and get motion working
2.  [done] Get the points system working... start simple, then try the event system
3.  [done] add some power-ups with the right motion
4.  [done] add some benefits to the power-ups and see that they trigger the right events
5.  [done] add some asteroids to avoid
6.  [done] add a 30sec timer for each level, and put up a countdown timer and points for staying alive!
7.  optional - add a terrain generator
8.  optional add additional weapons



"""


##
## Here is how you grab a pixel for color key transparency
##
## color = image.get_at((0,0)) #we get the color of the upper-left corner pixel
## image.set_colorkey(color)
##
##

# Global constants

# Screen constants
SCREENX = 1024
SCREENY = 768
##SCREENX = 1280
##SCREENY = 720
FRAMERATE = 60

STANDING = "standing"
RUNNING = "running"
JUMPING = "jumping"
FALLING = "falling"
FLYING = "flying"
THRUSTING = "thrusting"

# game play
EASY = "easy"
MEDIUM = "medium"
HARD = "hard"

DEBUG = False    # enables inline debug and print messages
SOUND = True    # turns on or off sound


# Color Constants
BLACK = (0,0,0)
WHITE = (255, 255, 255)
TRANSPARENT = (255,255,254)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# size of powerups in pixels
POWERUPDIA = 15

# Environment
GRAVITY = .15


#Overall game state modes
EXITGAME = 0
MAINMENU = 1
GAMERUNNING = 2
SCOREBOARD = 3
STATE = MAINMENU
HOWFAR = 0.15   # % how far to move across the screen each second
GAMESPEED = (SCREENX/float(FRAMERATE)) * HOWFAR  # number of pixels to move each update

# wanted to, but could not do the following... python must find definitions as it processes downward
#GAMESPEED = SCREENX * perSecond(HOWFAR)  # number of pixels to move each update

#####################################
#########  End of Constants    ######
#####################################

#I - Import and initalise
import pygame
#pygame.init()
from ablastergui import *
from ablastergameobjects import *
import math
import random
from random import randint


pygame.init()
screen = pygame.display.set_mode((SCREENX, SCREENY))
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill( (0, 44, 255) )

clock = pygame.time.Clock()


allShips = pygame.sprite.Group()
allBullets = pygame.sprite.Group()  # here's a group for all the bullets
explosions = pygame.sprite.Group()  # and the explosion effects
powerUps = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
GUI = pygame.sprite.Group()         # all the numbers and stats go through here
scrollingLandscape = pygame.sprite.Group()

# =======================================
# =======================================
# === getTheta()

# This is a function I made for you to help quickly convert compass angles to radians.  Whenever
# you need to get theta you can just do:
#   theta = getTheta(your_direction)
# replacing your_direction with the direction/angle you are facing.
def getTheta(angle):
    return angle * math.pi/180

# =======================================
# =======================================
# === getCoords()

# This is a helper function to deal with variable screen sizes
# supply tuple with xpercent and ypercent in whole integers (0-100%)
# returned will be a tuple with x and y screen coordinates for
# this particular screen size
# Gives similar relative coordinates per axis, but won't account for aspect ratio changes
def getCoords( (xpercent, ypercent)):
    a = xpercent * SCREENX
    b = ypercent * SCREENY
    return (a, b)


# =======================================
# =======================================
# === perSecond()

# This is a helper function to calculate a per frame amount
# supply a value of change you want every second, and this converts it to a per-frame value
# returned floating value will be the change per frame of the game loop
def perSecond(value):
    return (value/float(FRAMERATE))






# =======================================
# =======================================
# === Pew Pew Bullet class


""" These bullets can have color and mass, and get their initial starting spots from the
ship that fired them.  They have a sound when created.  Once inflight, they continue until
they hit an object, go off the screen, or deplete their range.
Bullets have wallop (damage they inflict).  They self-destruct collide with another object.
The collision routines determine what else happens at the collision, and
can decide to play a sound during collision.
"""

# for initial efforts pewPew bullets will be red, and will have zero mass

class PewPewBullet(pygame.sprite.Sprite):
    def __init__(self, ship):            # A ship can generate a bullet and set it's flight path
        pygame.sprite.Sprite.__init__(self)

# constant for speed of pewPew bullets
        LAUNCHVELOCITY = 15  # this is the speed in excess of ship
        self.timeToLive = 120  # frames before disappearing

        self.wallop = 10    # amount of damage delivered

# define the starting image (a small round cannonball)
        self.image = pygame.Surface((10,10))
        self.image.fill((0xff, 0xff, 0xfe))   # almost black
        self.image.set_colorkey((0xff, 0xff, 0xfe)) # set transparency
        pygame.draw.circle(self.image, (0xff,0,0), (5,5), 5) # red circle
        self.rect = self.image.get_rect()

# set the starting location direction and velocity
        self.x = ship.x
        self.y = ship.y
        self.dx = 0
        self.dy = 0
        self.rect.center = ship.rect.center  #does this work?
#        self.rect.center = (ship.x, ship.y)  #wonder if I could have used ship.rect.center?
        self.direction = ship.direction
        self.acceleration = ship.speed + LAUNCHVELOCITY

#  Do a little math here to determine the bullet's speed based on direction
        self.setSpeed()   # get the speed of the bullet set
        self.x += self.dx * 2  # jump a bit ahead of the ship... avoid instant collision
        self.y += self.dy * 2

        self.mass = 0.0     # start with weightless bullets

# make a "fired" sound

        if SOUND == True:
            if not pygame.mixer:
                print "there is a problem with sound"
            else:
                pygame.mixer.init()
                self.sndFired = pygame.mixer.Sound("pewPewFired.ogg")
                self.sndFired.play()    # blast away!


    # -----------------------------------------------
    def update(self):
        # Standard update-every tick.

        self.x += self.dx
        self.y += self.dy
        self.rect.center = (self.x, self.y) # CRITICAL LINE... MUST HAVE THIS

# check to see if this bullet continues to exist
        self.timeToLive -= 1
        if self.timeToLive <= 0:
            self.kill()

# add edge checking.  In this game, once this bullet leaves the screeen without
# hitting anything, it self destructs

        if self.rect.centery >= SCREENY: #flying off the bottom
            self.kill()
        elif self.rect.centery < 0:  #flying off the top
            self.kill()

        #handle right and left
        if self.rect.centerx >= SCREENX: #flying off the right side
            self.kill()
        elif self.rect.centerx < 0:  #flying off the left side
            self.kill()

# look for collisions
# here's the fun stuff... see where a bullet (any bullet) intersects with another object
# and explode and deliver a wallop.  For now, we've set things such that one hit
# destroys a powerup, due to the wallop of a single bullet

# hit a ship
        collisions = pygame.sprite.spritecollide(self, allShips, False)
#        print collisions
        if collisions:
            for victim in collisions:
                victim.hitpoints -= self.wallop

                for a in range(20):
                    explosion = Explosion(self)
                    explosions.add(explosion)

                self.kill()

# hit a asteroid
        collisions = pygame.sprite.spritecollide(self, asteroids, False)
#        print collisions
        if collisions:
            for victim in collisions:
                victim.hitpoints -= self.wallop
                self.kill()

# hit a powerUp
        collisions = pygame.sprite.spritecollide(self, powerUps, False)
#        print collisions
        if collisions:
            for victimpowerUp in collisions:
#                victim.hitpoints -= self.wallop  # we could deliver a wallop to a powerUp, but instead, let's just wipe it out
                victimpowerUp.kill()      # doesn't take much to kill a power up

                for a in range(20):
                    explosion = Explosion(self)
                    explosions.add(explosion)

                self.kill()

                
    def setSpeed(self):
        theta = getTheta(self.direction)
        ddx = self.acceleration * math.cos(theta)
        ddy = self.acceleration * math.sin(theta)
        ddy *= -1
        self.dx += ddx
        self.dy += ddy

        self.speed = math.sqrt(( self.dx * self.dx) + (self.dy * self.dy))



# =======================================
# =========== end of PewPewBullet class =========
# =======================================




# =======================================
# =======================================
# === Banana class


""" These bullets can have color and mass, and get their initial starting spots from the
ship that fired them.  They have a sound when created.  Once inflight, they continue until
they hit an object, go off the screen, or deplete their range.
Bullets have wallop (damage they inflict).  They self-destruct collide with another object.
The collision routines determine what else happens at the collision, and
can decide to play a sound during collision.
"""

# for initial efforts pewPew bullets will be red, and will have zero mass

class bananaBullet(pygame.sprite.Sprite):
    def __init__(self, ship):            # A ship can generate a bullet and set it's flight path
        pygame.sprite.Sprite.__init__(self)

# constant for speed of pewPew bullets
        LAUNCHVELOCITY = 15  # this is the speed in excess of ship
        self.timeToLive = 120  # frames before disappearing

        self.wallop = 20    # amount of damage delivered

# define the starting image (a small round cannonball)
        self.image = pygame.Surface((10,10))
        self.image.fill((0xff, 0xff, 0xfe))   # almost black
        self.image.set_colorkey((0xff, 0xff, 0xfe)) # set transparency
        pygame.draw.circle(self.image, (0xff,0xff,0), (5,5), 5) # some other color
        self.rect = self.image.get_rect()

# set the starting location direction and velocity
        self.x = ship.x
        self.y = ship.y
        self.dx = 0
        self.dy = 0
        self.rect.center = ship.rect.center  #does this work?
#        self.rect.center = (ship.x, ship.y)  #wonder if I could have used ship.rect.center?
        self.direction = ship.direction
        self.acceleration = ship.speed + LAUNCHVELOCITY

#  Establish initial rotation
        self.rotationAngle = 0
        self.rotationSpeed = perSecond(20)   #rotate at this freqency
        
#  Do a little math here to determine the bullet's speed based on direction
        self.setSpeed()   # get the speed of the bullet set
        self.x += self.dx * 2  # jump a bit ahead of the ship... avoid instant collision
        self.y += self.dy * 2

        self.mass = 0.0     # start with weightless bullets

# make a "fired" sound

        if SOUND == True:
            if not pygame.mixer:
                print "there is a problem with sound"
            else:
                pygame.mixer.init()
                self.sndFired = pygame.mixer.Sound("pewPewFired.ogg")
                self.sndFired.play()    # blast away!


    # -----------------------------------------------
    def update(self):
        # Standard update-every tick.

        self.x += self.dx
        self.y += self.dy
        self.rect.center = (self.x, self.y) # CRITICAL LINE... MUST HAVE THIS

# check to see if this bullet continues to exist
        self.timeToLive -= 1
        if self.timeToLive <= 0:
            self.kill()

# add edge checking.  In this game, once this bullet leaves the screeen without
# hitting anything, it self destructs

        if self.rect.centery >= SCREENY: #flying off the bottom
            self.kill()
        elif self.rect.centery < 0:  #flying off the top
            self.kill()

        #handle right and left
        if self.rect.centerx >= SCREENX: #flying off the right side
            self.kill()
        elif self.rect.centerx < 0:  #flying off the left side
            self.kill()


# rotate your image
        # self.rotationAngle = self.rotationAngle + self.rotationAnglespeed
        # do I pass angle, or theta?
        # redraw your image, now rotated by this new absolute


        
# look for collisions
# here's the fun stuff... see where a bullet (any bullet) intersects with another object
# and explode and deliver a wallop.  For now, we've set things such that one hit
# destroys a powerup, due to the wallop of a single bullet

# hit a ship
        collisions = pygame.sprite.spritecollide(self, allShips, False)
#        print collisions
        if collisions:
            for victim in collisions:
                victim.hitpoints -= self.wallop

                for a in range(20):
                    explosion = Explosion(self)
                    explosions.add(explosion)

                self.kill()

# hit a asteroid
        collisions = pygame.sprite.spritecollide(self, asteroids, False)
#        print collisions
        if collisions:
            for victim in collisions:
                victim.hitpoints -= self.wallop
                self.kill()

# hit a powerUp
        collisions = pygame.sprite.spritecollide(self, powerUps, False)
#        print collisions
        if collisions:
            for victimpowerUp in collisions:
#                victim.hitpoints -= self.wallop  # we could deliver a wallop to a powerUp, but instead, let's just wipe it out
                victimpowerUp.kill()      # doesn't take much to kill a power up

                for a in range(20):
                    explosion = Explosion(self)
                    explosions.add(explosion)

                self.kill()

                
    def setSpeed(self):
        theta = getTheta(self.direction)
        ddx = self.acceleration * math.cos(theta)
        ddy = self.acceleration * math.sin(theta)
        ddy *= -1
        self.dx += ddx
        self.dy += ddy

        self.speed = math.sqrt(( self.dx * self.dx) + (self.dy * self.dy))



# =======================================
# =========== end of bananaBullet class =========
# =======================================






# =======================================
# =======================================
# === Explosion class
# === from Prof. Woodward-Roth's class examples


class Explosion(pygame.sprite.Sprite):
    def __init__(self, parent):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((4, 4)).convert()
        self.image.fill(WHITE)
        pygame.draw.circle(self.image, YELLOW, (2,2), 2)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

        self.x = parent.x
        self.y = parent.y
        self.dx = 0
        self.dy = 0
        self.direction = randint(0,360)
        self.acceleration = randint(1, 8)
        self.timeToLive = 60
        self.setSpeed()


    def update(self):
        self.x += self.dx
        self.y += self.dy

        self.rect.center = (self.x, self.y)

        self.timeToLive -= 1

        if self.timeToLive <= 0:
            self.kill()
        return


    def setSpeed(self):
        theta = getTheta(self.direction)
        ddx = self.acceleration * math.cos(theta)
        ddy = self.acceleration * math.sin(theta)
        ddy *= -1
        self.dx += ddx
        self.dy += ddy


# =======================================
# =========== end of Explosion class =========
# =======================================



# =======================================
# =======================================
# === Ship Explosion class
# === from Prof. Woodward-Roth's class examples


class shipExplosion(pygame.sprite.Sprite):
    def __init__(self, parent):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((16, 16)).convert()
        self.image.fill(WHITE)
        pygame.draw.circle(self.image, RED, (8,8), 8)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

        self.x = parent.x
        self.y = parent.y
        self.dx = 0
        self.dy = 0
        self.direction = randint(0,360)
        self.acceleration = randint(1, 8)
        self.timeToLive = 90
        self.setSpeed()


    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (self.x, self.y)
        self.timeToLive -= 1
        if self.timeToLive <= 0:
            self.kill()
        return


    def setSpeed(self):
        theta = getTheta(self.direction)
        ddx = self.acceleration * math.cos(theta)
        ddy = self.acceleration * math.sin(theta)
        ddy *= -1
        self.dx += ddx
        self.dy += ddy


# =======================================
# =========== end of shipExplosion class =========
# =======================================



# =======================================
# =======================================
# === Power Up class
# === ===================================

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,30))
        self.image.fill(TRANSPARENT)
        self.image.set_colorkey(TRANSPARENT)
        pygame.draw.circle(self.image, GREEN, (15,15), POWERUPDIA, 0)
        self.rect = self.image.get_rect()

# generate a random starting position along the right side
        self.rect.centerx = SCREENX
        self.rect.centery = random.randrange(25, SCREENY-100)

        self.dx = -GAMESPEED

# generate a payload (fixed here... in the future, this could be random mix of weapons, fuel, points, lives
#        self.payload = ( ("weapon", "pew-pew gun", 20), ("fuel", 40), ("points", 2000), ("lives", 1) )
        self.payload = ( ("weapon", "pew-pew gun", 20), ("fuel", 40), ("points", 2000), ("health", 10) )
        

    def update(self):
        self.rect.centerx += self.dx


# if you reach the left side without collision, then disappear
        if self.rect.left <= 0:
            self.kill()


# delivery collisions
        collisions = pygame.sprite.spritecollide(self, allShips, False)
#        print collisions
        if collisions:
#Debug
#            print "powerUp payload:", self.payload
            for recipient in collisions:
                for item in self.payload:
                    if item[0] == "weapon":
                        weapon = (item[1], item[2])
                        recipient.weaponsrack.append(weapon)
                    elif item[0] == "fuel":
                        recipient.fuel += item[1]
                        if recipient.fuel > 100:
                            recipient.fuel = 100
                    elif item[0] == "points":
                        recipient.points += item[1]
                    elif item[0] == "health":
                        recipient.hitpoints += item[1]
                    elif item[0] == "lives":
                        recipient.lives += item[1]
#Debug
                print "Ship %d %s: %.2f hit points, %.2f fuel %d lives %d points" % (recipient.shipNumber, recipient.state, recipient.hitpoints, recipient.fuel, recipient.lives, recipient.points)
                print "Ship %d: Weapons: %s" % (recipient.shipNumber, recipient.weaponsrack)
                self.kill()




# =======================================
# =========== end of PowerUp class =========
# =======================================


# =======================================
# =======================================
# === Asteroid class
# === ===================================

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

# debug - this was just a red circle for the asteroid
##        self.image = pygame.Surface((30,30))
##        self.image.fill(TRANSPARENT)
##        self.image.set_colorkey(TRANSPARENT)
##        pygame.draw.circle(self.image, RED, (15,15), POWERUPDIA, 0)
##        self.rect = self.image.get_rect()
##
# load image
        self.image = pygame.image.load("dwbimg\\asteroid1.jpg")
        self.image = self.image.convert()
        transcolor = self.image.get_at((0,0)) # we snag the color of the upper-left corner pixel
        self.image.set_colorkey(transcolor)   # and make it the transparency color for the sprite
        ##self.image.set_colorkey(BLACK)  # this is the hardcoded version
        self.rect = self.image.get_rect()

# generate a random starting position along the right side
        self.rect.centerx = SCREENX
        self.rect.centery = random.randrange(25, SCREENY-100)
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.dx = -GAMESPEED - random.randrange(0,7)
        self.dy = 0

        self.wallop = 40    # amount of damage delivered
        self.hitpoints = 50  # how much damage I can take


    def update(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        self.x = self.rect.centerx
        self.y = self.rect.centery

# first thing to check... have you been destroyed

        if self.hitpoints <=0:   # something has destroyed you
            for a in range(20):
                explosion = Explosion(self)
                explosions.add(explosion)
            self.kill()

# if you reach the left side without collision, then disappear
        if self.rect.right <= 0:
            self.kill()
            

# delivery collisions
        collisions = pygame.sprite.spritecollide(self, allShips, False)
#        print collisions
        if collisions:
            for victim in collisions:
                victim.hitpoints -= self.wallop

###Debug
###            print "powerUp payload:", self.payload
##            for recipient in collisions:
##                for item in self.payload:
##                    if item[0] == "weapon":
##                        weapon = (item[1], item[2])
##                        recipient.weaponsrack.append(weapon)
##                    elif item[0] == "fuel":
##                        recipient.fuel += item[1]
##                        if recipient.fuel > 100:
##                            recipient.fuel = 100
##                    elif item[0] == "points":
##                        recipient.points += item[1]
##                    elif item[0] == "lives":
##                        recipient.lives += item[1]
###Debug
##                print "Ship %d %s: %.2f hit points, %.2f fuel %d lives %d points" % (recipient.shipNumber, recipient.state, recipient.hitpoints, recipient.fuel, recipient.lives, recipient.points)
##                print "Ship %d: Weapons: %s" % (recipient.shipNumber, recipient.weaponsrack)
                self.kill()




# =======================================
# =========== end of Asteroid class =========
# =======================================




# =======================================
# =======================================
# === Scoreboard class
# === ===================================

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.playerscore = dLabel((SCREENX/2 - 450), 20, 60, BLUE)
        GUI.add(self.playerscore)

        self.timeRemaining = dLabel((SCREENX/2 + 350), 30, 40)
        GUI.add(self.timeRemaining)

        self.livesremaining = dLabel((SCREENX/2 + 350), 60, 40, YELLOW)
        GUI.add(self.livesremaining)

        self.health = dLabel((SCREENX/2 + 125), 30, 40)
        GUI.add(self.health)

        self.fuelLevel = dLabel((SCREENX/2 - 100), 30)
        GUI.add(self.fuelLevel)

        self.weaponName = dLabel((SCREENX/2 - 450), 60)
        GUI.add(self.weaponName)
        
        self.remainingShots = dLabel((SCREENX/2 - 300), 60)
        GUI.add(self.remainingShots)                                


    def update(self, playerShip):
        thisShip = playerShip
# load up the values
        x = math.trunc(thisShip.points/10) * 10  #smooth out the display a bit... the 1s are changing too quickly
        self.playerscore.text = "Score: %d" % x
        self.health.text = "Health: %d" % thisShip.hitpoints
        self.timeRemaining.text = "Time: %d" % thisShip.timeRemaining
        self.livesremaining.text = "Lives: %d" % thisShip.lives
        self.fuelLevel.text = "Fuel: %d" % thisShip.fuel

        if thisShip.weaponsrack:
            self.weaponName.text = thisShip.currentWeaponName
            self.remainingShots.text = "%d" % thisShip.remainingShots
##            y = thisShip.weaponsrack[0]
##            self.weaponName.text = y[0]
##            self.remainingShots.text = "%d" % y[1]
        else:
            self.weaponName.text = "No Weapons left!"
            self.remainingShots.text = "zero"

#debug
#        print "score = ", self.playerscore.text       

# =======================================
# =========== end of Scoreboard class =========
# =======================================




# =======================================
# =======================================
# === Landscape class
# === ===================================

class Landscape(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img\\cityscape.jpg")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.dx = GAMESPEED
        self.reset()

    def update(self):
        self.rect.left -= self.dx
        if self.rect.left <= -700:
            self.reset()

    def reset(self):
        self.rect.left = SCREENX - 30 #just to see what happens


# =======================================
# =========== end of Landscape class =========
# =======================================









# =======================================
# =======================================
# === Ship class
SHIPUPDOWN = 10 #motion of ship in pixels/frame when commanded

class Ship(pygame.sprite.Sprite):
    def __init__(self, shipNum, allBullets):            # Supply ship number and bullets
        pygame.sprite.Sprite.__init__(self)

        global STATE

# load images
        self.baseImage = pygame.image.load("dwbimg\\dwbship_resting.png")
        self.baseImage = self.baseImage.convert()
        self.baseImage.set_colorkey(WHITE)
        self.thrustAnimation = []
        for r in range(3):
            img = pygame.image.load("dwbimg\\dwbship_thrusting%i.png" % r)
            img = img.convert()
            transcolor = img.get_at((0,0)) # we snag the color of the upper-left corner pixel
            img.set_colorkey(transcolor)   # and make it the transparency color for the sprite
##            img.set_colorkey(WHITE)  # the hardcoded way of setting transparency
            self.thrustAnimation.append(img)

# set initial variables
        self.shipNumber = shipNum   # we'll have two ships... 1 and 2
        self.frame = 0
        self.delay = 5
        self.pause = self.delay
        self.state = FLYING
        self.beginninghitpoints = 100      # number of points before this ship is destroyed
        self.hitpoints = self.beginninghitpoints    # start out at full strength
        self.lives = 3          # number of lives before it's game over!
        self.fuel = 75         # amount of fuel on board
        self.fuelburnrate = 4   # burn rate on fuel in units per second
        self.points = 0
        self.timeRemaining = 25
        self.stayalivepoints = 200   # per second
        
# set ship's initial weapons rack
# the weapons rack is a list of all the ship's inventory of weapons.  It consists of
# tuples... the first is a string with the weapon nanme, followed by a integer number of shots
# the weaponrack contains all the weapons, including, at the [0] location, the current weapon being used
# instead of fooling around with the list when counting down the weapon use, we have object variables below
# that deal with this.  later on, in the update section, if we run out shots, we'll discard item [0] from
# the rack and select the next weapon (if any).  Display "no weapon" or similar if the rack is empty

        self.weaponsrack = [("banana gun", 14), ("pew-pew gun", 8),("banana gun", 8) ]
        y = self.weaponsrack[0]
        self.currentWeaponName = y[0]
        self.remainingShots = y[1]
        
# set the ship's starting locations
        if self.shipNumber == 1:
            self.x = SCREENX/10     # somewhere in upper left of screen
            self.y = SCREENY/5
            self.direction = 0  #face right
        elif self.shipNumber == 2:
            self.x = screen.get_width() - 300
            self.y = screen.get_height() - 50
            self.direction = 180    # face left

        self.dx = 0
        self.dy = 0

        self.speed = 0
        self.acceleration = .05
        self.turnRate = 4
        self.mass = 1.0


        self.image = self.baseImage
        self.rect = self.image.get_rect()
#        self.rect.center = (self.x, self.y)



    # -----------------------------------------------
    def update(self):
        global STATE

# first thing... let's see if I'm still ok, or destroyed
        if self.hitpoints <= 0:
            self.sndExplosion = pygame.mixer.Sound("shipExploding.ogg")
            self.sndExplosion.play()    # boom!
            for a in range(40):
                explosion = shipExplosion(self)
                explosions.add(explosion)
            self.hitpoints = self.beginninghitpoints    # reset our health
            self.lives -= 1 #drop our lives by one

# in the future, include some logic if we reach zero lives, we declare ourselves out

# Standard update-every tick.
        self.timeRemaining -= perSecond(1)  # countdown timer
        self.fuel -= perSecond(self.fuelburnrate)
        self.points += perSecond(self.stayalivepoints)
        keys = pygame.key.get_pressed()
# check fuel levels
        if self.fuel <= 0:
            self.state = FALLING
        elif self.fuel > 0:
            self.state = FLYING

# if the weapon rack is empty, load the next weapon if you have one (collected via a power-up)
        if self.currentWeaponName == "None":
            if self.weaponsrack:   # load a weapon if there is one
                y = self.weaponsrack[0]
                self.currentWeaponName = y[0]
                self.remainingShots = y[1]                                    

# check to see which ship you are
        if self.shipNumber == 1:

            if keys[pygame.K_q] or keys[pygame.K_UP]:  # go up
                self.dy = -SHIPUPDOWN
            elif keys[pygame.K_a] or keys[pygame.K_DOWN]:  # go down
                self.dy = SHIPUPDOWN
            else:
                self.dy = 0

            if keys[pygame.K_ESCAPE]:  # look for an exit, work our way out (doubt the main to stopped)
                print "escape detected"
                if STATE == GAMERUNNING:
                    STATE = MAINMENU
                elif STATE == MAINMENU:
                    STATE = EXITGAME
                print "STATE = %d" % STATE
            if keys[pygame.K_SPACE]:  # shooting
##                if self.currentWeaponName == "None":
##                    if self.weaponsrack:   # load a weapon if there is one
##                        y = self.weaponsrack[0]
##                        self.currentWeaponName = y[0]
##                        self.remainingShots = y[1]                        

# Now, fire any loaded weapon
                if self.currentWeaponName == "pew-pew gun":
                    bullet = PewPewBullet(self)
                    allBullets.add(bullet)
                    self.remainingShots -= 1
                elif self.currentWeaponName == "banana gun":
                    bullet = bananaBullet(self)
                    allBullets.add(bullet)
                    self.remainingShots -=1

                
# ok, the weapon has been fired



                if self.remainingShots <= 0 and self.weaponsrack:    #done with this weapon
                    del self.weaponsrack[0]                         # remove the current weapon from the rack
                    if self.weaponsrack:    # load up the new weapon immediately if there is one
                        y = self.weaponsrack[0]
                        self.currentWeaponName = y[0]
                        self.remainingShots = y[1]
                    else:
                        self.currentWeaponName = "None"
                        self.remainingShots = 0
                        #note:  the scoreboard module also detects the empty rack condition and puts up a suitable display

        self.x += self.dx
        self.y += self.dy
        self.rect.center = (self.x, self.y) # CRITICAL LINE... MUST HAVE THIS



# handle ship state and animation
        if (self.state == THRUSTING or self.state == FLYING):
            self.pause -= 1
            if self.pause <= 0:
                self.pause = self.delay
                self.frame += 1
                if self.frame >= len(self.thrustAnimation):
                    self.frame = 0
            self.image = self.thrustAnimation[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
        else:
            self.image = self.baseImage
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)

# finally, edge checking. Clamp to top and bottom
        if self.rect.bottom > SCREENY: #flying into the bottom of the screen
            self.rect.bottom = SCREENY
        elif self.rect.top < 0:  #flying off the top
            self.rect.top = 0  # hold at the top

# =======================================
# =========== end of Ship class =========
# =======================================










def generateNPCs(difficulty):
    global STATE
    global DEBUG
    
# this function is being called at the frame rate, so your calculations for sprite generation should be paced for difficulty
# easy is larger number of powerUps, fewer asteroids
# medium is an even mix
# hard is a few more obstacles, fewer powerUps

    if difficulty == "easy":
        if (random.randrange(0, 1000) < 10):
            powerUps.add(PowerUp())
        if (random.randrange(0, 1000) < 1):
            asteroids.add(Asteroid())

    elif difficulty == "medium":
        if (random.randrange(0, 1000) < 5):
            powerUps.add(PowerUp())
        if (random.randrange(0, 1000) < 5):
            asteroids.add(Asteroid())
            
    elif difficulty == "hard":
        if (random.randrange(0, 1000) < 1):
            powerUps.add(PowerUp())
        if (random.randrange(0, 1000) < 10):
            asteroids.add(Asteroid())








def runMainMenu():
    global STATE

    keepGoing = True

    background = pygame.image.load("dwbimg\\ablasterwelcomesplash.gif")
    background = background.convert()
    screen.blit(background, (0,0))

    event = pygame.event.Event(pygame.USEREVENT, name = "newGameEvent")
    newGameButton = Button("img/buttons/newgame.png", event, (512, 375))



    buttons = pygame.sprite.Group()
    buttons.add(newGameButton)



    while keepGoing:
        clock.tick(FRAMERATE)
        # listen for events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                keepGoing = False
                STATE = STOPPED

            elif event.type == pygame.USEREVENT:
                if event.name == "scoreEvent":
                    print "player %i has scored %i points" % (event.player, event.score)
                if event.name == "aboutEvent":
                    print "They pressed the About button!!!!"
                if event.name == "newGameEvent":
                    STATE = GAMERUNNING
                    keepGoing = False




            sprites = buttons.sprites()
            for sprite in sprites:
                sprite.notify(event)



        # update our objects
        buttons.update(screen)

        # draw our objects
        screen.blit(background, (0,0))
        buttons.draw(screen)
        pygame.display.flip()





def runGameLoop():
    global STATE
    global DEBUG
    keepGoing = True

    background = pygame.image.load("img\\cityscape.jpg")
    background = background.convert()
    screen.blit(background, (0,0))

    terrain = pygame.sprite.Group()


    ship1 = Ship(1, allBullets)
    allShips.add(ship1)
##    if DEBUG == True:          # Why doesnt this debug flag work properly?
##        for a in range(20):
##            powerUps.add(PowerUp())

    scoreboard = Scoreboard()  # create all of the on-screen status info
    landscape = Landscape()    # create a scrolling landscape
    scrollingLandscape.add(landscape)




    while keepGoing:
        clock.tick(FRAMERATE)
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                STATE = EXITGAME

            for sprite in terrain.sprites():
                sprite.notify(event)


# generate any new NPCs
        generateNPCs(MEDIUM)


        # update objects
        terrain.update(screen)
        scrollingLandscape.update()
        allShips.update()
        allBullets.update()
        powerUps.update()
        asteroids.update()
        explosions.update()
        scoreboard.update(ship1)
        GUI.update(screen)

        # draw screen
        screen.blit(background, (0,0))  #wipe the screen
        scrollingLandscape.draw(screen)
        terrain.draw(screen)
        allBullets.draw(screen)
        powerUps.draw(screen)
        asteroids.draw(screen)
        explosions.draw(screen)
        allShips.draw(screen)
        GUI.draw(screen)
        
        pygame.display.flip()




def main():
    global STATE
#D - Display configuration
    pygame.display.set_caption("Asteroid Blasters... Q/A or up/down, space bar to shoot")

    while STATE <> EXITGAME:
        if STATE == MAINMENU:
            runMainMenu()
        elif STATE == GAMERUNNING:
            runGameLoop()

main()
pygame.quit()














