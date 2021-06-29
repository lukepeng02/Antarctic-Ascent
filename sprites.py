import pygame, random
from constants import width, height

class MainCharacter(pygame.sprite.Sprite):
    """The penguin sprite for the player"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("penguin.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 54))

        self.rect = self.image.get_rect()
        self.rect.center = (200, 300)

        self.score = 0
        self.boosting = False

class Jump_Platform(pygame.sprite.Sprite):
    """The stationary grass-and-dirt platform"""
    def __init__(self, x_center, y_center):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("platform.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 12))

        self.rect = self.image.get_rect()
        self.rect.center = (x_center, y_center)

        self.trampoline = None
        if random.randint(1, 10) == 1:
            self.tram_x = x_center + random.randint(-30, 30)
            self.tram_y = self.rect.top
            self.trampoline = Trampoline(self.tram_x, self.tram_y)

class Moving_Platform(pygame.sprite.Sprite):
    """Moving stone platforms"""
    max_left = 0
    max_right = width
    def __init__(self, max_l, max_r, y_bottom):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("stone.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 12))
    
        self.rect = self.image.get_rect()
        x_center = random.randint(max_l + 40, max_r - 40)
        self.rect.center = (x_center, y_bottom - 6)

        self.max_left = max_l
        self.max_right = max_r
        self.speed = 2

        self.trampoline = None
        if random.randint(1, 10) == 1:
            self.tram_x = x_center + random.randint(-30, 30)
            self.tram_y = self.rect.top
            self.trampoline = Trampoline(self.tram_x, self.tram_y)

    def update(self):
        """Move the platform"""
        self.rect = self.rect.move([self.speed, 0])
        if self.trampoline is not None:
            self.trampoline.rect = self.trampoline.rect.move([self.speed, 0])
        if self.rect.left <= self.max_left:
            self.speed = 2
        if self.rect.right >= self.max_right:
            self.speed = -2

class Cloud_Platform(pygame.sprite.Sprite):
    """Cloud platforms that disappear after bouncing on them"""
    def __init__(self, x_center, y_center):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("cloud.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 12))

        self.rect = self.image.get_rect()
        self.rect.center = (x_center, y_center)

        self.trampoline = None

class Bottom_Platform(pygame.sprite.Sprite):
    """The bottom platform that ensures the player does not lose instantly"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("bricks.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, 40))

        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height - 20)

        self.trampoline = None

class Trampoline(pygame.sprite.Sprite):
    """The trampoline that lets the player bounce super high"""
    def __init__(self, x_center, y_bottom):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("trampoline.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 12))

        self.rect = self.image.get_rect()
        self.rect.centerx = x_center
        self.rect.bottom = y_bottom

class Seal(pygame.sprite.Sprite):
    """The enemy that ends the game when touched"""
    def __init__(self, x_center, y_center):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("seal.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 36))

        self.rect = self.image.get_rect()
        self.rect.center = (x_center, y_center)

class Icicle(pygame.sprite.Sprite):
    """Used to kill enemies"""
    def __init__(self, x_center, y_bottom):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("icicle.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (10, 20))

        self.rect = self.image.get_rect()
        self.rect.center = (x_center, y_bottom - 10)

        self.speed = [0, -8]

    def update(self):
        """Move the icicle"""
        self.rect = self.rect.move(self.speed)
        if self.rect.bottom < 0:
            self.kill()
