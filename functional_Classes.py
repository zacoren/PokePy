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


# function to evolve pokemon, todo integrate it into the trainer class to check when a pokemon evolves,
#  add in stone functionality for eevee, possibly loaning for move "transform" for ditto and mew
def Evolve(pokemon):
    if pokemon.named:
        new_evolution = pokemon_list[pokemon.evolution(
            pokemon.name, pokemon.lvl, ivs=pokemon.IV, evs=pokemon.EV)]
    else:
        new_evolution = pokemon_list[pokemon.evolution](lvl=pokemon.lvl, ivs=pokemon.IV, evs=pokemon.EV)
    return new_evolution


# new code to change the games difficulty curve,
# randomly generated pokemon will be at a level equal to the average level
# of the trainers current roster. default level is between 3 and 5
def pokemon_level(team=None):
    if team is None:
        return random.randint(3, 5)
    else:
        level = 0
        for pokemon in team:
            level += pokemon.lvl
        level /= len(team)
        return level


# basic function for randomizing gender , takes r, ratio of male to females. higher ratio means more females
# r should always be a number between 0 and 1, if no ratio is defined then it is always 50/50
def get_gender(r=.5):
    g = random.randint(0, 100)
    if g <= r * 100:
        return "Male"
    else:
        return "Female"


# function that appends status effects and changes pokemon behavior /unfinished
def status_effects():
    pass


# Helper functions for ivs and evs
def ivs_starter(ivs=None):
    return ivs


def evs_starter(evs=None):
    return evs

# defines how many times the ball shakes before the pokemon breaks loose /unfinished
"""def ball_shake(pokemon, ball):
    def find_d():
        if ball is "Pokeball":
            d = pokemon.catch_rate * (100/255)
        elif ball is "Ultra Ball":
            d = pokemon.catch_rate * (100/ 200)
        else:
            d = pokemon.catch_rate * (100/ 150)
        return d
    if find_d() >= 256:
        return 3
    else:
        x = find_d() *"""


# defines moves and their abilities HORRIBLY UNFINISHED
class Move:

    def __init__(self, element, damage, accuracy: int = 100, status_effect=None):
        self.type = element
        self.damage = damage
        self.accuracy = accuracy
        self.status_effects = status_effect

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

    # will return weather or not a move hits /unfinished
    def accuracy(self, pokemon, op_pokemon):
        pass


# Defines trainer class, will be used to super() player class later, and possibly specific types of trainers /unfinished
class Trainer:
    def __init__(self, name, money=0, items=None, pokemon=None):
        self.name = name
        self.pokemon = []
        if pokemon is not None:
            self.pokemon = pokemon
        self.money = money
        self.items = items


