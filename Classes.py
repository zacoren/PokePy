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


# function that appends status effects and changes pokemon behavior /unfinished
def status_effects():
    pass


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


# returns a function that modifies pokemon behavior based on move statuses / unfinished


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
class Player(Trainer):
    def __init__(self, name="Red", gender=None):
        self.gender = gender
        super().__init__(name, 0)
        self.boxes = [[], [], [], []]
        self.current_box = self.boxes[0]

    # defines a players ability to catch pokemon /functional but needs work for interactivity
    def Catch_pokemon(self, pokeball, pokemon):
        if pokeball is "Masterball":
            self.items[pokeball] -= 1
            if len(self.pokemon) < 6:
                self.pokemon.append(pokemon)
            else:
                self.current_box.append(pokemon)
                print("You caught {0}".format(pokemon.name))
                return
        else:
            def get_catch_chance():
                if pokeball is "Pokeball":
                    chance = random.randint(0, 255)
                elif pokeball is "Great Ball":
                    chance = random.randint(0, 200)
                    self.items[pokeball] -= 1
                else:
                    chance = random.randint(0, 150)
                    self.items[pokeball] -= 1
                return chance

            catch_chance = get_catch_chance()

            def status_catch(current_chance):
                new_chance = current_chance
                if "asleep" in pokemon.status or "frozen" in pokemon.status:
                    if new_chance < 25:
                        self.pokemon.append(pokemon)
                        print("You caught {0}".format(pokemon.name))
                        return
                    else:
                        new_chance -= 25
                if "paralyzed" in pokemon.status or "burned" in pokemon.status or "poisoned" in pokemon.status:
                    if new_chance < 12:
                        self.pokemon.append(pokemon)
                        print("You caught {0}".format(pokemon.name))
                        return
                    else:
                        new_chance -= 12
                return new_chance

            if status_catch(catch_chance) is not None:
                if status_catch(catch_chance) > pokemon.catch_rate:
                    print("The Pokemon broke free!")
                    return
            elif status_catch(catch_chance) is not None:
                m = random.randint(0, 255)

                def F():
                    if pokeball is "Great Ball":
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
                    self.pokemon.append(pokemon)
                    print("You caught {0}".format(pokemon.name))
                    return
            else:
                print("The Pokemon broke free!")
                return


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
        self.status = None

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


# basic function for randomizing gender , takes r, ratio of male to females. higher ratio means more females
# r should always be a number between 0 and 1, if no ratio is defined then it is always 50/50
def get_gender(r=.5):
    g = random.randint(0, 100)
    if g <= r * 100:
        return "Male"
    else:
        return "Female"


# removed function for getting a pokemon and instead put all classes in a list, once theyre defined will 
# add function to create a random pokemon encounter
# defining each pokemon's base characteristics
# todo add pokemon moves, add all pokemon, add all pokemon catch rates
class Bulbasaur(Pokemon):
    def __init__(self, name="Bulbasaur", lvl=pokemon_level(), **evolve_args):
        self.elements = ["GRASS", "POISON"]
        self.pokemon_n = 1
        self.name = name
        self.catch_rate = 45
        ivs = None
        if evolve_args.get("ivs") is not None:
            ivs = evolve_args.get("ivs")
        evs = None
        if evolve_args.get("evs") is not None:
            evs = evolve_args.get("evs")
        if evolve_args.get("gender") is None:
            gender = get_gender(.875)
        else:
            gender = evolve_args.get("gender")
        base_stats = {"HP": 45, "ATTACK": 49, "DEFENSE": 45, "SPEED": 45, "SPECIAL": 65}
        self.named = False
        if self.name != "Bulbasaur":
            self.named = True
        self.evolution = 2
        super().__init__(gender, base_stats, lvl, ivs, evs)
        self.evolve_lvl = 16


