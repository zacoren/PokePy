import math
import random

# lists type effectiveness
element_def_weaknesses = {
    "BUG": ["FIRE", "FLYING"],
    "DRAGON": [None],
    "ELECTRIC": ["ELECTRIC", "GRASS"],
    "FIGHTING": ["FLYING", "PSYCHIC"],
    "FIRE": ["ROCK", "WATER"],
    "FLYING": ["ELECTRIC", "ROCK"],
    "GHOST": [None],
    "GRASS": ["BUG", "FIRE", "FLYING", "GRASS", "POISON"],
    "GROUND": ["GRASS"],
    "ICE": ["ICE", "WATER"],
    "NORMAL": [None],
    "POISON": ["GROUND", "POISON", "ROCK"],
    "PSYCHIC": ["PSYCHIC"],
    "ROCK": ["FIGHTING", "ROCK"],
    "WATER": ["GRASS", "ICE"]}
element_att_strengths = {
    "BUG": ["GRASS", "POISON", "PSYCHIC"],
    "DRAGON": [None],
    "ELECTRIC": ["FLYING", "WATER"],
    "FIGHTING": ["ICE", "NORMAL", "ROCK"],
    "FIRE": ["BUG", "GRASS", "ICE"],
    "FLYING": ["BUG", "FIGHTING", "GRASS"],
    "GHOST": [None],
    "GRASS": ["GROUND", "ROCK", "WATER"],
    "GROUND": ["ELECTRIC", "FIRE", "POISON", "ROCK"],
    "ICE": ["DRAGON", "FLYING", "GRASS", "GROUND"],
    "NORMAL": [None],
    "POISON": ["BUG", "GRASS"],
    "PSYCHIC": ["FIGHTING", "POISON"],
    "ROCK": ["BUG", "FIRE", "FLYING", "ICE"],
    "WATER": ["FIRE", "GROUND", "ROCK"]
}
element_no_effect = {
    "ELECTRIC": ["GROUND"],
    "FLYING": ["GHOST"],
    "GHOST": ["NORMAL", "PSYCHIC"],
    "GROUND": ["FLYING"],
    "NORMAL": ["GHOST"]
}


# returns a function that modifies pokemon behavior based on move statuses
def status_effects(status):
    pass


# defines moves and their abilities HORRIBLY UNFINISHED
class Move:

    def __init__(self, type, damage, accuracy=100, status_effects=None):
        self.type = type
        self.damage = damage
        self.accuracy = accuracy
        self.status_effects = status_effects

    # returns weather STAB is available, and returns super/not-very effectiveness
    def get_effective(self, pokemon, op_pokemon):
        stab = False
        effectiveness = 1
        # determines if the move has no effect
        if (self.type in element_no_effect) and (op_pokemon.type in element_no_effect[self.type]):
            effectiveness = 0
            return effectiveness
        # checking for STAB (same-type attack bonus
        elif self.type in pokemon.elements:
            stab = True
        # checking if the type is Super-Effective
        for element in element_att_strengths[op_pokemon.type]:
            if self.type == element:
                effectiveness *= 2
        # checking if type is "not that effective"
        for element in element_def_weaknesses[op_pokemon.type]:
            if self.type == element:
                effectiveness /= 2
        if stab:
            effectiveness *= 1.5
        return effectiveness

    #will return weather or not a move hits
    def accuracy(self, pokemon, op_pokemon):
        pass


# Defines trainer class, will be used to super() player class later.
class Trainer:
    pass