# Defines the player itself, will be used when creating the player instance. /unfinished
class Hero(Trainer):
    def __init__(self, name="Red", gender=None):
        self.gender = gender
        super().__init__(name, 0)
        self.boxes = [[], [], [], [], [], [], [], [], [], []]
        self.current_box = self.boxes[0]

    def __repr__(self):
        player_pokemon = [pokemon.name for pokemon in self.pokemon]
        return "{0} is a {1} with ${2} and their pokemon are {3}".format(
            self.name, self.gender, self.money, player_pokemon)

    # function used for catching pokemon, mainly hear to shorten the length of the code, if pokemon roster is full,
    # it will automatically find a box with space todo, add an exception for when you have no more space in any box
    def pokemon_caught(self, pokemon):
        if len(self.pokemon) <= 6:
            self.pokemon.append(pokemon)
            print("You caught {0}".format(pokemon.name))
            return
        else:
            print("You already have 6 pokemon on your team, so the pokemon was sent to your Box")
            if len(self.current_box) < 25:
                self.current_box.append(pokemon)
                return
            else:
                i = 0
                while len(self.current_box) == 25:
                    i += 1
                    self.current_box = self.boxes[i]
                self.current_box.append(pokemon)
                return

    # defines a players ability to catch pokemon /functional but needs work for interactivity and possibly more added
    def Catch_pokemon(self, pokeball, pokemon):
        if pokeball == "Masterball":
            self.items["Pokeball"][pokeball] -= 1
            self.pokemon_caught(pokemon)
        else:
            # returns a number based on the pokeball used and decrements the number of that pokeball
            def get_catch_chance():
                if pokeball == "Pokeball":
                    chance = random.randint(0, 255)
                    self.items["Pokeball"][pokeball] -= 1
                elif pokeball == "GreatBall":
                    chance = random.randint(0, 200)
                    self.items["Pokeball"][pokeball] -= 1
                else:
                    chance = random.randint(0, 150)
                    self.items["Pokeball"][pokeball] -= 1
                return chance

            catch_chance = get_catch_chance()

            # should return a new number based on status effects or outright catch the pokemon
            def status_catch(current_chance):
                new_chance = current_chance
                if "asleep" in pokemon.status or "frozen" in pokemon.status:
                    if new_chance < 25:
                        self.pokemon_caught(pokemon)
                        return
                    else:
                        new_chance -= 25
                if "paralyzed" in pokemon.status or "burned" in pokemon.status or "poisoned" in pokemon.status:
                    if new_chance < 12:
                        self.pokemon_caught(pokemon)
                        return
                    else:
                        new_chance -= 12
                if new_chance < 0:
                    new_chance = 0
                return new_chance

            # checks to see if the pokemon was caught via altered status:
            status_caught = status_catch(catch_chance)
            if status_caught is None:
                return
            else:
                if status_caught > pokemon.catch_rate:
                    print("The {0} broke free!".format(pokemon.name))
                    return
                else:
                    m = random.randint(0, 255)

                    def F():
                        if pokeball == "Great Ball":
                            f = math.trunc(pokemon.hp * 255 * 4) / (pokemon.current_hp * 8)
                        else:
                            f = math.trunc(pokemon.hp * 255 * 4) / (pokemon.current_hp * 12)
                        if f > 255:
                            f = 255
                        elif f < 1:
                            f = 1
                        return f

                    f_2 = F()
                    if f_2 >= m:
                        self.pokemon_caught(pokemon)
                        return
                    else:
                        print("The {0} broke free!".format(pokemon.name))
                        return

    def Evolve_check(self):
        for pokemon in self.pokemon:
            i = self.pokemon.index(pokemon)
            if pokemon.evolution is not None:
                try:
                    if pokemon.lvl > pokemon.evolve_lvl:
                        self.pokemon[i] = Evolve(pokemon)
                except ValueError:
                    continue

    def Pokemon_check(self):
        for pokemon in self.pokemon:
            if pokemon is not None:
                print(pokemon)