class Ivysaur(Pokemon):
    def __init__(self, name="Ivysaur", lvl=pokemon_level(), **evolve_args):
        self.elements = ["GRASS, POISON"]
        self.pokemon_n = 2
        self.name = name
        ivs = None
        if evolve_args.get("ivs") is not None:
            ivs = evolve_args.get("ivs")
        evs = None
        if evolve_args.get("evs") is not None:
            evs = evolve_args.get("evs")
        if evolve_args.get("gender") is None:
            gender = get_gender(.875)
        else:
            gender = evolve_args.get("gender")
        base_stats = {"HP": 45, "ATTACK": 49, "DEFENSE": 45, "SPEED": 45, "SPECIAL": 65}
        self.named = False
        if name != "Ivysaur":
            self.named = True
        self.evolution = 3
        super().__init__(gender, base_stats, lvl, ivs, evs)


class Venusaur(Pokemon):
    def __init__(self, name="Venusaur", lvl=pokemon_level(), **evolve_args):
        self.elements = ["GRASS", "POISON"]
        self.pokemon_n = 3
        self.name = name
        ivs = None
        if evolve_args.get("ivs") is not None:
            ivs = evolve_args.get("ivs")
        evs = None
        if evolve_args.get("evs") is not None:
            evs = evolve_args.get("evs")
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
        ivs = None
        if evolve_args.get("ivs") is not None:
            ivs = evolve_args.get("ivs")
        evs = None
        if evolve_args.get("evs") is not None:
            evs = evolve_args.get("evs")
        if evolve_args.get("gender") is None:
            gender = get_gender(.875)
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "Charmander":
            self.named = True
        base_stats = {"HP": 39, "ATTACK": 52, "DEFENSE": 43, "SPEED": 65, "SPECIAL": 50}
        self.evolution = 5

        super().__init__(gender, base_stats, lvl, ivs, evs)


class Charmeleon(Pokemon):
    def __init__(self, name="Charmeleon", lvl=pokemon_level(), **evolve_args):
        self.elements = ["FIRE"]
        self.pokemon_n = 5
        self.name = name
        ivs = None
        if evolve_args.get("ivs") is not None:
            ivs = evolve_args.get("ivs")
        evs = None
        if evolve_args.get("evs") is not None:
            evs = evolve_args.get("evs")
        if evolve_args.get("gender") is None:
            gender = get_gender(.875)
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "Charmeleon":
            self.named = True
        base_stats = {"HP": 58, "ATTACK": 64, "DEFENSE": 58, "SPEED": 80, "SPECIAL": 65}
        self.evolution = 6

        super().__init__(gender, base_stats, lvl, ivs, evs)


class Charizard(Pokemon):
    def __init__(self, name="Charizard", lvl=pokemon_level(), **evolve_args):
        self.elements = ["FIRE"]
        self.pokemon_n = 6
        self.name = name
        ivs = None
        if evolve_args.get("ivs") is not None:
            ivs = evolve_args.get("ivs")
        evs = None
        if evolve_args.get("evs") is not None:
            evs = evolve_args.get("evs")
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
        ivs = None
        if evolve_args.get("ivs") is not None:
            ivs = evolve_args.get("ivs")
        evs = None
        if evolve_args.get("evs") is not None:
            evs = evolve_args.get("evs")
        if evolve_args.get("gender") is None:
            gender = get_gender(.875)
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "Squirtle":
            self.named = True
        base_stats = {"HP": 44, "ATTACK": 48, "DEFENSE": 65, "SPEED": 43, "SPECIAL": 50}
        self.evolution = 8

        super().__init__(gender, base_stats, lvl, ivs, evs)


