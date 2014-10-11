import os, pygame
from random import randint, uniform
from functions import *

#classes for game objects

class Tree(pygame.sprite.Sprite):
    def __init__(self, loc):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('physicstree.png', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 700
        self.accel = .3
        self.yspeed = 0.0
        self.hspeed = 0.0
        self.rect = self.rect.move(loc * 150, randint(10, 850))
        self.damager = 2

    def update(self):
        if self.rect.bottom == self.area.bottom:
            if self.yspeed < 0:
                self.rect = self.rect.move((0, self.yspeed))
            elif self.yspeed == 0:    
                self.damager = 2
        elif self.rect.bottom > self.area.bottom:
            self.damager = 2
            self.rect = self.rect.move((0, self.area.bottom - self.rect.bottom))
            if self.yspeed > 2:
                self.yspeed = -self.yspeed / 2
            else:
                self.yspeed = 0.0
        else:
            self.yspeed += self.accel
            self.rect = self.rect.move((0, self.yspeed))

    def jump(self):
        if self.rect.bottom == self.area.bottom:
            self.yspeed = -20
        
class Smasher(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('looking n0000.bmp', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 100, 700
        self.hmove = 0.0
        self.vmove = 0.0
        self.topspeed = 20.0
        self.friction = .05
        self.score = 0
        self.aih = 1    #AI movement
        self.aiv = -1
        
    def update(self):
        "walk or spin, depending on the monkeys state"
        self._walk()

    def show_score(self, background, change):
        font = pygame.font.Font(None, 42)
        text = font.render("Ogre score: " + str(self.score), 1, (10, 200, 10))
        textpos = text.get_rect(centerx=background.get_width()/3 - 30, centery=15)
        background.blit(text, textpos)
        self.score += change
        font = pygame.font.Font(None, 42)
        text = font.render("Ogre score: " + str(self.score), 1, (220, 220, 220))
        textpos = text.get_rect(centerx=background.get_width()/3 - 30, centery=15)
        background.blit(text, textpos)
        
    def _walk(self):
        "move the monkey across the screen, and turn at the ends"
        "limit speed"
        if self.hmove > self.topspeed:
            self.hmove = self.topspeed
        elif self.hmove < -self.topspeed:
            self.hmove = -self.topspeed
        if self.vmove > self.topspeed:
            self.vmove = self.topspeed
        elif self.vmove < -self.topspeed:
            self.vmove = -self.topspeed

        if self.hmove > self.friction:
            self.hmove -= self.friction
        elif self.hmove < -self.friction:
            self.hmove += self.friction
        if self.vmove > self.friction:
            self.vmove -= self.friction
        elif self.vmove < -self.friction:
            self.vmove += self.friction
            
        newpos = self.rect.move((self.hmove, self.vmove))
        if (self.rect.left < self.area.left and self.hmove < 0) or \
           (self.rect.right > self.area.right and self.hmove > 0):
            self.hmove = -self.hmove
            newpos = self.rect.move((self.hmove, self.vmove))
            self.image = pygame.transform.flip(self.image, 1, 0)
        if (self.rect.top < self.area.top and self.vmove < 0) or \
           (self.rect.bottom > self.area.bottom and self.vmove > 0):
            self.vmove = -self.vmove
            newpos = self.rect.move((self.hmove, self.vmove))
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect = newpos
        
class Dino(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('attack n0006.bmp', -1)
        self.punching = 0
        self.score = 0

    def update(self):
        "move the fist based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5, 10)

    def show_score(self, background, change):
        font = pygame.font.Font(None, 42)
        text = font.render("Dino score: " + str(self.score), 1, (10, 200, 10))
        textpos = text.get_rect(centerx=background.get_width()/1.5 + 30, centery=15)
        background.blit(text, textpos)
        self.score += change
        font = pygame.font.Font(None, 42)
        text = font.render("Dino score: " + str(self.score), 1, (220, 220, 220))
        textpos = text.get_rect(centerx=background.get_width()/1.5 + 30, centery=15)
        background.blit(text, textpos)

class Bear(pygame.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('bear.bmp', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move = 9
        self.dizzy = 0
        self.hv = randint(0, 1)
        self.rect = self.rect.move(randint(10, 1550), randint(10, 850))

    def update(self):
        "walk or spin, depending on the monkeys state"
        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def _walk(self):
        "move the monkey across the screen, and turn at the ends"
        newpos = self.rect.move((self.move * self.hv, self.move *(1 - self.hv)))
        if self.rect.top < self.area.top or \
           self.rect.bottom > self.area.bottom or \
           self.rect.left < self.area.left or \
           self.rect.right > self.area.right:
            self.move = -self.move
            newpos = self.rect.move((self.move * self.hv, self.move *(1 - self.hv)))
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect = newpos

    def kill(self):
        pygame.sprite.Sprite.kill(self)
