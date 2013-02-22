import uuid
import random
import time

SHIP_NAMES = {1: "carrier",
              2: "battleship",
              3: "submarine",
              4: "destroyer",
              5: "patrol boat"
}


SHIP_IDS = {"carrier": 1,
            "battleship": 2,
            "submarine": 3,
            "destroyer": 4,
            "patrol boat": 5
}


SHIP_SIZE = {1: 5,
             2: 4,
             3: 3,
             4: 3,
             5: 2
}


class BattleshipGame:
    def __init__(self):
        self.id = uuid.uuid4()
        self.ships = []
        self.player_ships = []
        self.board = set()
        self.shots = set()
        self.last_touch = time.time()
        self.place_ships()

    def place_player_ships(self, player_ships):
        board = set()
        for ship in player_ships:
            if len(ship[1]) != SHIP_SIZE[ship[0]]:
                return False
            if len(board.intersection(ship[1])) > 0:
                return False
            board = board.union(ship[1])

        self.player_ships = player_ships
        return True

    def check_game_over(self):
        if len(self.ships) == 0:
            return (True, "player")
        if len(self.player_ships) == 0:
            return (True, "computer")

        return (False, None)

    def place_ships(self):
        ships = ((1, 5), (2, 4), (3, 3), (4, 3), (5, 2))
        for ship in ships:
            random.seed()
            horiz = (random.randrange(2) == 1)
            placed = False
            points = None
            while not placed:
                if (horiz):
                    startX = random.randrange(10 - ship[1])
                    y = random.randrange(10)
                    points = [(x, y) for x in range(startX, startX + ship[1])]
                    placed = True
                    for point in points:
                        if point in self.board:
                            placed = False
                else:
                    startY = random.randrange(10 - ship[1])
                    x = random.randrange(10)
                    points = [(x, y) for y in range(startY, startY + ship[1])]
                    placed = True
                    for point in points:
                        if point in self.board:
                            placed = False

            self.board.update(points)
            self.ships.append((ship[0], set(points)))

    def check_shot(self, shot):
        hit = False
        sunk = False
        ship = None
        for curship in self.ships:
            if shot in curship[1]:
                hit = True
                curship[1].remove(shot)
                if (len(curship[1]) == 0):
                    sunk = True
                    ship = SHIP_NAMES[ship[0]]
                    self.ships.remove(curship)

        return (hit, sunk, ship)

    def check_shot_player(self, shot):
        hit = False
        sunk = False
        ship = None
        for curship in self.player_ships:
            if shot in curship[1]:
                hit = True
                curship[1].remove(shot)
                if (len(curship[1]) == 0):
                    sunk = True
                    ship = SHIP_NAMES[ship[0]]
                    self.player_ships.remove(curship)

        return {"hit": hit, "sunk": sunk, "ship": ship}

    def make_shot(self):
        board = set([(x, y) for x in range(10) for y in range(10)])
        board -= self.shots
        shot = random.sample(board, 1)[0]
        self.shots.add(shot)
        check = self.check_shot_player(shot)
        return (shot, check)
