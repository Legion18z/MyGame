"""Здесь описаны классы являющиеся спрайтами (герои, враги, блоки окружения)"""
import pygame
import random
from scenes import *


class Barriers(pygame.sprite.Sprite):
    # Класс блоков окружения (создающими основу карты, препятствия, корридоры и пр.)
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32))
        self.image.fill(color)
        self.rect = pygame.rect.Rect(x, y, 32, 32)

class ExitBlock(Barriers):
    # Класс блоков для перехода на следующий уровень
    def __init__(self, x, y, color):
        Barriers.__init__(self, x, y, color)

class Persons(pygame.sprite.Sprite):
    """Базовый класс для всех персонажей: героев, врагов"""
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32))
        self.image.fill((img))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Боевые атрибуты персонажей
        self.level = 1
        self.hp = 0
        self.atk = 0
        self.defend = 0
        self.evade = 0
        self.crit = 0
        self.inventory = []


    def hit(self, enemy):
        enemy.hp -= int((self.atk-((self.atk / 100) * enemy.defend)))

class Heroes(Persons):
    """Класс героев"""
    def __init__(self, x, y, img):
        Persons.__init__(self, x, y, img)

    def update(self, up, left, right, down, barriers, total_win_w, total_win_h):
        self.speedx = 0
        self.speedy = 0
        if left:
            self.speedx -= self.movespeed
        if right:
            self.speedx += self.movespeed
        if up:
            self.speedy -= self.movespeed
        if down:
            self.speedy += self.movespeed
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.map_collide(total_win_w, total_win_h)
        self.barriers_collide(barriers)



    def map_collide(self, total_win_w, total_win_h):
        if self.rect.right > total_win_w:
            self.rect.right = total_win_w
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > total_win_h:
            self.rect.bottom = total_win_h

    def barriers_collide(self, barriers):
        barr_collide = pygame.sprite.spritecollide(self, barriers, False)
        if barr_collide:
            if self.speedx > 0: self.rect.right -= self.movespeed
            if self.speedx < 0: self.rect.left += self.movespeed
            if self.speedy > 0: self.rect.bottom -= self.movespeed
            if self.speedy < 0: self.rect.top += self.movespeed

class Warrior(Heroes):
    def __init__(self, x, y, img):
        Heroes.__init__(self, x, y, img)
        self.speedx = 0
        self.speedy = 0
        self.movespeed = 6
        self.atk = 120
        self.defend = 20
        self.hp = 1000
        self.first_strike = 0
        self.dodge = 0
        self.defend_limit = 90
        self.evade_limit = 0.75
        self.crit_limit = 0.95
class Mage(Heroes):
    def __init__(self, x, y, img):
        Heroes.__init__(self, x, y, img)
        self.speedx = 0
        self.speedy = 0
        self.movespeed = 6
        self.atk = 100
        self.defend = 0
        self.hp = 1000
        self.first_strike = 1
        self.dodge = 2
        self.defend_limit = 80
        self.evade_limit = 0.75
        self.crit_limit = 0.75
class Rogue(Heroes):
    def __init__(self, x, y, img):
        Heroes.__init__(self, x, y, img)
        self.speedx = 0
        self.speedy = 0
        self.movespeed = 6
        self.atk = 100
        self.defend = 10
        self.hp = 1000
        self.first_strike = 1
        self.dodge = 2
        self.defend_limit = 85
        self.evade_limit = 0.95
        self.crit_limit = 0.75
    def hit(self, enemy):
        enemy.hp -= int((self.atk - ((self.atk / 100) * int(enemy.defend / 2))))

class Enemies(Persons):
    """Класс - являющийся базовым для врагов"""
    def __init__(self, x, y, img):
        Persons.__init__(self, x, y, img)


    def update(self):
        pass

class Beast(Enemies):
    """Враги животные"""
    def __init__(self, x, y, img, lvl):
        Enemies.__init__(self, x, y, img)
        self.level = lvl
        self.atk = 50 * self.level
        self.defend = 10 * self.level
        self.hp = 300 * self.level
        self.crit = 0.1 * self.level


    def hit(self, enemy):
        if random.random() < self.crit:
            enemy.hp -= int((self.atk - ((self.atk / 100) * enemy.defend))) * 2
        else:
            enemy.hp -= int((self.atk - ((self.atk / 100) * enemy.defend)))
class Undead(Enemies):
    """Враги скелеты"""

    def __init__(self, x, y, img, lvl):
        Enemies.__init__(self, x, y, img)
        self.level = lvl
        self.atk = 70 * self.level
        self.defend = 5 * self.level
        self.hp = 350 * self.level
        self.evade = 0.1 * self.level
class Vampire(Enemies):
    """Враги вампиры"""

    def __init__(self, x, y, img, lvl):
        Enemies.__init__(self, x, y, img)
        self.level = lvl
        self.atk = 60 * self.level
        self.defend = 10 * self.level
        self.max_hp = 250 * self.level
        self.hp = self.max_hp
        self.regen = 0.1 * self.level

    def hit(self, enemy):
        enemy.hp -= int((self.atk - ((self.atk / 100) * enemy.defend)))
        self.hp += int((self.atk - ((self.atk / 100) * enemy.defend)) / self.regen)
        if self.hp >= self.max_hp:
            self.hp = self.max_hp


rand_enemies = ["Beast", "Undead", "Vampire"]