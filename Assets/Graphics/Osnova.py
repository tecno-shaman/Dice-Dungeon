import os
import pygame
import sys
import pytmx
import random

collisions = []
def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image

def get_collision_rects(tmx_map, layer_index):
    collision_rects = []
    layers = list(tmx_map.visible_layers)
    layer = layers[layer_index]
    if isinstance(layer, pytmx.TiledTileLayer):
        for x, y, gid in layer:
            tile = tmx_map.get_tile_image_by_gid(gid)
            if tile:
                rect = pygame.Rect(x * 16, y * 16, 16, 16)  # Используем 16x16 для коллизий
                collision_rects.append(rect)
    return collision_rects

def handle_collision(hero, hero_pos, keys, hero_speed, collision_rects): #Проверка коллизии
    for rect in collision_rects:
        if hero.rect.colliderect(rect):
            # Если происходит коллизия, откатить позицию героя
            if keys[pygame.K_LEFT]:
                hero_pos[0] += hero_speed
            if keys[pygame.K_RIGHT]:
                hero_pos[0] -= hero_speed
            if keys[pygame.K_UP]:
                hero_pos[1] += hero_speed
            if keys[pygame.K_DOWN]:
                hero_pos[1] -= hero_speed


def move_hero(hero, keys, hero_pos, hero_speed): #Движение гг
    moving = False  # Флаг для отслеживания движения
    if keys[pygame.K_LEFT]:
        hero_pos[0] -= hero_speed
        moving = True
    if keys[pygame.K_RIGHT]:
        hero_pos[0] += hero_speed
        moving = True
    if keys[pygame.K_UP]:
        hero_pos[1] -= hero_speed
        moving = True
    if keys[pygame.K_DOWN]:
        hero_pos[1] += hero_speed
        moving = True
    hero.rect.topleft = hero_pos  # Обновляем rect героя на основе hero_pos
    hero.update(moving)

def move_orks(): #Вражеский НПС
    global orks
    global orks_go
    if orks.rect.x < 600 and orks_go:
        orks.rect.x += 1
    elif orks.rect.x >= 400:
        if orks_go:
            orks = AnimatedSprite(load_image("orc2.png"), 8, 1, orks.rect.x, orks.rect.y)
            orks_go = False
        orks.rect.x -= 1
    else:
        orks_go = True
        orks = AnimatedSprite(load_image("orc.png"), 8, 1, orks.rect.x, orks.rect.y)

def move_orks2(): #Вражеский НПС
    global orks2
    global orks_go2# Объявляем orks как глобальную переменную
    if orks2.rect.y > 400 and orks_go2:
        orks2.rect.y -= 1  # Двигаем орка вправо
    elif orks2.rect.y < 500:
        if orks_go2:
            orks2 = AnimatedSprite(load_image("orc4.png"), 8, 1, orks2.rect.x, orks2.rect.y)
            orks_go2 = False
        orks2.rect.y += 1  # Двигаем орка влево
    else:
        orks_go2 = True
        orks2 = AnimatedSprite(load_image("orc3.png"), 8, 1, orks2.rect.x, orks2.rect.y)

def move_orks5(): #Вражеский НПС
    global orks5
    global orks_go5
    if orks5.rect.x < 900 and orks_go5:
        orks5.rect.x += 1
    elif orks5.rect.x >= 750:
        if orks_go5:
            orks5 = AnimatedSprite(load_image("orc2.png"), 8, 1, orks5.rect.x, orks5.rect.y)
            orks_go5 = False
        orks5.rect.x -= 1
    else:
        orks_go5 = True
        orks5 = AnimatedSprite(load_image("orc.png"), 8, 1, orks5.rect.x, orks5.rect.y)

def move_orks6(): #Вражеский НПС
    global orks6
    global orks_go6
    if orks6.rect.x < 1200 and orks_go6:
        orks6.rect.x += 1
    elif orks6.rect.x >= 800:
        if orks_go6:
            orks6 = AnimatedSprite(load_image("orc2.png"), 8, 1, orks6.rect.x, orks6.rect.y)
            orks_go6 = False
        orks6.rect.x -= 1
    else:
        orks_go6 = True
        orks6 = AnimatedSprite(load_image("orc.png"), 8, 1, orks6.rect.x, orks6.rect.y)