# defines the base class for all pokemon /unfinished, needs more work
class Pokemon:
    # xp_yield = (wild/owned * traded * base xp * feinted level)/7 * number in battle not feinted /not implemented
    def __init__(self, gender, base_stats, lvl, ivs=None, evs=None, owned=False):
        self.lvl = lvl
        self.base_stats = base_stats
        self.owned = owned
        # checks to see if EV's are imported from an evolution, or if its a newly caught pokemon
        if evs is None:
            self.EV = {"HP": 0, "ATTACK": 0, "DEFENSE": 0, "SPEED": 0, "SPECIAL": 0}
        else:
            self.EV = evs
        # checks to see if IVs are imported from a pre-evolution or if a newly caught pokemon, leaves out hp iv which
        # is calculated using the other ivs, then calculates HP iv and inserts it into self.iv
        if ivs is None:
            self.IV = {stat: random.randint(0, 15) for stat in self.base_stats.keys() if stat != "HP"}
            hp_binary = ""
            for item in self.IV.values():
                hp_binary += str(bin(item)[-1])
            self.IV["HP"] = int(hp_binary, 2)
        else:
            self.IV = ivs
        # function for determining a pokemon's max hp, rounding errors all over the place, might need to find out a way
        # clean that up
        self.hp = math.floor((math.floor(((self.base_stats["HP"] + self.IV["HP"]) * 2 + math.floor(
            math.ceil(math.sqrt(self.EV["HP"])) / 4)) * self.lvl) / 100) + self.lvl + 10)
        self.battle_stats = {stat: int(math.floor((((self.base_stats[stat] + self.IV[stat]) * 2 + math.floor(
            math.ceil(math.sqrt(self.EV[stat])) / 4)) * self.lvl) / 100) + 5) for stat in self.base_stats.keys() if
                             stat != "HP"}
        self.current_hp = self.hp
        self.xp = self.lvl ** 3
        self.xp_to_next = (self.lvl + 1) ** 3
        self.gender = gender
        self.moves = []
        self.ko = False
        self.status = []

    # initializes pokemon stats
    def __repr__(self):
        if self.gender == "Male":
            return "{0} is a lvl {1} {2}, he has {3} HP and knows the moves: {4}".format(self.name,
                                                                                         self.lvl,
                                                                                         self.pokemon_n,
                                                                                         self.current_hp,
                                                                                         self.moves)
        elif self.gender == "Female":
            return "{0} is a lvl {1} {2}, she has {3} HP and knows the moves: {4}".format(self.name,
                                                                                          self.lvl,
                                                                                          self.pokemon_n,
                                                                                          self.current_hp,
                                                                                          self.moves)

    # prints a description of the pokemon
    def Feinted(self):
        if self.current_hp <= 0:
            self.ko = True
        return print("{0} has feinted".format(self.name))

    # defines weather or not a pokemon is passed out / finished
    def Hp_update(self, value):
        # checks to see if incoming is damage
        if value <= 0:
            self.current_hp += value
            # placeholder update
            print("{0} took {1} damage".format(self.name, -value))
            if self.current_hp <= 0:
                self.current_hp = 0
                # calls the Feinted method to ko the pokemon
                self.Feinted()

        # checks to see if incoming is healing
        elif value > 0:
            self.current_hp += value
            if self.current_hp > self.hp:
                self.current_hp = self.hp
                print("{0} was healed to full.".format(self.name))
            else:
                print("{0} gained {1} HP!".format(self.name, value))

    # defines when a pokemon's hp changes
    def Revive(self, value):
        if self.current_hp == 0:
            self.current_hp += value
            self.ko = False
            print("{0} was revived and has {1} HP!".format(self.name, self.current_hp))

    # calculates EV gain of a pokemon when called (usually after a battle) / finished
    def Ev_gain(self, op_pokemon):
        for stat in op_pokemon.base_stats:
            self.EV[stat] += op_pokemon.base_stats[stat]

    # passes data to the returned evolved pokemon, instance should be a new instance with the same attributes /
    # unfinished
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

    # adds earned xp to pokemon's xp and calls the level_up function if they earned enough to be at the next level
    def Xp_gain(self, xp_earned):
        self.xp += xp_earned
        if self.xp == self.xp_to_next:
            self.Level_up()


# removed function for getting a pokemon and instead put all classes in a list, once they're defined will
# add function to create a random pokemon encounter
# defining each pokemon's base characteristics
# todo add pokemon moves, add all pokemon, add all pokemon catch rates
class Bulbasaur(Pokemon):
    def __init__(self, name="Bulbasaur", lvl=pokemon_level(), **evolve_args):
        self.elements = ["GRASS", "POISON"]
        self.pokemon_n = 1
        self.name = name
        self.catch_rate = 45
        ivs = ivs_starter(evolve_args.get('ivs'))
        evs = evs_starter(evolve_args.get('evs'))
        if evolve_args.get("gender") is None:
            gender = get_gender(.875)
        else:
            gender = evolve_args.get("gender")
        base_stats = {"HP": 45, "ATTACK": 49, "DEFENSE": 45, "SPEED": 45, "SPECIAL": 65}
        self.named = False
        if self.name != "Bulbasaur":
            self.named = True
        self.evolution = 2
        self.evolve_lvl = 16
        super().__init__(gender, base_stats, lvl, ivs, evs)


class Ivysaur(Pokemon):
    def __init__(self, name="Ivysaur", lvl=pokemon_level(), **evolve_args):
        self.elements = ["GRASS, POISON"]
        self.pokemon_n = 2
        self.name = name
        ivs = ivs_starter(evolve_args.get('ivs'))
        evs = evs_starter(evolve_args.get('evs'))
        if evolve_args.get("gender") is None:
            gender = get_gender(.875)
        else:
            gender = evolve_args.get("gender")
        base_stats = {"HP": 45, "ATTACK": 49, "DEFENSE": 45, "SPEED": 45, "SPECIAL": 65}
        self.named = False
        if name != "Ivysaur":
            self.named = True
        self.evolution = 3
        self.evolve_lvl = 32
        super().__init__(gender, base_stats, lvl, ivs, evs)