class Pokemon:
    # xp_yield = (wild/owned * traded * base xp * feinted level)/7 * number in battle not feinted /not implemented

    # initializes pokemon stats
    def __init__(self, name, elements, pokemon, gender, base_stats, evolutions=None,
                 ev={"HP": 0, "ATTACK": 0, "DEFENSE": 0, "SPEED": 0, "SPECIAL": 0}, lvl=5,
                 needs_stone=False):
        self.needs_stone = needs_stone
        self.name = name
        self.lvl = lvl
        self.base_stats = base_stats
        self.EV = ev
        self.IV = {stat: random.randint(0, 15) for stat in self.base_stats.keys() if stat != "HP"}
        hp_binary = ''
        for item in self.IV.values():
            hp_binary += str(bin(item)[-1])
        self.IV["HP"] = int(hp_binary, 2)

        self.hp = math.floor((math.floor(((self.base_stats["HP"] + self.IV["HP"]) * 2 + math.floor(
            math.ceil(math.sqrt(self.EV["HP"])) / 4)) * self.lvl) / 100) + self.lvl + 10)

        self.battle_stats = {stat: int(math.floor((((self.base_stats[stat] + self.IV[stat]) * 2 + math.floor(
            math.ceil(math.sqrt(self.EV[stat])) / 4)) * self.lvl) / 100) + 5) for stat in self.base_stats.keys() if
                             stat != "HP"}

        self.current_hp = self.hp
        self.xp = self.lvl ** 3
        self.xp_to_next = (self.lvl + 1) ** 3
        self.elements = elements
        self.pokemon = pokemon
        self.gender = gender
        self.moves = []
        self.evolutions = evolutions

    # prints a description of the pokemon
    def __repr__(self):
        if self.gender == "Male":
            return "{0} is a lvl {1} {2}, he has {3} HP and knows the moves: {4}".format(self.name,
                                                                                         self.lvl,
                                                                                         self.pokemon,
                                                                                         self.current_hp,
                                                                                         self.moves)
        elif self.gender == "Female":
            return "{0} is a lvl {1} {2}, she has {3} HP and knows the moves: {4}".format(self.name,
                                                                                          self.lvl,
                                                                                          self.pokemon,
                                                                                          self.current_hp,
                                                                                          self.moves)

    # calculates EV gain of a pokemon when called (usually after a battle)
    def Ev_gain(self, op_pokemon):
        for stat in op_pokemon.base_stats:
            self.EV[stat] += op_pokemon.base_stats[stat]

    # changes pokemon level, unfinished/needs to check possible moves to learn
    def Level_up(self):
        if self.lvl < 100:
            self.lvl += 1
            self.hp = math.floor((math.floor(((self.base_stats["HP"] + self.IV["HP"]) * 2 + math.floor(
                math.ceil(math.sqrt(self.EV["HP"])) / 4)) * self.lvl) / 100) + self.lvl + 10)
            self.battle_stats = {stat: int(math.floor((((self.base_stats[stat] + self.IV[stat]) * 2 + math.floor(
                math.ceil(math.sqrt(self.EV[stat])) / 4)) * self.lvl) / 100) + 5) for stat in self.base_stats.keys() if
                                 stat != "HP"}
            self.xp_to_next = (self.lvl + 1) ** 3
            # weather or not the pokemon evolves
            if self.evolutions is not None:
                if self.lvl == self.evolutions[0][0]:
                    self.pokemon = self.evolutions[0][1]

    # adds earned xp to pokemons xp and calls the level_up function if they earned enough to be at the next level
    def Xp_gain(self, xp_earned):
        self.xp += xp_earned
        if self.xp == self.xp_to_next:
            self.Level_up()


# basic function for randomizing gender , takes r, ratio of male to females. higher ratio means more females
# r should always be a number between 0 and 1, if no ratio is defined then it is always 50/50
def get_gender(r = .5):
    g = random.randint(0, 100)
    if g >= r*100:
        return "Male"
    else:
        return "Female"


# new code to change the games difficulty curve, randomly generated pokemon will be at a level equal to the average level
# of the trainers current roster. default level is between 1 and 5
def pokemon_level(team=None):
    if team is None:
        return random.randint(1,5)
    else:
        level = 0
        for pokemon in team:
            level += pokemon.lvl
        level /= len(team)
        return level


# example of defining each species of pokemon's specific traits
# defining each pokemon's base characteristics, to do: add all pokemon's learnable moves.
class Bulbasaur(Pokemon):
    def __init__(self, name="Bulbasaur"):
        elements = ["GRASS", "POISON"]
        gender = get_gender()
        base_stats = {"HP": 45, "ATTACK": 49, "DEFENSE": 45, "SPEED": 45, "SPECIAL": 65}
        pokemon_n = 1

        super().__init__(name, elements, pokemon_n, gender, base_stats)
class Ivysaur(Pokemon):

    def __init__(self, name= "Ivysaur"):
        elements = ["GRASS, POISON"],
        pokemon_n = 2
        gender = get_gender()
        base_stats = {"HP":60,"ATTACK":62,"DEFENSE":63,"SPEED":60,"SPECIAL":80}
        evolutions={"Venusaur":[32,3]}

        super().__init__(name, elements, pokemon_n, gender, base_stats)

class Venusaur(Pokemon):
    def __init__(self, name="Venusaur"):
        elements = ["GRASS", "POISON"],
        pokemon_n = 3
        gender = get_gender()
        base_stats = {"HP":80,"ATTACK":82,"DEFENSE":83, "SPEED":80,"SPECIAL":100}

        super().__init__(name, elements, pokemon_n, gender, base_stats)

class Charmander(Pokemon):
    def __init__(self, name = "Charmander"):
        elements = ["FIRE"]
        pokemon_n = 4
        gender = get_gender()
        base_stats = {"HP":39,"ATTACK":52, "DEFENSE":43,"SPEED":65,"SPECIAL":50}
        evolutions={"Charmeleon":[16,4]})

        super().__init__(name, elements, pokemon_n, gender, base_stats, evolutions)