def move_ratte(): #Вражеский НПС
    global ratte
    global ratte_go
    if ratte.rect.x < 600 and ratte_go:
        ratte.rect.x += 1
    elif ratte.rect.x >= 400:
        if ratte_go:
            ratte = AnimatedSprite(load_image("ratte.png"), 6, 1, ratte.rect.x, ratte.rect.y)
            ratte_go = False
        ratte.rect.x -= 1
    else:
        ratte_go = True
        ratte = AnimatedSprite(load_image("ratte2.png"), 6, 1, ratte.rect.x, ratte.rect.y)

def move_ratte2(): #Вражеский НПС
    global ratte2
    global ratte_go2# Объявляем orks как глобальную переменную
    if ratte2.rect.y > 415 and ratte_go2:
        ratte2.rect.y -= 1  # Двигаем орка вправо
    elif ratte2.rect.y < 600:
        if ratte_go2:
            ratte2 = AnimatedSprite(load_image("ratte3.png"), 6, 1, ratte2.rect.x, ratte2.rect.y)
            ratte_go2 = False
        ratte2.rect.y += 1  # Двигаем орка влево
    else:
        ratte_go2 = True
        ratte2 = AnimatedSprite(load_image("ratte4.png"), 6, 1, ratte2.rect.x, ratte2.rect.y)

