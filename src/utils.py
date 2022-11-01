ORCS = []
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
DICT = {(-1,0):"U", (1,0):"D", (0, -1):"L", (0, 1):"R"}

class Orc:
    def __init__(self, position, _range):
        self.position = position
        self.range = _range

    
    def is_in_range(self, position):
        return abs(position[0] - self.position[0]) + abs(position[1] - self.position[1]) <= self.range


class Gandalf:
    def __init__(self, initial_position, fellowship, steps_in_danger):
        self.position = initial_position
        self.fellowship = fellowship
        self.steps_in_danger = steps_in_danger


    def can_move(self, direction):
        new_position = list(map(sum,zip(self.position, direction)))

        if new_position[0] >= N or new_position[1] >= M:
            return False

        if new_position[0] < 0 or new_position[1] < 0:
            return False
        
        for idx, orc in enumerate(ORCS):
            if orc.position == new_position:
                return False
            if orc.is_in_range(new_position) and self.steps_in_danger[idx] >= orc.range:
                return False
       
        return True


    def move(self, direction, fellowships, fellowships_destination):
        previous_position = self.position
        self.position = list(map(sum,zip(self.position, direction)))

        if self.fellowship != [-1, -1]:
            if self.position == self.fellowship:
                self.fellowship = [-1, -1]
                fellowships_destination.remove(self.position)
        
        if self.fellowship == [-1,-1] and self.position in fellowships:      
            self.fellowship = fellowships_destination[fellowships.index(self.position)].copy()
            fellowships.remove(self.position)


        for idx, orc in enumerate(ORCS):
            if orc.is_in_range(previous_position) and not orc.is_in_range(self.position):
                self.steps_in_danger[idx] = 0

        for idx, orc in enumerate(ORCS):
            if orc.is_in_range(self.position):
                self.steps_in_danger[idx] += 1
            



class State:
    def __init__(self, gandalf, fellowships, fellowships_destination):
        self.gandalf = gandalf
        self.fellowships = fellowships
        self.fellowships_destination = fellowships_destination
        self.path = ""
        self.evaluation = 0
        
    
    def __lt__(self, other):
        return self.evaluation < other.evaluation

    
    def goal_test(self):
        return self.gandalf.position == FINAL_POSITION and len(self.fellowships) == 0 and len(self.fellowships_destination) == 0

    def new_states(self):
        states = []
        for direction in DIRECTIONS:
            if self.gandalf.can_move(direction):
                new_gandalf = Gandalf(self.gandalf.position, self.gandalf.fellowship, self.gandalf.steps_in_danger.copy())
                new_state = State(new_gandalf, self.fellowships.copy(), self.fellowships_destination.copy()) 
                new_state.gandalf.move(direction, new_state.fellowships, new_state.fellowships_destination)
                new_state.path = self.path + DICT[direction]
                states.append(new_state)

        return states

    def __eq__(self, other):
        c1 = self.gandalf.position == other.gandalf.position
        c2 = self.fellowships == other.fellowships
        c3 = self.fellowships_destination == other.fellowships_destination
        c4 = self.gandalf.steps_in_danger == other.gandalf.steps_in_danger
        return c1 and c2 and c3 and c4

    def __hash__(self):
        return hash(str(self.gandalf.position) + str(self.fellowships) + str(self.fellowships_destination) + str(self.gandalf.steps_in_danger))
        


def read_from_file(filename):
    global M, N, FINAL_POSITION, NUMBER_OF_ORCS
    file = open(filename, "r")
    N, M = map(int, file.readline().split())
    initial_position = list(map(int, file.readline().split()))
    FINAL_POSITION = list(map(int, file.readline().split()))
    NUMBER_OF_ORCS, number_of_fellowships = map(int, file.readline().split())
    
    for _ in range(NUMBER_OF_ORCS):
        x, y, _range = map(int, file.readline().split())
        ORCS.append(Orc([x, y], _range))
    
    fellowships = []
    for _ in range(number_of_fellowships):
        fellowships.append(list(map(int, file.readline().split())))

    fellowships_destination = []
    for _ in range(number_of_fellowships):
        fellowships_destination.append(list(map(int, file.readline().split())))

    gandalf = Gandalf(initial_position, [-1,-1], [0] * NUMBER_OF_ORCS)
    initial_state = State(gandalf, fellowships, fellowships_destination)
    return initial_state
