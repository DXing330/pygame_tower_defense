from dataclasses import dataclass
from classes.map import *
from config.character_dict import Enemy_Dict
E = Enemy_Dict()


@dataclass
class Enemy:
    name: str
    level: int = 1
    health: int = 0
    attack: int = 0
    defense: int = 0
    speed: int = 1
    weight: int = 1
    map: Map = None
    row: int = 0
    column: int = 0
    image = None

    def update_stats(self):
        selfdict = E.ENEMIES.get(self.name)
        self.health = selfdict.get("Health") * self.level
        self.attack = selfdict.get("Attack") * self.level
        self.defense = selfdict.get("Defense") * self.level
        self.speed = selfdict.get("Speed")

    def update_map(self, map: Map):
        self.map = map

    def move_to_next_tile(self):
        node: Node = self.map.previous_node[self.row][self.column]
        try:
            self.row = node.row
            self.column = node.column
        except:
            pass

    def attack_blocker(self, blocker):
        pass