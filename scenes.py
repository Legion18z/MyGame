import pygame
import random
import sys
from os import path
from tkinter import *
from tkinter import messagebox

from levels import *
from items import *
from classes import *


GAME_NAME = "HERO'S PATH!!!"
WIN_WIDTH = 640
WIN_HEIGHT = 480
FPS = 30
M_WIN_WIDTH = int(WIN_WIDTH / 2)
M_WIN_HEIGHT = int(WIN_HEIGHT /2)
BLOCK_SIZE = 32
IMG_DIR = path.join(path.dirname(__file__), "img")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
  


class SceneDirector:
    """ Класс отвечающий за управление сценами в игре"""

    def __init__(self, hero_name, hero_prof):
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        self.scene = None
        self.quit_flag = False
        self.clock = pygame.time.Clock()
        self.level = 1
        war_img = pygame.image.load(path.join(IMG_DIR, "warrior.png")).convert()
        mage_img = pygame.image.load(path.join(IMG_DIR, "mage.png")).convert()
        rogue_img = pygame.image.load(path.join(IMG_DIR, "rogue.png")).convert()
    
        if hero_prof == 1:
            self.hero = Warrior(0, 0, war_img, hero_name)
        elif hero_prof == 2:
            self.hero = Mage(0, 0, mage_img, hero_name)
        elif hero_prof ==3:
            self.hero = Rogue(0, 0, rogue_img, hero_name)

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
    """Сцена смерти или победы персонажа"""

    def __init__(self, director, text):
        Scene.__init__(self, director)
        self.font = pygame.font.SysFont("Arial", 56)
        self.sub_font = pygame.font.SysFont("Arial", 32)
        self.text = text

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                sys.exit()



    def on_update(self):
        pass

    def on_draw(self, screen):
        screen.fill(RED)
        text1 = self.font.render(GAME_NAME,True, WHITE)
        text2 = self.sub_font. render(self.text, True, WHITE)
        screen.blit(text1, (200, 30))
        screen.blit(text2, (100, 80))


class LvlScene(Scene):
    """Сцена поздравляющая с прохождением уровня и переводящая на новый уровень"""
    def __init__(self, director):
        Scene.__init__(self, director)
        self.font = pygame.font.SysFont("Arial", 18)
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
        screen.blit(text1, (50, 30))
        screen.blit(text2, (50, 80))


class GameScene(Scene):
    def __init__(self, director):
        Scene.__init__(self, director)
        self.all_sprites = pygame.sprite.Group()
        self.barriers = pygame.sprite.Group()
        self.exitblocks = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bosses = pygame.sprite.Group()
        
        x = 0
        y = 0

        self.total_level_width = len(levels[self.director.level][0]) * BLOCK_SIZE
        self.total_level_height = len(levels[self.director.level]) * BLOCK_SIZE

        block_image = pygame.image.load(path.join(IMG_DIR, "block{}.png".format(self.director.level))).convert()
        exit_image = pygame.image.load(path.join(IMG_DIR, "exit.png")).convert()
        img_beast = pygame.image.load(path.join(IMG_DIR, "beast.png")).convert()
        img_undead = pygame.image.load(path.join(IMG_DIR, "undead.png")).convert()
        img_vampire = pygame.image.load(path.join(IMG_DIR, "vampire.png")).convert()
        random.shuffle(items["Tier{}".format(self.director.level)])
        for row in levels[self.director.level]:
            for col in row:
                if col == "-":
                    b = Barriers(x, y, block_image)
                    self.all_sprites.add(b)
                    self.barriers.add(b)
                if col == "E":
                    e = ExitBlock(x, y, exit_image)
                    self.all_sprites.add(e)
                    self.exitblocks.add(e)
                if col == "M":
                    rand_item = items["Tier{}".format(self.director.level)].pop(0)
                    rand_mob = random.choice(["Beast", "Undead", "Vampire"])
                    if rand_mob == "Beast":
                        mob = Beast(x, y, img_beast, rand_mob, self.director.level)
                    if rand_mob == "Undead":
                        mob = Undead(x, y, img_undead, rand_mob, self.director.level)
                    if rand_mob == "Vampire":
                        mob = Vampire(x, y, img_vampire, rand_mob, self.director.level)
                    mob.inventory.append(rand_item)
                    self.all_sprites.add(mob)
                    self.enemies.add(mob)
                if col == "B":
                    rand_item = items["Tier{}".format(self.director.level)].pop(0)
                    boss = rand_boss(x, y, RED, self.director.level)
                    boss.inventory.append(rand_item)
                    self.all_sprites.add(boss)
                    self.bosses.add(boss)
                if col == "H":
                    self.director.hero.rect.x = x
                    self.director.hero.rect.y = y
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
                death_text = "ВЫ ПОГИБЛИ!!!"
                scene = TitleScene(self.director, death_text)
                self.director.change_scene(scene)
        #Бой с боссом
        boss_collide = pygame.sprite.spritecollide(self.director.hero, self.bosses, False)
        for b in boss_collide:
            battle_loser = battle(self.director.hero, b)
            if b == battle_loser:
                final_text = "Вы победили {}!!!!".format(b.name)
                b.kill()
                scene = TitleScene(self.director, final_text)
                self.director.change_scene(scene)
            if self.director.hero == battle_loser:
                death_text = "ВЫ ПОГИБЛИ!!!"
                scene = TitleScene(self.director, death_text)
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
    first_strike = hero.first_strike
    dodge = hero.dodge
    duel = True
    while duel:
        if hero.hp > 0 and enemy.hp > 0:
            now = pygame.time.get_ticks()
            if now - last_hit > hit_delay:
                last_hit = now
                # Нанесение первых ударов если есть возможность
                while first_strike > 0:
                    hero.hit(enemy)
                    first_strike -= 1
                # Рандомное нанесение ударов
                hit_order = random.randint(1, 2)
                evade_luck = random.random()
                if hit_order == 1:
                    if enemy.evade < evade_luck:
                        hero.hit(enemy)
                if hit_order == 2:
                    if hero.evade < evade_luck:
                        # Проверка на избегание удара
                        if dodge > 0:
                            dodge -= 1
                        else:
                            enemy.hit(hero)
        else: duel = False
    if enemy.hp <= 0:
        loser = enemy
        hero.exp += enemy.level * 5
        if hero.exp >= hero.exp_cap:
            hero.level_up()
        hero.grab_loot(enemy)
    elif hero.hp <= 0:
        loser = hero
    return loser