class Venusaur(Pokemon):
    def __init__(self, name="Venusaur", lvl=pokemon_level(), **evolve_args):
        self.elements = ["GRASS", "POISON"]
        self.pokemon_n = 3
        self.name = name
        ivs = ivs_starter(evolve_args.get('ivs'))
        evs = evs_starter(evolve_args.get('evs'))
        if evolve_args.get("gender") is None:
            gender = get_gender(.875)
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "Venusaur":
            self.named = True
        base_stats = {"HP": 80, "ATTACK": 82, "DEFENSE": 83, "SPEED": 80, "SPECIAL": 100}
        self.evolution = None

        super().__init__(gender, base_stats, lvl, ivs, evs)


class Charmander(Pokemon):
    def __init__(self, name="Charmander", lvl=pokemon_level(), **evolve_args):
        self.elements = ["FIRE"]
        self.pokemon_n = 4
        self.name = name
        self.catch_rate = 45
        ivs = ivs_starter(evolve_args.get('ivs'))
        evs = evs_starter(evolve_args.get('evs'))
        if evolve_args.get("gender") is None:
            gender = get_gender(.875)
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "Charmander":
            self.named = True
        base_stats = {"HP": 39, "ATTACK": 52, "DEFENSE": 43, "SPEED": 65, "SPECIAL": 50}
        self.evolution = 5
        self.evolve_lvl = 16
        super().__init__(gender, base_stats, lvl, ivs, evs)


class Charmeleon(Pokemon):
    def __init__(self, name="Charmeleon", lvl=pokemon_level(), **evolve_args):
        self.elements = ["FIRE"]
        self.pokemon_n = 5
        self.name = name
        self.catch_rate = 45
        ivs = ivs_starter(evolve_args.get('ivs'))
        evs = evs_starter(evolve_args.get('evs'))
        if evolve_args.get("gender") is None:
            gender = get_gender(.875)
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "Charmeleon":
            self.named = True
        base_stats = {"HP": 58, "ATTACK": 64, "DEFENSE": 58, "SPEED": 80, "SPECIAL": 65}
        self.evolution = 6
        self.evolve_lvl = 36
        super().__init__(gender, base_stats, lvl, ivs, evs)


class Charizard(Pokemon):
    def __init__(self, name="Charizard", lvl=pokemon_level(), **evolve_args):
        self.elements = ["FIRE"]
        self.pokemon_n = 6
        self.name = name
        self.catch_rate = 45
        ivs = ivs_starter(evolve_args.get('ivs'))
        evs = evs_starter(evolve_args.get('evs'))
        if evolve_args.get("gender") is None:
            gender = get_gender(.875)
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "Charizard":
            self.named = True
        base_stats = {"HP": 78, "ATTACK": 84, "DEFENSE": 78, "SPEED": 100, "SPECIAL": 86}
        self.evolution = None
        super().__init__(gender, base_stats, lvl, ivs, evs)


class Squirtle(Pokemon):
    def __init__(self, name="Squirtle", lvl=pokemon_level(), **evolve_args):
        self.elements = ["WATER"]
        self.pokemon_n = 7
        self.name = name
        self.catch_rate = 45
        ivs = ivs_starter(evolve_args.get('ivs'))
        evs = evs_starter(evolve_args.get('evs'))
        if evolve_args.get("gender") is None:
            gender = get_gender(.875)
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "Squirtle":
            self.named = True
        base_stats = {"HP": 44, "ATTACK": 48, "DEFENSE": 65, "SPEED": 43, "SPECIAL": 50}
        self.evolution = 8
        self.evolve_lvl = 16
        super().__init__(gender, base_stats, lvl, ivs, evs)


class Wartortle(Pokemon):
    def __init__(self, name="Wartortle", lvl=pokemon_level(), **evolve_args):
        self.elements = ["WATER"]
        self.pokemon_n = 8
        self.name = name
        self.catch_rate = 45
        ivs = ivs_starter(evolve_args.get('ivs'))
        evs = evs_starter(evolve_args.get('evs'))
        if evolve_args.get("gender") is None:
            gender = get_gender(.875)
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "Wartortle":
            self.named = True
        base_stats = {"HP": 59, "ATTACK": 63, "DEFENSE": 80, "SPEED": 58, "SPECIAL": 65}
        self.evolution = 9
        self.evolve_lvl = 36
        super().__init__(gender, base_stats, lvl, ivs, evs)


