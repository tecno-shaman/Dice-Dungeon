from const import *
from funcs import *
import pygame
import random

# Initialize Pygame
pygame.init()

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dice_Dungeon")

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Drag-and-Drop area
drag_area = pygame.Rect(100, 100, 600, 300)

# Button dimensions
button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT - 100, 150, 50)


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
        """Update position while keeping the dice within the drag area."""
        self.rect.x = max(drag_area.left, min(x, drag_area.right - DICE_SIZE))
        self.rect.y = max(drag_area.top, min(y, drag_area.bottom - DICE_SIZE))

class Entity:
    def __init__(self, name, image, container_values):
        self.name = name
        self.image = load_image(image)
        self.image = pygame.transform.scale(self.image, IMAGE_SIZE)  # Resize for card
        self.rect = pygame.Rect(0, 0, *CARD_SIZE)  # Card dimensions
        self.container = container_values  # List of required dice values
        self.container_slots = []  # Tracks which slots are filled
        self.container_rects = self._generate_container_rects(10, CARD_SIZE[1] - DICE_SIZE - 10)

    def _generate_container_rects(self, x, y):
        """Generate container slots below the enemy card."""
        rects = []
        for i in range(len(self.container)):
            rect = pygame.Rect(x + i * (CONTAINER_SLOT_SIZE + 10), y, CONTAINER_SLOT_SIZE, CONTAINER_SLOT_SIZE)
            rects.append(rect)
        return rects

    def is_defeated(self):
        return len(self.container_slots) == len(self.container)

    def add_dice(self, dice):
        """Add a dice to the container if its value matches an open slot."""
        for i, value in enumerate(self.container):
            if i not in self.container_slots and value == dice.value:
                self.container_slots.append(i)
                return True
        return False

    def draw(self, surface, x):
        # Draw card
        pygame.draw.rect(surface, CARD_COLOR, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        surface.blit(self.image, (x + 25, y + 10))
        name_text = font.render(self.name, True, BLACK)
        surface.blit(name_text, (x + 10, y + 120))

        # Draw container
        for i, rect in enumerate(self.container_rects):
            color = GREEN if i in self.container_slots else WHITE
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 2)
            text = small_font.render(str(self.container[i]), True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            surface.blit(text, text_rect)
# Enemy class
class Enemy(Entity):
    pass


# Game state
dice_list = []
enemies = [
    Enemy("Goblin", "ghost.png", [3, 4, 6]),
    Enemy("Orc","ghost.png", [2, 5, 6]),
    Enemy("Dragon", "ghost.png", [5, 6, 6]),
]

running = True
clock = pygame.time.Clock()


def roll_dice():
    """Roll a random D6 and add it to the game area."""
    value = random.randint(1, 6)
    x = random.randint(drag_area.left + 10, drag_area.right - DICE_SIZE - 10)
    y = random.randint(drag_area.top + 10, drag_area.bottom - DICE_SIZE - 10)
    dice_list.append(Dice(value, x, y))


# Main game loop
while running:

    # Draw background
    background_image = pygame.image.load("Assets/Graphics/dark_wood_table.jpg").convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    screen.blit(background_image, (0, 0))  # Top-left corner of the screen

    # Draw the drag area
    pygame.draw.rect(screen, RED, drag_area, 2)

    # Draw the button
    pygame.draw.rect(screen, GREEN if button_rect.collidepoint(pygame.mouse.get_pos()) else RED, button_rect)
    button_text = font.render("Roll Dice", True, WHITE)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)

    # Draw enemies
    x = 10
    y = 10
    for enemy in enemies:
        enemy.draw(screen, x)
        x += CARD_SIZE[0]

    # Draw dice
    for dice in dice_list:
        dice.draw(screen)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse press
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Check if button is clicked
                if button_rect.collidepoint(event.pos):
                    roll_dice()
                # Check if any dice is clicked
                for dice in dice_list:
                    if dice.rect.collidepoint(event.pos):
                        dice.dragging = True
                        mouse_x, mouse_y = event.pos
                        offset_x = dice.rect.x - mouse_x
                        offset_y = dice.rect.y - mouse_y

        # Handle mouse release
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click
                for dice in dice_list:
                    dice.dragging = False
                    for enemy in enemies:
                        if enemy.rect.collidepoint(dice.rect.center):
                            if enemy.add_dice(dice):
                                dice_list.remove(dice)
                                break

        # Handle mouse motion
        elif event.type == pygame.MOUSEMOTION:
            for dice in dice_list:
                if dice.dragging:
                    mouse_x, mouse_y = event.pos
                    dice.update_position(mouse_x + offset_x, mouse_y + offset_y)

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
