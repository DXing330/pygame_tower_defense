class Enemy_Dict:
    def __init__(self):
        self.ENEMIES = {
        "Goblin" : {"Health" : 5, "Attack" : 2, "Defense" : 1, "Speed" : 1, "Weight" : 1}
        }


class Turret_Dict:
    def __init__(self):
        self.TURRETS = {
            "Basic" : {"Health" : 5, "Attack" : 5, "Defense" : 1, "Speed" : 1, "Weight" : 0, "Cost" : 3, "Range" : 3, "Targets" : 1}
        }