class Blastoise(Pokemon):
    def __init__(self, name="Blastoise", lvl=pokemon_level(), **evolve_args):
        self.elements = ["WATER"]
        self.pokemon_n = 9
        self.name = name
        self.catch_rate = 45
        ivs = ivs_starter(evolve_args.get('ivs'))
        evs = evs_starter(evolve_args.get('evs'))
        if evolve_args.get("gender") is None:
            gender = get_gender(.875)
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "Blastoise":
            self.named = True
        base_stats = {"HP": 79, "ATTACK": 83, "DEFENSE": 100, "SPEED": 78, "SPECIAL": 85}
        self.evolutions = None

        super().__init__(gender, base_stats, lvl, ivs, evs)

    # empty pokemon creation class


class Caterpie(Pokemon):
    def __init__(self, name="Caterpie", lvl=pokemon_level(), **evolve_args):
        self.elements = ["BUG"]
        self.pokemon_n = 10
        self.name = name
        self.catch_rate = 255
        ivs = ivs_starter(evolve_args.get('ivs'))
        evs = evs_starter(evolve_args.get('evs'))
        if evolve_args.get("gender") is None:
            gender = get_gender()
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "Caterpie":
            self.named = True
        base_stats = {"HP": 45, "ATTACK": 30, "DEFENSE": 35, "SPEED": 45, "SPECIAL": 20}
        self.evolution = 11
        self.evolve_lvl = 7
        super().__init__(gender, base_stats, lvl, ivs, evs)


class Metapod(Pokemon):
    def __init__(self, name="Metapod", lvl=pokemon_level(), **evolve_args):
        self.elements = ["BUG"]
        self.pokemon_n = 11
        self.name = name
        self.catch_rate = 120
        ivs = ivs_starter(evolve_args.get('ivs'))
        evs = evs_starter(evolve_args.get('evs'))
        if evolve_args.get("gender") is None:
            gender = get_gender()
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "Metapod":
            self.named = True
        base_stats = {"HP": 50, "ATTACK": 20, "DEFENSE": 55, "SPEED": 30, "SPECIAL": 25}
        self.evolution = 12
        self.evolve_lvl = 10
        super().__init__(gender, base_stats, lvl, ivs, evs)


class Butterfree(Pokemon):
    def __init__(self, name="Butterfree", lvl=pokemon_level(), **evolve_args):
        self.elements = ["BUG", "FLYING"]
        self.pokemon_n = 12
        self.name = name
        self.catch_rate = 45
        ivs = ivs_starter(evolve_args.get('ivs'))
        evs = evs_starter(evolve_args.get('evs'))
        if evolve_args.get("gender") is None:
            gender = get_gender()
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "Butterfree":
            self.named = True
        base_stats = {"HP": 60, "ATTACK": 45, "DEFENSE": 50, "SPEED": 30, "SPECIAL": 36}
        self.evolution = None
        super().__init__(gender, base_stats, lvl, ivs, evs)


class Weedle(Pokemon):
    def __init__(self, name="Weedle", lvl=pokemon_level(), **evolve_args):
        self.elements = ["BUG", "POISON"]
        self.pokemon_n = 13
        self.name = name
        self.catch_rate = 255
        ivs = ivs_starter(evolve_args.get('ivs'))
        evs = evs_starter(evolve_args.get('evs'))
        if evolve_args.get("gender") is None:
            gender = get_gender()
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "Weedle":
            self.named = True
        base_stats = {"HP": 40, "ATTACK": 35, "DEFENSE": 30, "SPEED": 50, "SPECIAL": 20}
        self.evolution = 14
        self.evolve_level = 7
        super().__init__(gender, base_stats, lvl, ivs, evs)


class Kakuna(Pokemon):
    def __init__(self, name="Kakuna", lvl=pokemon_level(), **evolve_args):
        self.elements = ["BUG", "POISON"]
        self.pokemon_n = 14
        self.name = name
        self.catch_rate = 120
        ivs = ivs_starter(evolve_args.get('ivs'))
        evs = evs_starter(evolve_args.get('evs'))
        if evolve_args.get("gender") is None:
            gender = get_gender()
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "Kakuna":
            self.named = True
        base_stats = {"HP": 45, "ATTACK": 25, "DEFENSE": 50, "SPEED": 35, "SPECIAL": 25}
        self.evolution = 15
        self.evolve_level = 10
        super().__init__(gender, base_stats, lvl, ivs, evs)


