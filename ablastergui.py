import pygame
# Color Constants
BLACK = (0,0,0)
WHITE = (255, 255, 255)
TRANSPARENT = (255,255,254)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

def loadImage(name, useColorKey = False):
    image = pygame.image.load(name)
    image = image.convert()

    if useColorKey:
        colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey)

    return image
        
class dLabel(pygame.sprite.Sprite):
    def __init__(self, x, y, size = 20, color = BLACK, font="bankgothic"):
        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.SysFont(font, size)
        self.text = "Hello World!"
        self.x = x
        self.y = y
        self.color = color
        self.image = self.font.render(self.text, 1, self.color)
        self.rect = self.image.get_rect()

        print " debug: create lable:  text, x, y = ", self.text, self.x, self.y

    def update(self, screen):
        self.image = self.font.render(self.text, 1, self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y







class Label(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.SysFont("bankgothic", 20)
        self.text = "Hello World!"
        self.x = x
        self.y = y

        self.image = self.font.render(self.text, 1, BLACK)
        self.rect = self.image.get_rect()

        print " debug: create lable:  text, x, y = ", self.text, self.x, self.y

    def update(self, screen):
        self.image = self.font.render(self.text, 1, BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y



class woodyLabel(pygame.sprite.Sprite):
    def __init__(self, text, position):
        pygame.sprite.Sprite.__init__(self)
        # position
        self.pos = position
        
        # font object to render the text
        self.font = pygame.font.SysFont("Impact", 16)
        
        # some way of updating the image with the text we're saving
        self.updateText(text)

    def update(self, screen):
        pass

    def notify(self, event):
        pass

    def updateText(self, text):
        self.image = self.font.render(text, 1, (0,0,0) )
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos


class Button(pygame.sprite.Sprite):
    def __init__(self, image, event, pos = (150, 150) ):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = loadImage(image).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.event = event

    def update(self, screen):
        pass

    def notify(self, event):
        pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(pos):
                # they've clicked me!!!!!
                pygame.event.post(self.event)
            
        
        

