class Charmeleon(Pokemon):
    def __init__(self, name = "Charmeleon"):
        elements =  ["FIRE"]
        pokemon_n = 5
        gender = get_gender()
        base_stats = {"HP":58,"ATTACK":64,"DEFENSE":58,"SPEED":80,"SPECIAL":65}

        super().__init__(name, elements, pokemon_n, gender, base_stats)

class Charizard(Pokemon):
    def __init__(self, name = "Charizard"):
        elements = ["FIRE"]
        pokemon_n = 6
        gender = get_gender()
        base_stats = {"HP": 78,"ATTACK": 84,"DEFENSE": 78, "SPEED": 100, "SPECIAL": 86}

        super().__init__(name, elements, pokemon_n, gender, base_stats)

class Squirtle(Pokemon):
    def __init__(self, name = "Squirtle"):
        elements = ["WATER"]
        pokemon_n = 7
        gender = get_gender()
        base_stats = {"HP": ,"ATTACK": ,"DEFENSE": , "SPEED": , "SPECIAL":}

        super().__init__(name, elements, pokemon_n, gender, base_stats)
# empty pokemon creation class
"""class (Pokemon):
    def __init__(self, name = ""):
        elements = []
        pokemon_n =
        gender = get_gender()
        base_stats = {"HP": ,"ATTACK": ,"DEFENSE": , "SPEED": , "SPECIAL"}

        super().__init__(name, elements, pokemon_n, gender, base_stats)
"""
    #  i did this for some reason, and i forgot, could be useful later
"""pokemon = {
        0:None,
        1: bulbasaur, 2: ivysaur, 3: venusaur,
        4: charmander, 5: charmeleon, 6:charizard,
        7: squirtle, 8: wartortle, 9: blastoise,
        10: caterpie,11:metapod, 12:butterfree,
        13: weedle, 14: kakuna, 15:beedrill,
        16: pidgey, 17: pidgeotto, 18: pidgeot,
        19: rattata, 20: raticate,
        21: spearow, 22: fearow,
        23: ekans, 24: arbok,
        25: pikachu, 26: raichu,
        27: sandshrew, 28: sandslash,
        29: nidoran♀, 30: nidorina, 31: nidoqueen,
        32: nidoran♂, 33: nidorino, 34: nidoking,
        35: clefairy, 36: clefable ,
        37: vulpix, 38: ninetales,
        39: jigglypuff ,40: wigglytuff,
        41: zubat, 42: golbat,
        43: oddish, 44: gloom ,45: vileplume,
        46: paras, 47: parasect ,
        48: venonat, 49: venomoth,
        50: diglett, 51: dugtrio,
        52: meowth, 53: persian,
        54: psyduck, 55: golduck,
        56: mankey, 57: primeape,
        58: growlithe, 59: arcanine,
        60: poliwag, 61: poliwhirl, 62: poliwrath,
        63: abra, 64: kedabra, 65: alakazam,
        66: machop, 67: machoke, 68: machamp,
        69: bellsprout, 70: weepinbell, 71: victreebel,
        72: tentacool, 73: tentacruel,
        74: geodude, 75: graveler, 76: golem,
        77: ponyta, 78: rapidash ,
        79: slowpoke, 80: slowbro,
        81: magnemite, 82:magneton,
        83: farfetchd,
        84: doduo, 85: dodrio,
        86: seel, 87: dewgong,
        88: grimer, 89: muk,
        90: shellder, 91: cloyster,
        92: gastly, 93: haunter, 94: gengar,
        95: onyx,
        96: drowzee, 97: hypno,
        98: crabby, 99: kingler,
        100: voltorb, 101: electrode,
        102: exeggcute, 103: exeggutor,
        104: cubone, 105: marowak,
        106: hitmonlee, 107: hitmonchan,
        108: lickitung,
        109: koffing, 110: weezing,
        111: ryhorn,
        112: rhydon,
        113: chansey,
        114: tangela,
        115: kangaskhan,
        116: horsea, 117: seadra,
        118: goldeen, 119: seaking,
        120: staryu, 121: starmie,
        122: Mr_Mime,
        123: Scyther,
        124: jynx,
        125: electabuzz,
        126: magmar,
        127: pinsir,
        128: tauros,
        129: magikarp, 130: gyarados,
        131: lapras,
        132: ditto,
        133: eevee, 134: vaporeon, 135: jolteon, 136: flareon,
        137: porygon,
        138: omanyte, 139: omastar,
        140: kabuto, 141: kabutops,
        142: aerodactyl,
        143: snorlax,
        144: articuno,
        145: zapdos,
        146: moltres,
        147: dratini, 148: dragonair, 149: dragonite,
        150: mewtwo,
        151: mew}"""


def get_pokemon_name(n):
    name = str(pokemon[n])


bulbasaur = Bulbasaur()
bulbasaur2 = Bulbasaur()
print(bulbasaur)
print(bulbasaur2)
