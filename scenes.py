import pygame
import random

from levels import *
from items import *
from classes import *


GAME_NAME = "HERO'S PATH!!!"
WIN_WIDTH = 640
WIN_HEIGHT = 480
FPS = 30
M_WIN_WIDTH = int(WIN_WIDTH / 2)
M_WIN_HEIGHT = int(WIN_HEIGHT /2)

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class SceneDirector:
    """ Класс отвечающий за управление сценами в игре"""

    def __init__(self, hero):
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        self.scene = None
        self.quit_flag = False
        self.clock = pygame.time.Clock()
        self.level = 1
        self.hero = hero

    def loop(self):
        """Основной цикл игры"""
        while not self.quit_flag:
            time = self.clock.tick(FPS)

            # События выхода из игры
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
                # Вызов метода производящего все события в сцене
                self.scene.on_event(event)
            # Вызов метода обновляющего всю сцену
            self.scene.on_update()
            # Вызов метода отрисовывающего сцену
            self.scene.on_draw(self.screen)
            pygame.display.flip()

    def change_scene(self, scene):
        self.scene = scene

    def quit(self):
        self.quit_flag = True


class Camera:
    def __init__(self,camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self,target):
        try:
            return target.rect.move(self.state.topleft)
        except AttributeError:
            return map(sum, zip(target, self.state.topleft))

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, w, h= -l + M_WIN_WIDTH, -t + M_WIN_HEIGHT, w, h

    l = min(0, l)
    l = max(-(camera.width - WIN_WIDTH), l)
    t = min(0, t)
    t = max(-(camera.height - WIN_HEIGHT), t)

    return pygame.Rect(l, t, w, h)


class Scene:
    """Базовый класс сцены - от него пойдут все остальные типы сцен"""

    def __init__(self, scene_dir):
        self.director = scene_dir

    def on_update(self):
        # Определяется в дочерних классах сцен
        raise NotImplementedError

    def on_event(self):
        # Определяется в дочерних классах сцен
        raise NotImplementedError

    def on_draw(self, screen):
        # Определяется в дочерних классах сцен
        raise NotImplementedError


class TitleScene(Scene):
    """Начальная сцена - выбор персонажа"""

    def __init__(self, director):
        Scene.__init__(self, director)
        self.font = pygame.font.SysFont("Arial", 56)
        self.sub_font = pygame.font.SysFont("Arial", 32)

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                scene = GameScene(self.director)
                self.director.change_scene(scene)



    def on_update(self):
        pass

    def on_draw(self, screen):
        screen.fill(RED)
        text1 = self.font.render(GAME_NAME,True, WHITE)
        text2 = self.sub_font. render(">Выбери начинающего героя<", True, WHITE)
        screen.blit(text1, (200, 30))
        screen.blit(text2, (100, 80))


class LvlScene(Scene):
    """Сцена поздравляющая с прохождением уровня и переводящая на новый уровень"""
    def __init__(self, director):
        Scene.__init__(self, director)
        self.font = pygame.font.SysFont("Arial", 56)
        self.sub_font = pygame.font.SysFont("Arial", 18)


    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.director.level += 1
                scene = GameScene (self.director)
                self.director.change_scene(scene)

    def on_update(self):
        pass

    def on_draw(self, screen):
        screen.fill(BLUE)
        text1 = self.font.render('Поздравляю вы прошли уровень {}!!!'.format(self.director.level), True, WHITE)
        text2 = self.sub_font.render('Для перехода к следующему уровню нажмите "ПРОБЕЛ"', True, WHITE)
        screen.blit(text1, (200, 30))
        screen.blit(text2, (200, 80))


class GameScene(Scene):
    def __init__(self, director):
        Scene.__init__(self, director)
        self.all_sprites = pygame.sprite.Group()
        self.barriers = pygame.sprite.Group()
        self.exitblocks = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        x = 0
        y = 0

        self.total_level_width = len(levels[self.director.level][0]) * 32
        self.total_level_height = len(levels[self.director.level]) * 32

        random.shuffle(rand_enemies)
        for row in levels[self.director.level]:
            for col in row:
                if col == "-":
                    b = Barriers(x, y, YELLOW)
                    self.all_sprites.add(b)
                    self.barriers.add(b)
                if col == "E":
                    e = ExitBlock(x, y, WHITE)
                    self.all_sprites.add(e)
                    self.exitblocks.add(e)
                if col == "M":
                    rand_mob = rand_enemies.pop(0)
                    if rand_mob == "Beast":
                        m = Beast(x, y, RED, self.director.level)
                    if rand_mob == "Undead":
                        m = Undead(x, y, GREEN, self.director.level)
                    if rand_mob == "Vampire":
                        m = Vampire(x, y, BLUE, self.director.level)
                    self.all_sprites.add(m)
                    self.enemies.add(m)
                if col == "H":
                    self.director.hero = Warrior(x, y, GREEN)
                    self.all_sprites.add(self.director.hero)
                x += 32
            y += 32
            x = 0

        self.camera = Camera(complex_camera, self.total_level_width, self.total_level_height)

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                scene = TitleScene(self.director)
                self.director.change_scene(scene)

    def on_update(self):
        # Управление персонажем
        pressed = pygame.key.get_pressed()
        up, left, right, down = [pressed[key] for key in (pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN)]
        self.director.hero.update(up, left, right, down, self.barriers, self.total_level_width, self.total_level_height)
        # Сценарий при столкновении с врагом
        enemy_collide = pygame.sprite.spritecollide(self.director.hero, self.enemies, False)
        for e in enemy_collide:
            battle_loser = battle(self.director.hero, e)
            if e == battle_loser:
                e.kill()
            if self.director.hero == battle_loser:
                scene = TitleScene(self.director)
                self.director.change_scene(scene)
        # Сценарий при выходе с уровня
        exit_collide = pygame.sprite.spritecollide(self.director.hero, self.exitblocks, False)
        if exit_collide:
            scene = LvlScene(self.director)
            self.director.change_scene(scene)
        self.camera.update(self.director.hero)


    def on_draw(self, screen):
        screen.fill(BLACK)
        for s in self.all_sprites:
            screen.blit(s.image, self.camera.apply(s))


def battle(hero, enemy):
    hit_delay = 500
    last_hit = pygame.time.get_ticks()
    while hero.hp >= 0 or enemy.hp >= 0:
        now = pygame.time.get_ticks()
        if now - last_hit > hit_delay:
            last_hit = now
            # Рандомное нанесение ударов
            hit_order = random.randint(1, 2)
            if hit_order == 1:
                hero.hit(enemy)
            if hit_order == 2:
                enemy.hit(hero)
    if enemy.hp <= 0:
        loser = enemy
    elif hero.hp <= 0:
        loser = hero

    return loser

def main():
    hero = None
    dir = SceneDirector(hero)
    scene = TitleScene(dir)
    dir.change_scene(scene)
    dir.loop()


if __name__ == "__main__":
    pygame.init()
    main()