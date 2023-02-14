import random
import sys
sys.path.append("./assets")
sys.path.append("./classes")
sys.path.append("./config")
import pygame
pygame.init()
from classes.map import *
from classes.enemy import *
from classes.turret import Turret
from config.character_dict import *

FONT = pygame.font.SysFont("comicsans", 25)
WIN = pygame.display.set_mode((1200, 1000), pygame.RESIZABLE)


class Tower_Defense_Game:
    def __init__(self, size: int = 5, levels: int = 1, enemies: list[Enemy] = None, turrets: list[Turret] = None):
        self.size = size
        self.levels = levels
        self.enemies = enemies
        self.turrets = turrets
        self.MAP = Map(self.size)
        self.squares = [[None for x in range(self.size)] for x in range(self.size)]
        self.turret = None
        self.update_dimensions()
        self.MAP.generate_map()
        self.make_turret_list()

    def update_dimensions(self):
        self.width = WIN.get_width()
        self.height = WIN.get_height()

    def make_turret_list(self):
        self.turret_texts = []
        self.turret_rects = []
        counter = 1
        for turret in self.turrets:
            turret_text = FONT.render(turret.name, 1, (255, 255, 255))
            turret_rect = pygame.Rect(self.width-turret_text.get_width(), (self.height//3)+(counter*turret_text.get_height()), turret_text.get_width(), turret_text.get_height())
            self.turret_texts.append(turret_text)
            self.turret_rects.append(turret_rect)
            counter += 1

    def draw_turret_lists(self):
        counter = 1
        for turret_rect in self.turret_rects:
            pygame.draw.rect(WIN, (0, 100, 0), turret_rect)
        for turret_text in self.turret_texts:
            WIN.blit(turret_text, (self.width-turret_text.get_width(), (self.height//3)+(counter*turret_text.get_height())))
            counter += 1

    def draw_self_turret(self):
        pygame.draw.rect(WIN, (0, 0, 0), pygame.Rect(self.width-200, 0, 200, 200))
        try:
            text = FONT.render(str(self.turret.name), 1, (250, 250, 250))
        except:
            text = FONT.render("None", 1, (250, 250, 250))
        WIN.blit(text, (self.width-text.get_width(), 0))

    def draw_square(self, width, height, x, y):
        square = pygame.Rect(width, height, 50, 50)
        self.squares[x][y] = square
        color = (150, 150, 150)
        if self.MAP.grid[x][y].value > 0:
            color = (100, 200, 200)
        elif self.MAP.grid[x][y].value == -1:
            color = (150, 0, 0)
        if x == y == 0:
            color = (0, 0, 150)
        pygame.draw.rect(WIN, color, square)

    def draw_map(self):
        total_dim = 50 * self.size
        width = (self.width - total_dim)//2
        height = (self.height - total_dim)//2
        for x in range(self.size):
            for y in range(self.size):
                self.draw_square(width, height, x, y)
                height += 50
            height = (self.height - total_dim)//2
            width += 50
        pygame.display.flip()

    def initialize_turrets(self):
        for turret in self.turrets:
            turret.update_stats()

    def initialize_enemies(self):
        for enemy in self.enemies:
            enemy.update_map(self.MAP)
            enemy.update_stats()

    def update_map(self):
        self.MAP.find_shortest_path()
        for enemy in self.enemies:
            enemy.update_map(self.MAP)

    def update_enemy_hp(self):
        for enemy in self.enemies:
            if enemy.health <= 0:
                self.enemies.remove(enemy)

    def update_enemy_position(self):
        for enemy in self.enemies:
            enemy.move_to_next_tile()
            if enemy.row == enemy.column == self.size -1:
                enemy.row = 0
                enemy.column = 0
        
    def draw_enemies(self):
        for enemy in self.enemies:
            x = ((self.width-(50 * self.size))//2)+(enemy.row*50)+25+random.randint(-5, 5)
            y = ((self.height-(50 * self.size))//2)+(enemy.column*50)+25+random.randint(-5, 5)
            pygame.draw.circle(WIN, (150, 0, 0), (x, y), 20)

    def find_active_turrets(self):
        self.active_turrets: list[Turret] = []
        for x in range(self.size):
            for y in range(self.size):
                if self.MAP.turrets[x][y] != None:
                    self.active_turrets.append(self.MAP.turrets[x][y])
        self.turret_actions()

    def turret_actions(self):
        for turret in self.active_turrets:
            turret.target_enemy(self.enemies)
        self.update_enemy_hp()

    def game_loop(self):
        self.game = True
        self.draw_turret_lists()
        self.draw_self_turret()
        self.MAP.find_shortest_path()
        self.initialize_enemies()
        self.initialize_turrets()
        while self.game:
            self.draw_map()
            self.draw_enemies()
            self.find_active_turrets()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (x, y) = pygame.mouse.get_pos()
                    click = pygame.Rect(x, y, 1, 1)
                    for nx in range(self.size):
                        for ny in range(self.size):
                            if self.squares[nx][ny].contains(click):
                                if event.button == 1:
                                    if self.turret == None:
                                        self.MAP.place_block(nx, ny)
                                    else:
                                        self.MAP.place_turret(self.turret, nx, ny)
                                elif event.button == 3:
                                    self.MAP.remove_block(nx, ny)
                                self.update_map()
                    for turret_rect in self.turret_rects:
                        if turret_rect.contains(click):
                            index = self.turret_rects.index(turret_rect)
                            self.turret = self.turrets[index]
                            self.draw_self_turret()
            pygame.display.update()
            pygame.time.delay(100)
            self.update_enemy_position()

tdg = Tower_Defense_Game(13, 1, [Enemy("Goblin")], [Turret("Basic")])
tdg.game_loop()