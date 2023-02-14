from dataclasses import dataclass
from config.character_dict import Turret_Dict
T = Turret_Dict()


@dataclass
class Turret:
    name: str
    level: int = 1
    cost: int = 0
    health: int = 0
    attack: int = 0
    defense: int = 0
    attack_speed: int = 1
    range: int = 1
    targets: int = 1
    block: int = 0
    row: int = 0
    column: int = 0

    def update_stats(self):
        selfdict = T.TURRETS.get(self.name)
        self.health = selfdict.get("Health") * self.level
        self.attack = selfdict.get("Attack") * self.level
        self.defense = selfdict.get("Defense") * self.level
        self.attack_speed = selfdict.get("Speed")
        self.block = selfdict.get("Weight")
        self.cost = selfdict.get("Cost")
        self.range = selfdict.get("Range")
        self.targets = selfdict.get("Targets")

    def target_enemy(self, enemies):
        target_list = []
        for enemy in enemies:
            if (enemy.row == self.row or enemy.row == self.row + 1 or enemy.row == self.row - 1) and (enemy.column == self.column or enemy.column == self.column + 1 or enemy.column == self.column - 1):
                target_list.append(enemy)
        if len(target_list) > 0:
            for number in range(self.targets):
                try:
                    target = target_list[number]
                    self.attack_enemy(target)
                except:
                    pass

    def attack_enemy(self, enemy):
        enemy.health -= (self.attack - enemy.defense) * self.attack_speed