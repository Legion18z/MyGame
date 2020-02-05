class Items:
    def __init__(self, name, type, lvl, atk=0, defend=0, hp=0, evade=0.0, crit=0.0, fs=0, dodge = 0):
        self.name = name
        self.type = type
        self.item_lvl = lvl
        self.my_hero = None
        self.atk_buff = atk
        self.defend_buff = defend
        self.hp_buff = hp
        self.evade_buff = evade
        self.crit_buff = crit
        self.fs_buff = fs
        self.hero_defend_overdone = 0
        self.hero_evade_overdone = 0
        self.hero_crit_overdone = 0
        self.dodge_buff = dodge

    def on_inventory(self, hero):
        self.my_hero = hero
        if self.atk_buff != 0:
            self.my_hero.atk += self.atk_buff
        if self.defend_buff != 0:
            self.my_hero.defend += self.defend_buff
            if self.my_hero.defend >= self.my_hero.defend_limit:
                self.hero_defend_overdone = self.my_hero.defenf - hero.defend_limit
                self.my_hero.defend = self.my_hero.defend_limit
        if self.hp_buff != 0:
            self.my_hero.hp += self.hp_buff
        if self.evade_buff != 0:
            self.my_hero.evade += self.evade_buff
            if self.my_hero.evade >= self.my_hero.evade_limit:
                self.hero_evade_overdone = self.my_hero.evade - self.my_hero.evade_limit
                self.my_hero.evade = self.my_hero.evade_limit
        if self.crit_buff != 0:
            self.my_hero.crit += self.crit_buff
            if self.my_hero.crit >= self.my_hero.crit_limit:
                self.hero_crit_overdone = self.my_hero.crit - self.my_hero.crit_limit
                self.my_hero.crit = self.my_hero.crit_limit
        if self.fs_buff != 0:
            self.my_hero.first_strike += self.fs_buff
        if self.dodge_buff != 0:
            self.my_hero.dodge += self.dodge_buff

    def __del__(self):
        if self.my_hero != None:
            if self.atk_buff != 0:
                self.my_hero.atk -= self.atk_buff
            if self.defend_buff != 0:
                self.my_hero.defend -= self.defend_buff-self.hero_defend_overdone
            if self.hp_buff != 0:
                self.my_hero.hp -= self.hp_buff
            if self.evade_buff != 0:
                self.my_hero.evade -= self.evade_buff - self.hero_evade_overdone
            if self.crit_buff != 0:
                self.my_hero.crit -= self.crit_buff - self.hero_crit_overdone
            if self.fs_buff != 0:
                self.my_hero.first_strike -= self.fs_buff
            if self.dodge_buff != 0:
                self.my_hero.dodge -= self.dodge_buff

items = {
    "Tier1": [Items("Короткий меч", type="weapon", lvl=1, atk=30),
              Items("Топор лесоруба", type="weapon", lvl=1, atk=40),
              Items("Деревянный щит", type="armor", lvl=1, defend=10),
              Items("Кираса", type="armor", lvl=1, defend=20),
              Items("Старый лук", type="ranged", lvl=1, fs=1),
              Items("Плащ путника", type="cloak", lvl=1, defend=5),
              Items("Самодельный амулет", type="jewelry", lvl=1, hp=100),
              Items("Кольцо плута", type="jewelry", lvl=1, evade=0.1)],
    "Tier2": [Items("Кирка горняка", type="weapon", lvl=2, atk=60),
              Items("Кинжалы контрабандиста", type="weapon", lvl=2, atk=40, crit=0.1),
              Items("Каска горняка", type="armor", lvl=2, defend=20, hp=100),
              Items("Кожаная спецовка", type="armor", lvl=2, defend=15, evade=0.15),
              Items("Пистоль", type="ranged", lvl=2, fs=1, crit=0.15),
              Items("Посох мага", type="ranged", lvl=2, atk=20, fs=2),
              Items("Плащ контрабандиста", type="cloak", lvl=2, evade=0.3),
              Items("Кристал на нитке", type="jewelry", lvl=2, defend=15, hp=50),
              Items("Гномское кольцо", type="jewelry", lvl=2, atk=50, defend=20)],
    "Tier3": [Items("Клеймора", type="weapon", lvl=3, atk=120, crit=0.2),
              Items("Клинки ветров", type="weapon", lvl=3, atk=100, evade=0.3),
              Items("Щит и меч паладина", type="weapon", lvl=3, atk=100, defend=40),
              Items("Доспехи паладина", type="armor", lvl=3, defend=40, hp=100),
              Items("Гномская бригантина", type="armor", lvl=3, defend=40, crit=0.2),
              Items("Ручной арбалет", type="jewelry", lvl=3, atk=50, fs=2),
              Items("Лук ветра", type="jewelry", lvl=3, atk=50, evade=0.2, fs=2),
              Items("Накидка с мехом", type="cloak", lvl=3, defend=15, hp=50, dodge=1),
              Items("Амулет берсерка", type="jewelry", lvl=3, atk=250, defend=-100, crit=0.5),
              Items("Кольцо с жемчугом", type="jewelry", lvl=3, hp=100, evade=0.2, crit=0.2)],
    "Tier4": [Items("Секира могущества", type="weapon", lvl=4, atk=200, crit=0.4),
              Items("Кинжалы из зубов дракона", type="weapon", lvl=4, atk=100, evade=0.3, crit=0.3),
              Items("Императорские доспехи", type="armor", lvl=4, defend=50, hp=200),
              Items("Мифриловая броня", type="armor", lvl=4, defend=40, evade=0.4),
              Items("Посох мудрости", type="ranged", lvl=4, atk=70, hp=70, fs=3),
              Items("Плащ невидимости", type="cloak", lvl=4, evade=0.5, fs=2),
              Items("Амулет предвидения", type="jewelry", lvl=4, dodge=4),
              Items("Кольцо императора", type="jewelry", lvl=4, atk=70, defend=20, hp=80, evade=0.15, crit=0.15)],
    "Tier5": [Items("Амулет правителей", type="artifact", lvl=5),
              Items("Грааль господства", type="artifact", lvl=5),
              Items("Посох богов", type="artifact", lvl=5)]
}