def validate_games(input):
    f = open(input, "r")
    games = [validate_game(game) for game in f.readlines()]
    f.close()
    return sum(games)


def validate_game(game):
    game_t, rounds_t = game.split(": ")
    game_n = int(game_t.split(" ")[1])
    rounds = [get_round_map(round) for round in rounds_t.split("; ")]
    rounds_valid = [validate_round(round) for round in rounds]
    if False in rounds_valid:
        return 0
    return game_n


def get_round_map(round):
    cubes = round.split(", ")
    round_map = {}
    for cube in cubes:
        v, k = cube.split(" ")
        round_map[k.strip()] = int(v)
    return round_map


def validate_round(round, limits={"red": 12, "green": 13, "blue": 14}):
    for key in round.keys():
        if round[key] > limits[key]:
            return False
    return True



    
