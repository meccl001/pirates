import random
from game import combat, config, display, event, location
from game.events import seagull
from game.locations.island import ManEatingMonkeys


class MakIsland (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "mak's island"
        self.symbol = 'I'
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

class PinkPirate(combat.Monster):
    def __init__(self, name):
        attacks = {}
        attacks['glitter bomb'] = ['glitter bomb', random.randrange(45,70), (5,15)]
        attacks['pretty punch'] = ['pretty punch', random.randrange(25,45), (5,15)]
        attacks['magic wand'] = ['magic wand', random.randrange(15,35), (5, 15)]
        #["bites",random.randrange(35,51), (5,15)]
        super().__init__(name, random.randrange(5,26), attacks, 75 + random.randrange(-10,11))
        #7 to 19 hp, bite attack, 65 to 85 speed (100 is "normal")
        
        self.type_name = "Pink Pirate"
        
class EncounterPinkPirates (event.Event): #not done!!! still have to complete and figure out how to get combat going.
    '''
    A combat encounter with a crew of pink pirates.
    When the event is drawn, creates a combat encounter with 2 to 6 pink pirates, kicks control over to the combat code
    to resolve the fight, then adds itself and a simple success message to the result
    '''
    purplePirate = False
    def __init__ (self):
        self.name = "pink pirate attack"

    def process (self, world):
        '''Process the event. Populates a combat with pink pirates. The first pink may be modified into a "Pirate captain" by buffing its speed and health.'''
        result = {}
        result["message"] = "the pink pirates are defeated!"
        monsters = []
        min = 2
        uplim = 6
        if not PinkPirate.purplePirate:
            PinkPirate.purplePirate = True
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
    
class Beach_with_ship (location.SubLocation): #sub location 1
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        #self.verbs['onwards'] = self #new verb that is the only verb that will move player on to next "room"
        self.event_chance = 50
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
        display.announce ("A large assumibly scary figure approches you!!!")   #turns out to be not scary
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south" or verb == "north"):
            display.announce ("you walked all around the area, pretty rocky")
        elif (verb == "east"):
            display.announce ("You walk to the edge of the shore, it is quite tranquil")
        elif (verb == "west"):
            display.announce ("You retreat back into the scary forest, be safe!")
            config.the_player.next_loc = self.main_location.locations["scary forest"]
            
          
class NorthernShore (location.SubLocation): #sublocation 4
    def __init__ (self, m):
        super().__init__(m) #no event on this "room", only treasure found
        self.name = "Northern Shore" #the treasure found code can be found in island.py where they get to eat the monkeys 
        self.verbs['north'] = self #and when there is things found in trees
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
       # self.verbs['onwards'] = self #new verb that is the only verb that will move player on to next "room"
        
    def enter (self):
        display.announce ("arrive at a shore scattered with litter")
        display.announce ("curiosity fills you as you wonder what trinkets you could find")   
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"): #fix the process verbs to do what I want
            display.announce ("you travel south and see a clean beach ahead")
            config.the_player.next_loc = self.main_location.locations["beach"]
        elif (verb == "north"):
            display.announce ("you walk to the edge of the beach and clean up some litter on the way")
        elif (verb == "east"):
            display.announce ("You walk all the way around the island on the beach. It's not very interesting.")
        elif (verb == "west"):
            display.announce ("You walk all the way around the island on the beach. It's not very interesting.")

class ForbiddenArea(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m) #puzzle event not combat event
        self.name = "forbidden area" #letter guessing game 
        self.verbs['north'] = self #if you win you can leave
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        #self.verbs['onwards'] = self #new verb that is the only verb that will move player on to next "room"
        #self.event_chance = 50
        #self.events.append()#letter guessing game
        
    def enter (self):
        display.announce ("the sky turns dark as it fills with clouds")
        display.announce ("the area grows increasingly eerie the more you look around")   
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"): 
            display.announce ("")
            self.main_location.end_visit()
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["trees"]
        elif (verb == "east"):
            display.announce ("You walk all the way around the island on the beach. It's not very interesting.")
        elif (verb == "west"):
            display.announce ("You walk all the way around the island on the beach. It's not very interesting.")
