import os
import pygame
import sys
import pytmx

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

def get_collision_rects(tmx_map, layer_index): #Список обьектов для коллизии
    collision_rects = []
    layers = list(tmx_map.visible_layers)
    layer = layers[layer_index]
    if isinstance(layer, pytmx.TiledTileLayer):
        for x, y, gid in layer:
            tile = tmx_map.get_tile_image_by_gid(gid)
            if tile:
                rect = pygame.Rect(x * tmx_map.tilewidth, y * tmx_map.tileheight,
                                   tmx_map.tilewidth, tmx_map.tileheight)
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
    if orks.rect.x < 500 and orks_go:
        orks.rect.x += 1
    elif orks.rect.x >= 200:
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
    elif orks2.rect.y < 600:
        if orks_go2:
            orks2 = AnimatedSprite(load_image("orc4.png"), 8, 1, orks2.rect.x, orks2.rect.y)
            orks_go2 = False
        orks2.rect.y += 1  # Двигаем орка влево
    else:
        orks_go2 = True
        orks2 = AnimatedSprite(load_image("orc3.png"), 8, 1, orks2.rect.x, orks2.rect.y)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
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


if __name__ == '__main__':
    pygame.init()
    screen_size = (600, 400)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Перемещение героя")
    width, height = 600, 400
    tmx_map = load_map('map4.tmx')
    all_sprites = pygame.sprite.Group()
    ork_pos = [200, 50]
    ork_pos2 = [500, 500]
    orks = AnimatedSprite(load_image("orc.png"), 8, 1, *ork_pos)
    orks2 = AnimatedSprite(load_image("orc3.png"), 8, 1, *ork_pos2)
    orks_exists = True
    hero = AnimatedSprite(load_image("run.png"), 10, 1, 50, 50)
    all_sprites.add(orks)
    all_sprites.add(orks2)
    orks_go = True
    orks_go2 = True
    # Создаем героя
    hero_pos = [300, 0]
    hero.rect.topleft = hero_pos
    hero_speed = 5
    fps = 50
    collision_rects = get_collision_rects(tmx_map, 1)
    clock = pygame.time.Clock()
    camera = Camera()
    running = True
    two = True
    three = True
    orks_exists2 = False
    orks_exists3 = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        move_hero(hero, keys, hero_pos, hero_speed)
        if hero.rect.y >= 700 and two:#Переход на вторую локацию
            tmx_map = load_map('map_now.tmx')
            hero_pos = [100, 0]
            collisions = []
            collision_rects = get_collision_rects(tmx_map, 1)
            orks.kill()
            orks2.kill()
            orks_exists = False
            two = False
            knight_pos = [500, 1000]
            knight = AnimatedSprite(load_image("Knight.png"), 8, 1, *knight_pos)
            knight_pos2 = [400, 1000]
            knight2 = AnimatedSprite(load_image("Knight.png"), 8, 1, *knight_pos2)
            knight_white_pos = [920, 1000]
            knight_white = AnimatedSprite(load_image("Knight_2.png"), 6, 1, *knight_white_pos)
            knight_walking_pos = [800, 1000]
            knight_walking = AnimatedSprite(load_image("idle.png"), 2, 1, *knight_walking_pos)
            all_sprites.add(knight_walking)
            all_sprites.add(knight)
            all_sprites.add(knight2)
            all_sprites.add(knight_white)
            orks_exists2 = True

        if three and hero.rect.y >= 1100 and hero.rect.x >= 1400:#Переход на 3 локацию
            tmx_map = load_map('Boss1.tmx')
            hero_pos = [0, 200]
            collisions = []
            collision_rects = get_collision_rects(tmx_map, 1)
            original_width = 800
            original_height = 250
            scale_factor = 1.5
            drakon_image = load_image("Drakon3.png")
            scaled_drakon_image = pygame.transform.scale(drakon_image,
                                                         (int(original_width * scale_factor),
                                                          int(original_height * scale_factor)))
            drakon_pos = [600, 150]
            drakon = AnimatedSprite(scaled_drakon_image, 5, 1, *drakon_pos)
            knight_dead_pos = [600, 150]
            knight_dead = AnimatedSprite(load_image("knight_dead.png"), 5, 1, *knight_dead_pos)
            knight_dead_pos2 = [600, 200]
            knight_dead2 = AnimatedSprite(load_image("knight_dead.png"), 5, 1, *knight_dead_pos2)
            all_sprites.add(knight_dead2)
            all_sprites.add(knight_dead)
            all_sprites.add(drakon)
            orks_exists3 = True

        handle_collision(hero, hero_pos, keys, hero_speed, collision_rects)
        screen.fill((0, 0, 0))
        camera.update(hero)

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
            for ork in [orks, orks2]:
                if hero.rect.colliderect(ork.rect):
                    Game()
        if orks_exists2:# 2 локация
            knight.update(True)
            knight2.update(True)
            knight_white.update(True)
            knight_walking.update(True)
            screen.blit(knight2.image, (knight2.rect.x + camera.dx, knight2.rect.y + camera.dy))
            screen.blit(knight.image, (knight.rect.x + camera.dx, knight.rect.y + camera.dy))
            screen.blit(knight_white.image, (knight_white.rect.x + camera.dx, knight_white.rect.y + camera.dy))
            screen.blit(knight_walking.image, (knight_walking.rect.x + camera.dx, knight_walking.rect.y + camera.dy))
        if orks_exists3:# 3 локация
            drakon.update(True)
            screen.blit(drakon.image, (drakon.rect.x + camera.dx, drakon.rect.y + camera.dy))
            knight_dead.rect.x -= 1
            knight_dead.update(True)
            screen.blit(knight_dead.image, (knight_dead.rect.x + camera.dx, knight_dead.rect.y + camera.dy))
            knight_dead2.rect.x -= 1
            knight_dead2.update(True)
            screen.blit(knight_dead2.image, (knight_dead2.rect.x + camera.dx, knight_dead2.rect.y + camera.dy))


        pygame.display.flip()  # Обновление экрана
        clock.tick(fps)
    pygame.quit()
    sys.exit()
