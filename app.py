from flask import Flask
from flask import render_template
from flask import jsonify
from flask import abort
from flask import request

import time

from game import BattleshipGame
from game import SHIP_IDS, SHIP_NAMES

app = Flask(__name__)

games = {}

class OverlappingShipsError:
    pass

class ShipsNotSetError:
    pass

@app.route("/")
def index():
    import pdb; pdb.set_trace()
    return render_template("index.html")

@app.route("/game/", methods=["PUT"])
@app.route("/game", methods=["PUT"])
def new_game():
    for (id, game) in games:
        if (time.time() - game.last_touch > 3600):
            del games[id]

    newgame = BattleshipGame()
    games[unicode(newgame.id)] = newgame
    return jsonify(id=unicode(newgame.id))

@app.route("/game/<id>/", methods=["POST"])
@app.route("/game/<id>", methods=["POST"])
def post_turn(id):
    if id not in games:
        return abort(404)

    game = games[id]
    if (len(game.player_ships) == 0):
        abort(400)

    shot = tuple(request.json['shot'])
    shot_result = game.check_shot(shot)
    response_shot = game.make_shot()
    game_over = game.check_game_over()
    return jsonify(hit=shot_result[0], sunk=shot_result[1], 
        ship=shot_result[2], shot=response_shot, game_over=game_over[0],
        winner=game_over[1])

@app.route("/game/<id>/ships", methods=["POST"])
@app.route("/game/<id>/ships/", methods=["POST"])
def post_ships(id):
    if id not in games:
        abort(404)

    game = games[id]

    ships = request.json
    player_ships = []
    for name in SHIP_IDS:
        if name not in ships:
            abort(400)
        player_ships.append((SHIP_IDS[name], set([tuple(point) for point in ships[name]])))

    if not game.place_player_ships(player_ships):
        abort(400)

    return jsonify(ships=dict([(SHIP_NAMES[ship[0]], list(ship[1])) for ship in game.player_ships]))


@app.route("/game/<id>/", methods=["GET"])
def get_status(id):
    if id not in games:
        abort(404)

    game = games[id]

    return jsonify(ships=dict([(SHIP_NAMES[ship[0]], list(ship[1])) for ship in game.player_ships]))

if __name__ == "__main__":
    app.run()