class Wartortle(Pokemon):
    def __init__(self, name="Wartortle", lvl=pokemon_level(), **evolve_args):
        self.elements = ["WATER"]
        self.pokemon_n = 8
        self.name = name
        ivs = None
        if evolve_args.get("ivs") is not None:
            ivs = evolve_args.get("ivs")
        evs = None
        if evolve_args.get("evs") is not None:
            evs = evolve_args.get("evs")
        if evolve_args.get("gender") is None:
            gender = get_gender(.875)
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "Wartortle":
            self.named = True
        base_stats = {"HP": 59, "ATTACK": 63, "DEFENSE": 80, "SPEED": 58, "SPECIAL": 65}
        self.evolution = 9

        super().__init__(gender, base_stats, lvl, ivs, evs)


class Blastoise(Pokemon):
    def __init__(self, name="Blastoise", lvl=pokemon_level(), **evolve_args):
        self.elements = ["WATER"]
        self.pokemon_n = 9
        self.name = name
        ivs = None
        if evolve_args.get("ivs") is not None:
            ivs = evolve_args.get("ivs")
        evs = None
        if evolve_args.get("evs") is not None:
            evs = evolve_args.get("evs")
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
        ivs = None
        if evolve_args.get("ivs") is not None:
            ivs = evolve_args.get("ivs")
        evs = None
        if evolve_args.get("evs") is not None:
            evs = evolve_args.get("evs")
        if evolve_args.get("gender") is None:
            gender = get_gender()
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "Caterpie":
            self.named = True
        base_stats = {"HP": 45, "ATTACK": 30, "DEFENSE": 35, "SPEED": 45, "SPECIAL": 20}
        self.evolution = 11

        super().__init__(gender, base_stats, lvl, ivs, evs)


class Metapod(Pokemon):
    def __init__(self, name="Metapod", lvl=pokemon_level(), **evolve_args):
        self.elements = ["BUG"]
        self.pokemon_n = 11
        self.name = name
        ivs = None
        if evolve_args.get("ivs") is not None:
            ivs = evolve_args.get("ivs")
        evs = None
        if evolve_args.get("evs") is not None:
            evs = evolve_args.get("evs")
        if evolve_args.get("gender") is None:
            gender = get_gender()
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "Metapod":
            self.named = True
        base_stats = {"HP": 50, "ATTACK": 20, "DEFENSE": 55, "SPEED": 30, "SPECIAL": 25}
        self.evolution = 12

        super().__init__(gender, base_stats, lvl, ivs, evs)


class Butterfree(Pokemon):
    def __init__(self, name="Butterfree", lvl=pokemon_level(), **evolve_args):
        self.elements = ["BUG", "FLYING"]
        self.pokemon_n = 12
        self.name = name
        ivs = None
        if evolve_args.get("ivs") is not None:
            ivs = evolve_args.get("ivs")
        evs = None
        if evolve_args.get("evs") is not None:
            evs = evolve_args.get("evs")
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


"""class (Pokemon):
    def __init__(self, name="", lvl=pokemon_level(), **evolve_args):
        self.elements = []
        self.pokemon_n = 
        self.catch_rate = 
        self.name = name
        ivs = None
        if evolve_args.get("ivs") is not None:
            ivs = evolve_args.get("ivs")
        evs = None
        if evolve_args.get("evs") is not None:
            evs = evolve_args.get("evs")
        if evolve_args.get("gender") is None:
            gender = get_gender()
        else:
            gender = evolve_args.get("gender")
        self.named = False
        if self.name != "":
            self.named = True
        base_stats = {"HP": , "ATTACK": , "DEFENSE": , "SPEED": , "SPECIAL": }
        self.evolution = 

        super().__init__(gender, base_stats, lvl, ivs, evs)"""