class Beedrill(Pokemon):
    def __init__(self, name="Beedrill", lvl=pokemon_level(), **evolve_args):
        self.elements = ["BUG", "POISON"]
        self.pokemon_n = 15
        self.name = name
        self.catch_rate = 45
        ivs = ivs_starter(evolve_args.get('ivs'))
        evs = evs_starter(evolve_args.get('evs'))
        if evolve_args.get("gender") is None:
            gender = get_gender()
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "Beedrill":
            self.named = True
        base_stats = {"HP": 65, "ATTACK": 80, "DEFENSE": 40, "SPEED": 75, "SPECIAL": 45}
        self.evolution = None
        self.evolve_level = None
        super().__init__(gender, base_stats, lvl, ivs, evs)


class Pidgey(Pokemon):
    def __init__(self, name="Pidgey", lvl=pokemon_level(), **evolve_args):
        self.elements = ["NORMAL", "FLYING"]
        self.pokemon_n = 16
        self.name = name
        self.catch_rate = 255
        ivs = ivs_starter(evolve_args.get('ivs'))
        evs = evs_starter(evolve_args.get('evs'))
        if evolve_args.get("gender") is None:
            gender = get_gender()
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "Pidgey":
            self.named = True
        base_stats = {"HP": 40, "ATTACK": 45, "DEFENSE": 40, "SPEED": 56, "SPECIAL": 35}
        self.evolution = 17
        self.evolve_level = 18
        super().__init__(gender, base_stats, lvl, ivs, evs)


class Pidgeotto(Pokemon):
    def __init__(self, name="Pidgeotto", lvl=pokemon_level(), **evolve_args):
        self.elements = []
        self.pokemon_n = 17
        self.name = name
        self.catch_rate = 120
        ivs = ivs_starter(evolve_args.get('ivs'))
        evs = evs_starter(evolve_args.get('evs'))
        if evolve_args.get("gender") is None:
            gender = get_gender()
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "Pidgeotto":
            self.named = True
        base_stats = {"HP": 63, "ATTACK": 60, "DEFENSE": 55, "SPEED": 71, "SPECIAL": 50}
        self.evolution = 18
        self.evolve_level = 36
        super().__init__(gender, base_stats, lvl, ivs, evs)


class Pidgeot(Pokemon):
    def __init__(self, name="Pidgeot", lvl=pokemon_level(), **evolve_args):
        self.elements = ["NORMAL", "FLYING"]
        self.pokemon_n = 18
        self.name = name
        self.catch_rate = 45
        ivs = ivs_starter(evolve_args.get('ivs'))
        evs = evs_starter(evolve_args.get('evs'))
        if evolve_args.get("gender") is None:
            gender = get_gender()
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "Pidgeot":
            self.named = True
        base_stats = {"HP": 83, "ATTACK": 80, "DEFENSE": 75, "SPEED": 91, "SPECIAL": 70}
        self.evolution = None
        self.evolve_level = None
        super().__init__(gender, base_stats, lvl, ivs, evs)


"""class (Pokemon):
    def __init__(self, name="", lvl=pokemon_level(), **evolve_args):
        self.elements = []
        self.pokemon_n = 
        self.name = name
        self.catch_rate = 
        ivs = ivs_starter(evolve_args.get('ivs'))
        evs = evs_starter(evolve_args.get('evs'))
        if evolve_args.get("gender") is None:
            gender = get_gender()
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "":
            self.named = True
        base_stats = {"HP": , "ATTACK": , "DEFENSE": , "SPEED": , "SPECIAL": }
        self.evolution = 
        self.evolve_level = 
        super().__init__(gender, base_stats, lvl, ivs, evs)"""
