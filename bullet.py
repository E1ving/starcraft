import pygame
import random
from StarCraft import bg_size


class Bullet1(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/bullet1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.right = position
        self.active = False
        self.speed = 12
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True

class Bullet2(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/bullet2.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.right = position
        self.active = False
        self.speed = 18
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True

class Enemy_Bullet1(pygame.sprite.Sprite):
    hurt = 2
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/enemy_bullet1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.right = position
        self.active = False
        self.speed = 4
        self.hurt = Enemy_Bullet1.hurt
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.y += self.speed
        if self.rect.top > bg_size[1]:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        if random.random() < 0.8:
            self.active = True

class Enemy_Bullet2(pygame.sprite.Sprite):
    hurt = 2.5
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/enemy_bullet2.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.right = position
        self.active = False
        self.speed = 3
        self.hurt = Enemy_Bullet2.hurt
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.y += self.speed
        if self.rect.bottom > bg_size[1]:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        if random.random() < 0.5:
            self.active = True