def chose_your_hero(enter_name, profession, window):
    name = enter_name.get()
    p = profession.get()
    if name == "":
        messagebox.showinfo(GAME_NAME, "Не введено имя!!!")
    elif len(name) >= 12:
        messagebox.showinfo(GAME_NAME, "Слишком длинное имя!! Такое имя никто не запомнит в веках!!")
    elif p == 0:
        messagebox.showinfo(GAME_NAME, "Не выбран персонаж!!!")
    else:
        window.destroy()

def disable_event():
    pass

def main():
    # Приветственное окно с возможностью выбора игрового персонажа
    title = Tk()
    title.title(GAME_NAME)
    title.geometry("{}x{}".format(WIN_WIDTH, WIN_HEIGHT))
    title.overrideredirect(True)

    lbl1 = Label(text=GAME_NAME)
    lbl1.place(relx=.4, rely=.2)
    #lbl1.grid(row=0, column=1)
    lbl2 = Label(text="Введи своё имя:")
    lbl2.place(relx=.2, rely=.4)
    #lbl2.grid(row=1, column=0)
    enter_name = StringVar()
    name_entry = Entry(textvariable=enter_name)
    name_entry.place(relx=.6, rely=.4)
    #name_entry.grid(row=1, column=1)
    lbl3 = Label(text="Выберите начинающего героя:")
    lbl3.place(relx=.4, rely=.6)
    #lbl3.grid(row=2, column=1)
    
    hero_var = IntVar()
    warrior_check = Radiobutton(text="Воин", value=1, variable=hero_var, padx=15, pady=10)
    warrior_check.place(relx=.2, rely=.7)
    #warrior_check.grid(row=3, column=0)
    mage_check = Radiobutton(text="Маг", value=2, variable=hero_var, padx=15, pady=10)
    mage_check.place(relx=.4, rely=.7)
    #mage_check.grid(row=3, column=1)
    rogue_check = Radiobutton(text="Разбойник", value=3, variable=hero_var, padx=15, pady=10)
    rogue_check.place(relx=.6, rely=.7)
    #rogue_check.grid(row=3, column=2)

    btn=Button(text="В игру!", command=lambda: chose_your_hero(enter_name, hero_var, title))
    btn.place(relx=.8, rely=.9)

    btnExit = Button(text="Выход", command=sys.exit)
    btnExit.place(relx=.1, rely=.9)
    
    title.protocol("WM_DELETE_WINDOW", disable_event)
    title.mainloop()
    
    name = enter_name.get()
    p = hero_var.get()
    
    dir = SceneDirector(name, p)
    scene = GameScene(dir)
    dir.change_scene(scene)
    dir.loop()




if __name__ == "__main__":
    pygame.init()
    main()