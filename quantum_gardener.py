import pygame
import random
import sys
import os
from enum import Enum

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Настройки экрана
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Quantum Gardener")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)

# Состояния растений
class PlantState(Enum):
    SEED = 0
    ALIVE = 1
    DEAD = 2
    FLOWER = 3
    POISON = 4

class QuantumPlant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.states = [PlantState.ALIVE, PlantState.FLOWER, PlantState.POISON]
        self.current_state = None
        self.entangled = None
        self.growth_time = random.randint(5, 15)
        self.age = 0
        self.image = self.load_image("seed")

    def load_image(self, name):
        try:
            return pygame.image.load(f"assets/{name}.png").convert_alpha()
        except:
            # Заглушка, если изображение не найдено
            surf = pygame.Surface((40, 40), pygame.SRCALPHA)
            color = {
                "seed": (100, 100, 100),
                "alive": GREEN,
                "dead": (150, 75, 0),
                "flower": (255, 192, 203),
                "poison": (128, 0, 128)
            }.get(name, BLACK)
            pygame.draw.circle(surf, color, (20, 20), 20)
            return surf

    def update(self):
        self.age += 0.1
        if self.age >= self.growth_time and not self.current_state:
            self.observe()

    def observe(self):
        self.current_state = random.choice(self.states)
        if self.entangled:
            self.entangled.current_state = self.current_state
        self.update_image()
        return self.current_state

    def update_image(self):
        images = {
            PlantState.SEED: "seed",
            PlantState.ALIVE: "alive",
            PlantState.DEAD: "dead",
            PlantState.FLOWER: "flower",
            PlantState.POISON: "poison"
        }
        self.image = self.load_image(images.get(self.current_state, "seed"))

    def draw(self, surface):
        surface.blit(self.image, (self.x - 20, self.y - 20))

class Game:
    def __init__(self):
        self.plants = []
        self.font = pygame.font.SysFont("Arial", 24)
        self.sounds = {
            "plant": self.load_sound("plant"),
            "collapse": self.load_sound("collapse")
        }
        self.load_assets()

    def load_sound(self, name):
        try:
            return pygame.mixer.Sound(f"assets/{name}.wav")
        except:
            # Заглушка, если звука нет
            return pygame.mixer.Sound(buffer=bytearray(100))

    def load_assets(self):
        # Создаем папку assets, если её нет
        if not os.path.exists("assets"):
            os.makedirs("assets")

    def add_plant(self, x, y):
        new_plant = QuantumPlant(x, y)
        if len(self.plants) > 0 and random.random() < 0.3:
            new_plant.entangled = random.choice(self.plants)
        self.plants.append(new_plant)
        self.sounds["plant"].play()

    def update(self):
        for plant in self.plants:
            plant.update()

    def draw(self, surface):
        surface.fill(WHITE)
        for plant in self.plants:
            plant.draw(surface)
        self.draw_ui(surface)
        pygame.display.flip()

    def draw_ui(self, surface):
        text = self.font.render(f"Растений: {len(self.plants)}", True, BLACK)
        surface.blit(text, (10, 10))
        text2 = self.font.render("ЛКМ: посадить, ПКМ: наблюдать", True, BLACK)
        surface.blit(text2, (10, 40))

def main():
    game = Game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # ЛКМ
                    game.add_plant(*event.pos)
                elif event.button == 3:  # ПКМ
                    for plant in game.plants:
                        if ((plant.x - event.pos[0])**2 + (plant.y - event.pos[1])**2) <= 900:
                            plant.observe()
                            game.sounds["collapse"].play()

        game.update()
        game.draw(screen)
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
