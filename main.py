import os
import pygame
import sys
import pytmx
import random

from funcs import *
from table_top import start_fight


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen_size = (1200, 700)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Dice Dungeon")
        self.clock = pygame.time.Clock()
        self.running = True
        self.hero_speed = 5
        self.fps = 50
        self.inventory = Inventory()
        self.inventory_ui = InventoryUI(self.inventory)
        self.inventory_open = False
        self.hero = Hero("run2.png", 6, 1, 100, 350)
        self.enemies = []
        self.chests = []
        self.load_resources()
        self.state = "menu"

        self.chests.append(Chest(200, 350))

        # Sound
        pygame.mixer.init()
        self.background_music = pygame.mixer.Sound("Assets/Sound/chill.mp3")
        self.chest_sound = pygame.mixer.Sound("Assets/Sound/close_chest.mp3")
        self.inventory_open_sound = pygame.mixer.Sound("Assets/Sound/open_chest.mp3")
        self.inventory_close_sound = pygame.mixer.Sound("Assets/Sound/close_chest.mp3")
        self.fight_sound = pygame.mixer.Sound("Assets/Sound/anger.mp3")
        self.walking_sound = pygame.mixer.Sound("Assets/Sound/mid-fight.mp3")
        self.game_over_sound = pygame.mixer.Sound("Assets/Sound/lose.mp3")
        self.death_scream_sound = pygame.mixer.Sound("Assets/Sound/death_scream.mp3")

        self.background_music.set_volume(0.5)
        self.fight_sound.set_volume(0.5)
        self.walking_sound.set_volume(0.5)
        self.game_over_sound.set_volume(0.5)

    def load_resources(self):
        self.tmx_data = pytmx.util_pygame.load_pygame('map_now1.tmx')  # Загружаем карту
        self.collision_rects = get_collision_rects(self.tmx_data, 1)
        self.spawn_enemies()
        self.chests.append(Chest(200, 350))

    def draw_map(self):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        self.screen.blit(tile, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))

    def spawn_enemies(self):
        enemy_positions = [(400, 200), (400, 400)]
        for pos in enemy_positions:
            self.enemies.append(Enemy("orc.png", 8, 1, *pos))

    def run(self):
        while self.running:
            if self.state == "menu":
                self.show_main_menu()
            elif self.state == "game":
                self.game_loop()
            elif self.state == "results":
                self.show_results_menu()
        pygame.quit()
        sys.exit()

    def game_loop(self):
        self.walking_sound.play(-1)
        while self.state == "game":
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.state = None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                self.inventory_open = not self.inventory_open

    def update(self):
        keys = pygame.key.get_pressed()
        self.hero.move(keys, self.hero_speed, self.collision_rects)
        self.hero.update_animation(True)
        for enemy in self.enemies:
            enemy.move()
            enemy.update_animation(True)
        self.check_interactions()

    def check_interactions(self):
        for chest in self.chests:
            if self.hero.rect.colliderect(chest.rect) and pygame.key.get_pressed()[pygame.K_e]:
                self.chest_sound.play()
                self.inventory.add_item("Coins: " + str(chest.open_chest()))

        for enemy in self.enemies[:]:  # Создаем копию списка, чтобы безопасно удалять элементы
            if self.hero.rect.colliderect(enemy.rect):
                pygame.mixer.stop()
                self.fight_sound.play(-1)
                result = start_fight(self.screen)  # Получаем результат боя
                if result == 1:  # Победа игрока
                    self.enemies.remove(enemy)  # Удаляем врага
                else:  # Поражение
                    self.state = "results"  # Переключаемся на экран завершения игры
                pygame.mixer.stop()

    def render(self):
        self.screen.fill((0, 0, 0))
        self.draw_map()  # Отрисовка карты

        for chest in self.chests:
            self.screen.blit(chest.image, chest.rect.topleft)  # Отрисовка сундуков

        for enemy in self.enemies:
            self.screen.blit(enemy.image, enemy.rect.topleft)  # Отрисовка врагов

        self.screen.blit(self.hero.image, self.hero.rect.topleft)  # Отрисовка героя

        if self.inventory_open:
            self.inventory_ui.draw(self.screen)  # Отрисовка инвентаря

        pygame.display.flip()

    def show_main_menu(self):
        font = pygame.font.Font(None, 80)
        title = font.render("Dice Dungeon", True, (255, 255, 255))
        start_button = pygame.Rect(500, 300, 200, 50)
        quit_button = pygame.Rect(500, 400, 200, 50)
        self.background_music.play(-1)

        while self.state == "menu":
            self.screen.fill((0, 0, 0))
            self.screen.blit(title, (450, 100))
            pygame.draw.rect(self.screen, (100, 100, 255), start_button)
            pygame.draw.rect(self.screen, (255, 100, 100), quit_button)

            font_small = pygame.font.Font(None, 40)
            self.screen.blit(font_small.render("Начать игру", True, (255, 255, 255)), (535, 310))
            self.screen.blit(font_small.render("Выход", True, (255, 255, 255)), (565, 410))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.state = None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        self.state = "game"
                    if quit_button.collidepoint(event.pos):
                        self.running = False
                        self.state = None
        pygame.mixer.stop()

    def show_results_menu(self):
        font = pygame.font.Font(None, 80)
        text = font.render("Игра окончена", True, (255, 255, 255))
        restart_button = pygame.Rect(500, 300, 200, 50)
        quit_button = pygame.Rect(500, 400, 200, 50)

        pygame.mixer.stop()
        self.game_over_sound.play()
        self.death_scream_sound.play()

        while self.state == "results":
            self.screen.fill((0, 0, 0))
            self.screen.blit(text, (500, 100))
            pygame.draw.rect(self.screen, (100, 255, 100), restart_button)
            pygame.draw.rect(self.screen, (255, 100, 100), quit_button)

            font_small = pygame.font.Font(None, 40)
            self.screen.blit(font_small.render("Начать с начала", True, (255, 255, 255)), (545, 310))
            self.screen.blit(font_small.render("Выход", True, (255, 255, 255)), (565, 410))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.state = None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        self.__init__()  # Перезапуск игры
                        self.state = "game"
                    if quit_button.collidepoint(event.pos):
                        self.running = False
                        self.state = None


