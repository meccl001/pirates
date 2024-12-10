import random
from game import combat, config, display, event, location
from game.events import lucky, seagull
from game.locations.island import ManEatingMonkeys
import string
import game.items as item

'''-------------------------------------------------------------------------------------------------------------'''

class MakIsland (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "mak's island"
        self.symbol = 'P'
        self.visitable = True
        self.locations = {}
        self.locations["forbidden area"] = ForbiddenArea(self)
        self.locations["northern shore"] = NorthernShore(self)
        self.locations["rocky shore"] = RockyShore(self)
        self.locations["scary forest"] = ScaryForest(self)
        self.locations["beach"] = Beach_with_ship(self) #one good place to anchor
        
        self.starting_location = self.locations["beach"]

    def enter (self, ship):
        display.announce ("arrived at mak's island, the sand is pink!", pause=False)
'''-------------------------------------------------------------------------------------------------------------'''

class PinkPirate(combat.Monster):
    def __init__(self, name):
        attacks = {}
        attacks['glitter bombed'] = ['glitter bombed', random.randrange(45,70), (5,15)]
        attacks['pretty punched'] = ['pretty punched', random.randrange(25,45), (5,15)]
        attacks['magic wand'] = ['magic wand', random.randrange(15,35), (5, 15)]
        #["bites",random.randrange(35,51), (5,15)]
        super().__init__(name, random.randrange(5,26), attacks, 75 + random.randrange(-10,11))
        #7 to 19 hp, bite attack, 65 to 85 speed (100 is "normal")
        
        self.type_name = "Pink Pirate"
'''-------------------------------------------------------------------------------------------------------------'''
       
class EncounterPinkPirates (event.Event): #not done!!! still have to complete and figure out how to get combat going.
    purplePirate = False
    '''
    A combat encounter with a crew of pink pirates.
    When the event is drawn, creates a combat encounter with 2 to 6 pink pirates, kicks control over to the combat code
    to resolve the fight, then adds itself and a simple success message to the result
    '''
    
    def __init__ (self):
        self.name = "pink pirate attack"

    def process (self, world):
        '''Process the event. Populates a combat with pink pirates. The first pink may be modified into a "Pirate captain" by buffing its speed and health.'''
        result = {}
        result["message"] = "the pink pirates are defeated!"
        monsters = []
        min = 2
        uplim = 6
        if not EncounterPinkPirates.purplePirate:
            EncounterPinkPirates.purplePirate = True
            min = 1
            uplim = 5
            monsters.append(PinkPirate("Purple People Eating Pirate"))
            self.type_name = "Purple People Eating Pirate"
            monsters[0].health = 3*monsters[0].health
        elif random.randrange(2) == 0:
            min = 1
            uplim = 5
            monsters.append(PinkPirate("Pirate Queen"))
            self.type_name = "Pirate Queen"
            monsters[0].speed = 1.2*monsters[0].speed
            monsters[0].health = 2*monsters[0].health
        n_appearing = random.randrange(min, uplim)
        n = 1
        while n <= n_appearing:
            monsters.append(PinkPirate("Pink Pirate Crew "+str(n)))
            n += 1
        display.announce ("You are attacked by a crew of pink pirates!")
        combat.Combat(monsters).combat()
        result["newevents"] = [ self ]
        return result
'''-------------------------------------------------------------------------------------------------------------'''
   
class Beach_with_ship (location.SubLocation): #sub location 1
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        #self.verbs['onwards'] = self #new verb that is the only verb that will move player on to next "room"
        self.event_chance = 20 #60
        self.events.append(EncounterPinkPirates())

    def enter (self):
        display.announce ("arrive at the beach. Your ship is at anchor in a small bay to the south.")
        display.announce ("watch out, there may be pink pirates here")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"): 
            display.announce ("You return to your ship.")
            self.main_location.end_visit()
        elif (verb == "north"):
            display.announce ("you travel northern and see what appears to be a dirty beach ahead")
            config.the_player.next_loc = self.main_location.locations["northern shore"]
        elif (verb == "east"):
            display.announce ("You travel eastward and see what appears to be a forest ahead")
            config.the_player.next_loc = self.main_location.locations["scary forest"]
        elif (verb == "west"):
            display.announce ('You travel westwards, you see a bunch of "no tresspassing" signs')
            display.announce ("You cannot enter, perhaps there's a different spot that you can?")
        
'''-------------------------------------------------------------------------------------------------------------'''

class ScaryForest (location.SubLocation): #sub location 2
    def __init__ (self, m): #fix the process verbs to do what I want
        super().__init__(m)
        self.name = "Scary Forest"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        #self.verbs['onwards'] = self #new verb that is the only verb that will move player on to next "room"
        self.event_chance = 50
        self.events.append (seagull.Seagull())
    def enter (self):
        display.announce ("shiver me timbers! you arrive at the scary forest")
        display.announce ("you're scared to proceed")
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"): 
            display.announce ("you walked all around the area, pretty scary")
        elif (verb == "north"):
            display.announce ("You found a secret escape! A dirty beach is ahead")
            config.the_player.next_loc = self.main_location.locations["northern shore"]
        elif (verb == "west"):
            display.announce ("you retreat back to the beach (scaredy cat)")
            config.the_player.next_loc = self.main_location.locations["beach"]
        elif (verb == "east"):
            display.announce ("you made it through the forest, ahead is a treacherous beach")
            config.the_player.next_loc = self.main_location.locations["rocky shore"]
'''-------------------------------------------------------------------------------------------------------------'''

class RockyShore (location.SubLocation):#sub location 3
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Rocky Shore"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        #self.verbs['onwards'] = self #new verb that is the only verb that will move player on to next "room"
        #self.event_chance = 50
        #self.event_append = #number guessing game where if won, treasure is granted
    def enter (self):
        display.announce ("arrive at a rocky shore, watch your step!.")
        display.announce ("A large assumibly scary figure approches you!!!") #maybe do this?  #turns out to be not scary
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south" or verb == "north"):
            display.announce ("you walked all around the area, pretty rocky")
        elif (verb == "east"):
            display.announce ("You walk to the edge of the shore, it is quite tranquil")
        elif (verb == "west"):
            display.announce ("You found a way around the scary forest!")
            config.the_player.next_loc = self.main_location.locations["northern shore"]
'''-------------------------------------------------------------------------------------------------------------'''
            
class PrettyPinkBazooka(item.Item):
    def __init__(self):
        super().__init__("pink bazooka", 175) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (20,60)
        self.skill = "blaster"
        self.verb = "blows up"
        self.verb2 = "demolishes"
class PrettyPinkPearls(item.Item):
    def __init__(self):
        super().__init__('pretty pink pearls', 50)
        self.damage = (0,0)
        lucky.LuckyDay()
        self.skill = "confidence"
        self.verb = 'pretty'
'''-------------------------------------------------------------------------------------------------------------'''

class NorthernShore (location.SubLocation): #sublocation 4
    def __init__ (self, m):
        super().__init__(m) #no event on this "room", only treasure found
        self.name = "Northern Shore" #the treasure found code can be found in island.py where they get to eat the monkeys 
        self.verbs['north'] = self #and when there is things found in trees
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['investigate'] = self
        self.verbs['stay'] = self
        self.verbs['take'] = self
       # self.verbs['onwards'] = self #new verb that is the only verb that will move player on to next "room"
       #do a random thing, no ,atter what the variable should exist (=none)
        self.found_by_shore = PrettyPinkBazooka()
        self.found_in_litter = PrettyPinkPearls()

    def enter (self): 
        description = "curiosity fills you as you arrive at a shore scattered with litter."

        #Add a couple items as a demo. This is kinda awkward but students might want to complicated things.
        if self.found_by_shore != None:
            description = description + f" You see a {self.found_by_shore.name} in a pile of rubbish."
        if self.found_in_litter != None:
            description = description + f" You see {self.found_in_litter.name} in an abandoned sand castle."
        display.announce (description) 
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"): #fix the process verbs to do what I want
            display.announce ("you travel south and see a clean beach ahead")
            config.the_player.next_loc = self.main_location.locations["beach"]
        elif (verb == "north"):
            display.announce ("you walk to the edge of the beach and clean up some litter on the way")
        elif (verb == "east"):
            display.announce ("you take your path back to the rocky shore.")
            config.the_player.next_loc = self.main_location.locations["rocky shore"]
        elif (verb == "west"):
            display.announce ("There is a forbidden area ahead, there appears to be a section that is not blocked")
            display.announce ("do you wish to investigate? ")
            
        elif (verb == "investigate"):
            display.announce ("You chose your fate")
            config.the_player.go = True
            config.the_player.next_loc = self.main_location.locations["forbidden area"]
        elif (verb == "stay"):
            display.announce("You chose to stay, wise choice")
            config.the_player.go = True

        if verb == "take":
            if self.found_by_shore == None and self.found_in_litter == None:
                display.announce ("You don't see anything to take.")
            elif len(cmd_list) > 1:
                at_least_one = False #Track if you pick up an item, print message if not.
                item = self.found_by_shore
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    display.announce(f"You take the {item.name} from the ground.")
                    config.the_player.add_to_inventory([item])
                    self.found_by_shore = None
                    config.the_player.go = True
                    at_least_one = True
                item = self.found_in_litter
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    display.announce(f"You pick up the {item.name} out of the pile of litter... ...it is shiny and pretty and pink.")
                    config.the_player.add_to_inventory([item])
                    self.found_in_litter = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    display.announce ("You don't see one of those around.")
'''-------------------------------------------------------------------------------------------------------------'''
class ForbiddenArea(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m) #puzzle event not combat event
        self.name = "forbidden area" #letter guessing game 
        self.verbs['north'] = self #if you win you can leave
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 100
        self.events.append(LetterGuessingGame())
        
    def enter (self):
        display.announce ("the sky turns dark as it fills with clouds")
        display.announce ("the more you look around the more scared you get")   
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"): 
            display.announce ("you wandered south, who knows what will happen")
            # self.main_location.end_visit()
        elif (verb == "north"):
            display.announce("you wander back north, but can't seem to find the exit")
        elif (verb == "east"):
            display.announce ("You look across the east side of the area, you think you found the exit")
            config.the_player.next_loc = self.main_location.locations['beach']
        elif (verb == "west"):
            display.announce ("You wander to the east edge of the forest, it is shockingly peaceful")
'''-------------------------------------------------------------------------------------------------------------'''

class LetterGuessingGame (event.Event):
    
    #display.announce("a scary monster approaches, it looks menacing")
    def __init__ (self):
        self.name = "Letter Guessing Game"

    def inflictDamage(self):
        c = random.choice(config.the_player.get_pirates())
        if (c.isLucky() == True):
                    self.result["message"] = "luckly, the attacker missed"
        else:
            self.result["message"] = f"{c.get_name()} is attacked by the Leter Monster."
            if (c.inflict_damage (5, "Killed by the Letter Monster")): #what instead of self.seagulls
                self.result["message"] = f".. {c.get_name()} is slain by the Letter Monster!"
                self.cleanup_pirates()

    def process (self, world):
        letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        randLetterIndex=(random.choice(range(len(letters))))
        display.announce('The scary monster wants you to try and guess what letter it is thinking of')
        display.announce("You can try and fight, but it won't do much")
        guess = display.get_text_input("Guess now: ")
        n = 0

        if guess in letters: 
            guessIndex = letters.index(guess)
            while guessIndex!=randLetterIndex:
                min = 1
                uplim = 5
    
                if guessIndex < randLetterIndex: #if the guess is too 'soon' in the alphabet
                    display.announce("Incorrect! Your guess is before mine in the alphabet") #figure out how to take damage, probably have tp create a combat monster
                    display.announce("Pick again loser, or keep losing health. Up to you!")
                    self.inflictDamage()
                    guess = display.get_text_input("Guess Again: ") 
                    n+=1
                    
                elif guessIndex > randLetterIndex: #guess is too 'late' in the alphabet, take damage
                    display.announce("Incorrect! Your guess is after mine in the alphabet moron!")
                    self.inflictDamage()
                    guess = display.get_text_input("Guess Again:")
                    n+=1
                    
                else:
                    display.announce("Rats!!! You Guessed correctly!")
                    display.announce("Go east before I change my mind... NOW!!!")
                    n+=1
                    display.announce()
        result = {}
        msg = (f'It took you {n} amount of tries!')
        result["message"] = msg
        result["newevents"] = [ self ]
        return result