#  List of pokemon, used to return the class for the currently generated pokemon
pokemon_list = {
    0: None,
    1: Bulbasaur, 2: Ivysaur, 3: Venusaur,
    4: Charmander, 5: Charmeleon, 6: Charizard,
    7: Squirtle, 8: Wartortle, 9: Blastoise,
    10: Caterpie, 11: Metapod, 12: Butterfree,
    # 13: Weedle, 14: Kakuna, 15: Beedrill,
    # 16: Pidgey, 17: Pidgeotto, 18: Pidgeot,
    # 19: Rattata, 20: Raticate,
    # 21: Spearow, 22: Fearow,
    # 23: Ekans, 24: Arbok,
    # 25: Pikachu, 26: Raichu,
    # 27: Sandshrew, 28: Sandslash,
    # 29: Nidoran♀, 30: Nidorina, 31: Nidoqueen,
    # 32: Nidoran♂, 33: Nidorino, 34: Nidoking,
    # 35: Clefairy, 36: Clefable,
    # 37: vulpix, 38: ninetales,
    # 39: jigglypuff ,40: wigglytuff,
    # 41: zubat, 42: golbat,
    # 43: oddish, 44: gloom ,45: vileplume,
    # 46: paras, 47: parasect ,
    # 48: venonat, 49: venomoth,
    # 50: diglett, 51: dugtrio,
    # 52: meowth, 53: persian,
    # 54: psyduck, 55: golduck,
    # 56: mankey, 57: primeape,
    # 58: growlithe, 59: arcanine,
    # 60: poliwag, 61: poliwhirl, 62: poliwrath,
    # 63: abra, 64: kedabra, 65: alakazam,
    # 66: machop, 67: machoke, 68: machamp,
    # 69: bellsprout, 70: weepinbell, 71: victreebel,
    # 72: tentacool, 73: tentacruel,
    # 74: geodude, 75: graveler, 76: golem,
    # 77: ponyta, 78: rapidash ,
    # 79: slowpoke, 80: slowbro,
    # 81: magnemite, 82:magneton,
    # 83: farfetchd,
    # 84: doduo, 85: dodrio,
    # 86: seel, 87: dewgong,
    # 88: grimer, 89: muk,
    # 90: shellder, 91: cloyster,
    # 92: gastly, 93: haunter, 94: gengar,
    # 95: onyx,
    # 96: drowzee, 97: hypno,
    # 98: crabby, 99: kingler,
    # 100: voltorb, 101: electrode,
    # 102: exeggcute, 103: exeggutor,
    # 104: cubone, 105: marowak,
    # 106: hitmonlee, 107: hitmonchan,
    # 108: lickitung,
    # 109: koffing, 110: weezing,
    # 111: ryhorn,
    # 112: rhydon,
    # 113: chansey,
    # 114: tangela,
    # 115: kangaskhan,
    # 116: horsea, 117: seadra,
    # 118: goldeen, 119: seaking,
    # 120: staryu, 121: starmie,
    # 122: Mr_Mime,
    # 123: Scyther,
    # 124: jynx,
    # 125: electabuzz,
    # 126: magmar,
    # 127: pinsir,
    # 128: tauros,
    # 129: magikarp, 130: gyarados,
    # 131: lapras,
    # 132: ditto,
    # 133: eevee, 134: vaporeon, 135: jolteon, 136: flareon,
    # 137: porygon,
    # 138: omanyte, 139: omastar,
    # 140: kabuto, 141: kabutops,
    # 142: aerodactyl,
    # 143: snorlax,
    # 144: articuno,
    # 145: zapdos,
    # 146: moltres,
    # 147: dratini, 148: dragonair, 149: dragonite,
    # 150: mewtwo,
    # 151: mew
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


# test cases
bulbasaur = Bulbasaur(lvl=20)
print(bulbasaur)
print(bulbasaur.base_stats)
print(bulbasaur.IV)
bulbasaur.Ev_gain(bulbasaur)
bulbasaur.Ev_gain(bulbasaur)
bulbasaur.Ev_gain(bulbasaur)
bulbasaur.Ev_gain(bulbasaur)
bulbasaur.Ev_gain(bulbasaur)
print(bulbasaur.EV)
bulbasaur = Evolve(bulbasaur)
print(bulbasaur)
print(bulbasaur.base_stats)
print(bulbasaur.IV)
print(bulbasaur.EV)
