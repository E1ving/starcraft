import pygame


class MyPlane(pygame.sprite.Sprite):
    energy = 20
    def __init__(self, bg_size, init_pos):
        pygame.sprite.Sprite.__init__(self)

        self.images = []
        self.images.extend([pygame.image.load("images/me1.png").convert_alpha(),\
                            pygame.image.load("images/me2.png").convert_alpha()])
        self.night_images = []
        self.night_images.extend([pygame.image.load("images/n_me1.png").convert_alpha(),\
                                  pygame.image.load("images/n_me2.png").convert_alpha()])
        self.ex_images = []
        self.ex_images.extend([pygame.image.load("images/ex_me1.png").convert_alpha(), \
                            pygame.image.load("images/ex_me2.png").convert_alpha()])

        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load("images/me_destroy_1.png").convert_alpha(),\
                                    pygame.image.load("images/me_destroy_2.png").convert_alpha(),\
                                    pygame.image.load("images/me_destroy_3.png").convert_alpha(),\
                                    pygame.image.load("images/me_destroy_4.png").convert_alpha()])
        self.rect = self.images[0].get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.pos = init_pos
        self.rect.left, self.rect.top = init_pos
        self.speed = 10
        self.active = True  # 检测是否存活
        self.mask = pygame.mask.from_surface(self.images[0]) # 将非透明部分标记为mask，这样可以实现完美的碰撞检测
        self.invincible = False
        self.energy = MyPlane.energy

    def reset(self):
        self.rect.left,self.rect.top = self.pos
        self.active = True
        self.invincible = True
        self.energy = MyPlane.energy

    # 移动
    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def moveDown(self):
        if self.rect.bottom < self.height - 50:
            self.rect.bottom += self.speed
        else:
            self.rect.bottom = self.height - 50

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.right += self.speed
        else:
            self.rect.right = self.width
