class Player:
    def __init__(self,name,hp):
        self.name = name
        self.hp = hp
        self.items = []
    

class GameState:
    '''This is just to keep track of the Game's state and the reason to make a seperate class for is it will be
    simpler for the AI to make new states for prediction'''
    def __init__(self):
        self.player = Player('Player',4)
        self.dealer = Player('AI',4)
        self.shells = [] # '1' : Live, 0: Blank
        self.shell_index = 0
        self.turn = 'Player' #Initally it is always players turn

    #It returns the deep copy of the current state
    #Changes in deepcopy doesnt afftect the real data which is useful for AI data simulations
    def copy(self):
        import copy
        return copy.deepcopy(self)
    

    