class Character(pygame.sprite.Sprite):
    def __init__(self, image_path, columns, rows, x, y):
        super().__init__()
        self.frames = []
        self.cut_sheet(load_image(image_path), columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_speed = 0.1
        self.animation_timer = 0

    def cut_sheet(self, sheet, columns, rows):
        frame_width = sheet.get_width() // columns
        frame_height = sheet.get_height() // rows
        for j in range(rows):
            for i in range(columns):
                frame_location = (frame_width * i, frame_height * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, (frame_width, frame_height))))

    def update_animation(self, moving):
        if moving:
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.animation_timer = 0
        else:
            self.cur_frame = 0
        self.image = self.frames[self.cur_frame]


class Hero(Character):
    def move(self, keys, speed, collisions):
        moving = False
        old_pos = self.rect.topleft
        if keys[pygame.K_LEFT]:
            self.rect.x -= speed
            moving = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += speed
            moving = True
        if keys[pygame.K_UP]:
            self.rect.y -= speed
            moving = True
        if keys[pygame.K_DOWN]:
            self.rect.y += speed
            moving = True
        if any(self.rect.colliderect(c) for c in collisions):
            self.rect.topleft = old_pos
        self.update_animation(moving)


class Enemy(Character):
    def __init__(self, image_path, columns, rows, x, y):
        super().__init__(image_path, columns, rows, x, y)
        self.direction = 1

    def move(self):
        self.rect.x += self.direction
        if self.rect.x > 600 or self.rect.x < 400:
            self.direction *= -1


class Chest(Character):
    def __init__(self, x, y):
        super().__init__("chest.png", 1, 4, x, y)
        self.is_open = False

    def open_chest(self):
        if not self.is_open:
            self.is_open = True
            return random.randint(1, 5)
        return 0


class Inventory:
    def __init__(self, size=8):
        self.size = size
        self.items = []

    def add_item(self, item):
        if len(self.items) < self.size:
            self.items.append(item)
            return True
        return False


class InventoryUI:
    def __init__(self, inventory):
        self.inventory = inventory
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        pygame.draw.rect(screen, (50, 50, 50), (50, 50, 400, 300))
        for i, item in enumerate(self.inventory.items):
            text = self.font.render(item, True, (255, 255, 255))
            screen.blit(text, (60, 60 + i * 40))


if __name__ == "__main__":
    game = Game()
    game.run()