#  List of pokemon, used to return the class for the currently generated pokemon
pokemon_list = {
    0: None,
    1: Bulbasaur, 2: Ivysaur, 3: Venusaur,
    4: Charmander, 5: Charmeleon, 6: Charizard,
    7: Squirtle, 8: Wartortle, 9: Blastoise,
    10: Caterpie, 11: Metapod, 12: Butterfree,
    13: Weedle, 14: Kakuna, 15: Beedrill,
    16: Pidgey, 17: Pidgeotto, 18: Pidgeot,
    # 19: Rattata, 20: Raticate,
    # 21: Spearow, 22: Fearow,
    # 23: Ekans, 24: Arbok,
    # 25: Pikachu, 26: Raichu,
    # 27: Sandshrew, 28: Sandslash,
    # 29: Nidoran♀, 30: Nidorina, 31: Nidoqueen,
    # 32: Nidoran♂, 33: Nidorino, 34: Nidoking,
    # 35: Clefairy, 36: Clefable,
    # 37: Vulpix, 38: Ninetales,
    # 39: Jigglypuff, 40: Wigglytuff,
    # 41: Zubat, 42: Golbat,
    # 43: Oddish, 44: Gloom, 45: Vileplume,
    # 46: Paras, 47: Parasect,
    # 48: Venonat, 49: Venomoth,
    # 50: Diglett, 51: Dugtrio,
    # 52: Meowth, 53: Persian,
    # 54: Psyduck, 55: Golduck,
    # 56: Mankey, 57: Primeape,
    # 58: Growlithe, 59: Arcanine,
    # 60: Poliwag, 61: Poliwhirl, 62: Poliwrath,
    # 63: Abra, 64: Kedabra, 65: Alakazam,
    # 66: Machop, 67: Machoke, 68: Machamp,
    # 69: Bellsprout, 70: Weepinbell, 71: Victreebel,
    # 72: Tentacool, 73: Tentacruel,
    # 74: Geodude, 75: Graveler, 76: Golem,
    # 77: Ponyta, 78: Rapidash,
    # 79: Slowpoke, 80: Slowbro,
    # 81: Magnemite, 82: Magneton,
    # 83: Farfetchd,
    # 84: Doduo, 85: Dodrio,
    # 86: Seel, 87: Dewgong,
    # 88: Grimer, 89: Muk,
    # 90: Shellder, 91: Cloyster,
    # 92: Gastly, 93: Haunter, 94: Gengar,
    # 95: Onyx,
    # 96: Drowzee, 97: Hypno,
    # 98: Crabby, 99: Kingler,
    # 100: Voltorb, 101: Electrode,
    # 102: Exeggcute, 103: Exeggutor,
    # 104: Cubone, 105: Marowak,
    # 106: Hitmonlee, 107: Hitmonchan,
    # 108: Lickitung,
    # 109: Koffing, 110: Weezing,
    # 111: Ryhorn,
    # 112: Rhydon,
    # 113: Chansey,
    # 114: Tangela,
    # 115: Kangaskhan,
    # 116: Horsea, 117: Seadra,
    # 118: Goldeen, 119: Seaking,
    # 120: Staryu, 121: Starmie,
    # 122: Mr_Mime,
    # 123: Scyther,
    # 124: Jynx,
    # 125: Electabuzz,
    # 126: Magmar,
    # 127: Pinsir,
    # 128: Tauros,
    # 129: Magikarp, 130: Gyarados,
    # 131: Lapras,
    # 132: Ditto,
    # 133: Eevee, 134: Vaporeon, 135: Jolteon, 136: Flareon,
    # 137: Porygon,
    # 138: Omanyte, 139: Omastar,
    # 140: Kabuto, 141: Kabutops,
    # 142: Aerodactyl,
    # 143: Snorlax,
    # 144: Articuno,
    # 145: Zapdos,
    # 146: Moltres,
    # 147: Dratini, 148: Dragonair, 149: Dragonite,
    # 150: Mewtwo,
    # 151: Mew
}

""" test cases
bulbasaur = Bulbasaur(lvl=2)
charmander = Charmander(lvl=3)
squirtle = Squirtle(lvl=5)
caterpie = Caterpie(lvl=2)
red = Player("Zack", "boy")
red.items = {"Pokeball": {"Masterball": 10, "Pokeball": 10, "Greatball": 10, "Ultraball": 10}}
red.Catch_pokemon("Greatball", bulbasaur)
red.Catch_pokemon("Pokeball", charmander)
red.Catch_pokemon("Greatball", squirtle)
red.Catch_pokemon("Pokeball", caterpie)
print(red.pokemon)
print(red.items)
"""