def move_monstr(): #Вражеский НПС
    global monstr
    global monstr_go
    if monstr.rect.x < 500 and monstr_go:
        monstr.rect.x += 1
    elif monstr.rect.x >= 300:
        if monstr_go:
            monstr = AnimatedSprite(load_image("Monstr2.png"), 5, 2, monstr.rect.x, monstr.rect.y)
            monstr_go = False
        monstr.rect.x -= 1
    else:
        monstr_go = True
        monstr = AnimatedSprite(load_image("Monstr.png"), 5, 2, monstr.rect.x, monstr.rect.y)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        # Ограничиваем движение камеры по x
        self.dx = max(-(target.rect.x + target.rect.w // 2 - width // 2),
                       -(tmx_map.width * tmx_map.tilewidth - width))
        self.dx = min(0, self.dx)  # Не позволяем камере выходить за левую границу
        # Ограничиваем движение камеры по y
        self.dy = max(-(target.rect.y + target.rect.h // 2 - height // 2),
                       -(tmx_map.height * tmx_map.tileheight - height))
        self.dy = min(0, self.dy)


class AnimatedSprite(pygame.sprite.Sprite):#Анимация спрайтов
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.animation_speed = 0.1
        self.animation_timer = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, moving):
        if moving:
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.animation_timer = 0
        else:
            self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def change_animation(self, sheet, columns, rows):
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0

class Game(): #Класс для перехода в боёвку
    pass

def load_map(filename):
    return pytmx.load_pygame(filename)

def check_hero_ork_collision(hero, orks):
    return hero.rect.colliderect(orks.rect)

class Inventory:
    def __init__(self, size= 8):
        self.size = size
        self.items = [None] * self.size  # Список для хранения предметов (None означает пустой слот)

    def add_item(self, item):
        for i in range(self.size):
            if self.items[i] is None:  # Найти первый пустой слот
                self.items[i] = item
                return True
        return False  # Если инвентарь полон

    def remove_item(self, index):
        if 0 <= index < self.size:
            self.items[index] = None  # Удаляем предмет из слота

    def get_items(self):
        return [item for item in self.items if item is not None]

class InventoryUI:
    def __init__(self, inventory):
        self.inventory = inventory
        self.font = pygame.font.Font(None, 36)  # Шрифт для отображения текста

    def draw(self, screen):
        # Рисуем фон инвентаря
        pygame.draw.rect(screen, (50, 50, 50), (50, 50, 400, 300))  # Фон
        for i in range(self.inventory.size):
            pygame.draw.rect(screen, (255, 255, 255), (60 + i * 50, 60, 40, 40), 2)  # Слот
            item = self.inventory.items[i]
            if item:
                text = self.font.render(item, True, (255, 255, 255))
                screen.blit(text, (60 + i * 50, 60))  # Отображаем предмет

class Chest(AnimatedSprite):  # Сундук
    def __init__(self, x, y):
        super().__init__(load_image("chest.png"), 1, 4, x, y)  # Загрузка спрайтов для анимации
        self.is_open = False  # Флаг для проверки, открыт ли сундук

    def open_chest(self):
        if not self.is_open:
            self.is_open = True
            return random.randint(1, 5)  # Возвращаем случайное количество монет (от 1 до 5)
        return 0  # Если сундук уже открыт

    def update(self, moving):
        super().update(moving)  # Вызов обновления анимации
        if self.is_open:
            self.cur_frame = 1  # Меняем на второй кадр анимации

if __name__ == '__main__':
    pygame.init()
    screen_size = (600, 400)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Перемещение героя")
    width, height = 100, 100
    tmx_map = load_map('map_now1.tmx')
    inventory = Inventory()
    inventory_ui = InventoryUI(inventory)
    inventory_open = False
    all_sprites = pygame.sprite.Group()
    ork_pos = [400, 200]
    ork_pos2 = [400, 400]
    orks = AnimatedSprite(load_image("orc.png"), 8, 1, *ork_pos)
    orks2 = AnimatedSprite(load_image("orc3.png"), 8, 1, *ork_pos2)
    orks_exists = True
    hero = AnimatedSprite(load_image("run.png"), 6, 1, 50, 50)
    all_sprites.add(orks)
    all_sprites.add(orks2)
    orks_go = True
    orks_go2 = True
    coin_image = load_image("mani.png")  # Замените на имя Вашего файла с изображением монеты
    coin_count = 0
    chest = Chest(200, 350)  # Замените координаты на нужные
    all_sprites.add(chest)
    font = pygame.font.Font(None, 36)
    # Создаем героя
    hero_pos = [100, 350]
    hero.rect.topleft = hero_pos
    hero_speed = 5
    fps = 50
    collision_rects = get_collision_rects(tmx_map, 1)
    clock = pygame.time.Clock()
    camera = Camera()
    running = True
    two = True
    three = False
    orks_exists2 = False
    orks_exists3 = False


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    inventory_open = not inventory_open
                if hero.rect.colliderect(chest.rect) and keys[pygame.K_e]:  # Если герой рядом с сундуком и нажата клавиша E
                    coins_gained = chest.open_chest()  # Открываем сундук и получаем монеты
                    coin_count += coins_gained  # Увеличиваем количество монет



        keys = pygame.key.get_pressed()
        move_hero(hero, keys, hero_pos, hero_speed)
        if hero.rect.colliderect(chest.rect):
            # Если герой рядом с сундуком, отображаем текст
            text_surface = font.render("Нажмите E, чтобы открыть сундук", True, (255, 255, 255))
            screen.blit(text_surface, (chest.rect.x, chest.rect.y - 30))  # Отображаем текст над сундуком

            if keys[pygame.K_e]:  # Если нажата клавиша E
                coins_gained = chest.open_chest()  # Открываем сундук
                coin_count += coins_gained  # Увеличиваем кол
        if hero.rect.y >= 500 and hero.rect.x >= 900 and two:#Переход на вторую локацию
            tmx_map = load_map('map_now2.tmx')
            hero_pos = [100, 350]
            collisions = []
            collision_rects = get_collision_rects(tmx_map, 1)
            orks.kill()
            orks2.kill()
            orks_exists = False
            two = False
            three = True
            ratte_pos = [500, 280]
            ratte = AnimatedSprite(load_image("ratte2.png"), 6, 1, *ratte_pos)
            ratte_go = True
            ratte_pos2 = [300, 500]
            ratte2 = AnimatedSprite(load_image("ratte4.png"), 6, 1, *ratte_pos2)
            ratte_go2 = True
            original_width = 500
            original_height = 50
            madgic_image = load_image("Madgic.png")
            scaled_madgic_image = pygame.transform.scale(madgic_image,
                                                            (int(original_width),
                                                            int(original_height)))
            madgic_pos = [500, 700]
            madgic = AnimatedSprite(scaled_madgic_image, 8, 1, *madgic_pos)
            orks3_pos = [710, 200]
            orks3 = AnimatedSprite(load_image("orc5.png"), 4, 1, *orks3_pos)
            orks4_pos = [710, 350]
            orks4 = AnimatedSprite(load_image("orc5.png"), 4, 1, *orks4_pos)
            ork_pos5 = [800, 200]
            orks5 = AnimatedSprite(load_image("orc.png"), 8, 1, *ork_pos5)
            orks_go5 = True
            ork_pos6 = [800, 300]
            orks6 = AnimatedSprite(load_image("orc.png"), 8, 1, *ork_pos6)
            orks_go6 = True
            all_sprites.add(orks6)
            all_sprites.add(orks5)
            all_sprites.add(orks4)
            all_sprites.add(orks3)
            all_sprites.add(ratte)
            all_sprites.add(ratte2)
            all_sprites.add(madgic)
            orks_exists2 = True

        elif three and hero.rect.x >= 1100:#Переход на 3 локацию
            tmx_map = load_map('map_now3.tmx')
            hero_pos = [100, 100]
            collisions = []
            three = False
            collision_rects = get_collision_rects(tmx_map, 1)
            original_width1 = 900
            original_height1 = 300
            monstr_image = load_image("Monstr.png")
            scaled_monstr_image = pygame.transform.scale(monstr_image,
                                                            (int(original_width1),
                                                            int(original_height1)))
            monstr_pos = [300, 50]
            monstr = AnimatedSprite(scaled_monstr_image, 5, 2, *monstr_pos)
            monstr_go = True
            all_sprites.add(monstr)
            orks_exists3 = True
            orks_exists2 = False

        handle_collision(hero, hero_pos, keys, hero_speed, collision_rects)
        screen.fill((0, 0, 0))
        camera.update(hero)
        tmx_map.tilewidth = 16
        tmx_map.tileheight = 16
        chest.update(True)  # Обновляем анимацию сундука
        screen.blit(chest.image, (chest.rect.x + camera.dx, chest.rect.y + camera.dy))

        # Отображение количества монет
        coin_text = f"Coins: {coin_count}"
        font = pygame.font.Font(None, 36)
        text_surface = font.render(coin_text, True, (255, 255, 255))
        screen.blit(text_surface, (screen_size[0] - text_surface.get_width() - 10, 10))
        # Отрисовка карты
        for layer in tmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tmx_map.get_tile_image_by_gid(gid)
                    if tile:
                        # Применяем смещение камеры к координатам
                        screen.blit(tile, (x * tmx_map.tilewidth + camera.dx, y * tmx_map.tileheight + camera.dy))

        camera.apply(hero)  # Применяем смещение камеры к герою
        screen.blit(hero.image, hero.rect.topleft)
        if orks_exists:#1 локация
            move_orks()
            move_orks2()
            orks.update(True)
            orks2.update(True)
            screen.blit(orks.image, (orks.rect.x + camera.dx, orks.rect.y + camera.dy))
            screen.blit(orks2.image, (orks2.rect.x + camera.dx, orks2.rect.y + camera.dy))
            screen.blit(chest.image, (chest.rect.x + camera.dx, chest.rect.y + camera.dy))

            for ork in [orks, orks2]:
                if hero.rect.colliderect(ork.rect):
                    Game()
        if orks_exists2:# 2 локация
            move_orks6()
            move_orks5()
            move_ratte2()
            move_ratte()
            ratte.update(True)
            ratte2.update(True)
            madgic.update(True)
            orks3.update(True)
            orks4.update(True)
            orks5.update(True)
            orks6.update(True)
            screen.blit(ratte.image, (ratte.rect.x + camera.dx, ratte.rect.y + camera.dy))
            screen.blit(ratte2.image, (ratte2.rect.x + camera.dx, ratte2.rect.y + camera.dy))
            screen.blit(madgic.image, (madgic.rect.x + camera.dx, madgic.rect.y + camera.dy))
            screen.blit(orks3.image, (orks3.rect.x + camera.dx, orks3.rect.y + camera.dy))
            screen.blit(orks4.image, (orks4.rect.x + camera.dx, orks4.rect.y + camera.dy))
            screen.blit(orks5.image, (orks5.rect.x + camera.dx, orks5.rect.y + camera.dy))
            screen.blit(orks6.image, (orks6.rect.x + camera.dx, orks6.rect.y + camera.dy))
        if orks_exists3:# 3 локация
            move_monstr()
            monstr.update(True)
            screen.blit(monstr.image, (monstr.rect.x + camera.dx, monstr.rect.y + camera.dy))
        if inventory_open:
            inventory_ui.draw(screen)


        pygame.display.flip()  # Обновление экрана
        clock.tick(fps)
    pygame.quit()
    sys.exit()
