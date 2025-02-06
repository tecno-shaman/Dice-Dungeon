from const import *
from funcs import *
from spritesheet import SpriteSheet
import pygame
import random

pygame.init()

# Variables
x = X0
y = Y0
# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
# Drag-and-Drop area
upper_area = pygame.Rect(100, 450, WIDTH - 200, 150)  # Updated area for dice

# Button dimensions
button_rect = pygame.Rect(WIDTH // 2 - 95, HEIGHT - 100, 200, 50)

# Constants
ROLL_COUNT = 3  # Number of dice to roll each turn
PLAYER_HEALTH = 100

# Game state
dice_list = []
active_dice = None  # Track which dice is currently being dragged


# Dice class
class Dice:
    def __init__(self, value, x, y):
        self.value = value
        self.rect = pygame.Rect(x, y, DICE_SIZE, DICE_SIZE)
        self.dragging = False

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        text = font.render(str(self.value), True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def update_position(self, x, y):
        """Keep the dice within the screen boundaries."""
        self.rect.x = max(0, min(x, WIDTH - DICE_SIZE))
        self.rect.y = max(0, min(y, HEIGHT - DICE_SIZE))


class Entity:
    def __init__(self, name, image, container_values, attack):
        global x, y
        self.name = name
        self.image = SpriteSheet("Assets/Graphics/" + image)
        # self.image = pygame.transform.scale(self.image, IMAGE_SIZE)  # Resize for card
        self.rect = pygame.Rect(x, y, *CARD_SIZE)  # Card dimensions
        x += CARD_SIZE[0] + 5
        y += 0
        self.container = container_values  # List of required dice values
        self.container_slots = [-1] * len(self.container)  # Tracks which slots are filled
        self.container_rects = self._generate_container_rects()
        self.attack = attack
        self.defeated = False

    def _generate_container_rects(self):
        """Generate container slots below the enemy card."""
        rects = []
        x = self.rect.x + 10
        y = self.rect.bottom - DICE_SIZE - 10
        for i in range(len(self.container)):
            rect = pygame.Rect(x + i * (CONTAINER_SLOT_SIZE + 10), y, CONTAINER_SLOT_SIZE, CONTAINER_SLOT_SIZE)
            rects.append(rect)
        return rects

    def is_defeated(self):
        if not self.defeated and all(slot != -1 for slot in self.container_slots):
            self.defeated = True
        return self.defeated

    def add_dice(self, dice):
        """Add a dice to the container if its value matches an open slot and is dropped in that slot."""
        for i, value in enumerate(self.container):
            if self.container_slots[i] == -1 and value == dice.value and self.container_rects[i].collidepoint(
                    dice.rect.center):
                self.container_slots[i] = dice.value
                return True
        return False

    def draw(self, surface):
        if self.defeated:
            # defeated_text = font.render("DEFEATED", True, RED)
            # surface.blit(defeated_text, self.rect.topleft)
            background_image = load_image("card_back.png")
            # background_image = pygame.transform.scale(background_image, IMAGE_SIZE)
            surface.blit(background_image, (self.rect.x, self.rect.y))
            return

        # Draw card background
        pygame.draw.rect(surface, CARD_COLOR, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)

        # Draw image
        surface.blit(self.image.get_current_frame(),
                     (self.rect.x + CARD_SIZE[0] // 2 - 100, self.rect.y + CARD_SIZE[1] // 2 - 64))
        if random.randint(0,1):
            self.image.next_frame()

        # Draw name
        name_text = font.render(self.name, True, BLACK)
        surface.blit(name_text, (self.rect.x + (CARD_SIZE[0] - name_text.get_size()[0]) // 2, self.rect.y))

        # Draw attack strength
        attack_text = small_font.render(f"ATK: {self.attack}", True, RED)
        surface.blit(attack_text, (self.rect.right - 70, self.rect.y + 35))

        # Draw container slots
        for i, rect in enumerate(self.container_rects):
            color = GREEN if self.container_slots[i] != -1 else WHITE
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 2)
            text = small_font.render(str(self.container[i]), True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            surface.blit(text, text_rect)


class Enemy(Entity):
    pass


class Hero:
    def __init__(self, health):
        self.health = health

    def take_damage(self, damage):
        self.health -= damage

    def draw(self, surface):
        health_text = font.render(f"ХП: {self.health}", True, RED)
        surface.blit(health_text, (10, HEIGHT - 50))


def roll_dice():
    """Roll a random D6 and add it to the game area."""
    for _ in range(ROLL_COUNT):
        value = random.randint(1, 6)
        x = random.randint(upper_area.left + 10, upper_area.right - DICE_SIZE - 10)
        y = random.randint(upper_area.top + 10, upper_area.bottom - DICE_SIZE - 10)
        dice_list.append(Dice(value, x, y))


def display_message(screen, text, color):
    """Display a large message on the screen."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Semi-transparent black overlay
    screen.blit(overlay, (0, 0))
    message = font.render(text, True, color)
    text_rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(message, text_rect)
    pygame.display.flip()
    pygame.time.wait(1000)


def handle_game_over(screen, player, enemies):
    global running, game_over_state
    if player.health <= 0:
        game_over_state = "game_over"
        display_message(screen, "Game Over!", RED)
        running = False
    elif all(enemy.is_defeated() for enemy in enemies):
        game_over_state = "victory"
        display_message(screen, "Congratulations! You Won!", GREEN)
        running = False


def start_fight(screen, *args):
    global active_dice
    all_cards = get_enemies()
    enemies = []
    if args:
        for enemy in args:
            enemies.append(Enemy(*all_cards[enemy]))
    else:
        # enemies = [Enemy(*all_cards["snake"]), Enemy(*all_cards["wasp"]), Enemy(*all_cards["thing"])]
        enemies = [Enemy(*all_cards["rat"])]
        print("Подан пустой список врагов")

    player = Hero(PLAYER_HEALTH)
    player_turn = True
    button_state = "roll"  # Tracks the current button state ('roll' or 'end_turn')
    round_number = 1  # Tracks the current round
    game_over_state = None  # None, "victory", or "game_over"

    running = True
    clock = pygame.time.Clock()

    pygame.mixer.init()
    pygame.mixer.music.load("Assets/Sound/anger.mp3")
    pygame.mixer.music.set_volume(0.09)
    pygame.mixer.music.play(-1)

    # Main game loop
    while running:

        # Draw background
        background_image = pygame.image.load("Assets/Graphics/dark_wood_table.jpg").convert()
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        screen.blit(background_image, (0, 0))  # Top-left corner of the screen

        # Draw buttons
        if game_over_state is None:
            pygame.draw.rect(screen, GREEN if button_rect.collidepoint(pygame.mouse.get_pos()) else RED, button_rect)
            button_text = font.render("Бросить кости" if button_state == "roll" else "Конец хода", True, WHITE)
            button_text_rect = button_text.get_rect(center=button_rect.center)
            screen.blit(button_text, button_text_rect)

        # Draw round number
        round_text = font.render(f"Раунд: {round_number}", True, WHITE)
        screen.blit(round_text, (WIDTH - 140, HEIGHT // 12))

        # Draw enemies
        for enemy in enemies:
            enemy.draw(screen)

        # Draw dice
        for dice in dice_list:
            dice.draw(screen)

        # Draw player
        player.draw(screen)

        # Check for game over or victory
        handle_game_over(screen, player, enemies)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_over_state is not None:
                continue  # Ignore events when the game is over

            # Handle mouse press
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Check if button is clicked
                    if button_rect.collidepoint(event.pos) and player_turn:
                        if button_state == "roll":
                            roll_dice()
                            button_state = "end_turn"  # Switch to "End Turn" button
                        elif button_state == "end_turn":
                            # Enemies deal damage
                            total_damage = sum(enemy.attack for enemy in enemies if not enemy.is_defeated())
                            player.take_damage(total_damage)
                            player_turn = False
                            dice_list.clear()
                            button_state = "roll"  # Reset to "Roll Dice" for the next turn
                            round_number += 1  # Increment round number

                    # Check if any dice is clicked
                    for dice in dice_list:
                        if dice.rect.collidepoint(event.pos) and active_dice is None:
                            active_dice = dice
                            dice.dragging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = dice.rect.x - mouse_x
                            offset_y = dice.rect.y - mouse_y
                            break

            # Handle mouse release
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left click
                    if active_dice:
                        active_dice.dragging = False
                        for enemy in enemies:
                            if enemy.add_dice(active_dice):
                                dice_list.remove(active_dice)
                                break
                        active_dice = None

            # Handle mouse motion
            elif event.type == pygame.MOUSEMOTION:
                if active_dice and active_dice.dragging:
                    mouse_x, mouse_y = event.pos
                    active_dice.update_position(mouse_x + offset_x, mouse_y + offset_y)

        # If not player's turn, reset for the next turn
        if not player_turn:
            player_turn = True

        # Update display
        pygame.display.flip()
        clock.tick(30)

    # pygame.quit()


if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()

    # Initialize screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dice Dungeon")
    start_fight(screen)
