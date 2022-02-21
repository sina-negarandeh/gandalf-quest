import utils
import time
import os
import bisect

# tedad yar haye baghi moonde
def heu1(state):
    return len(state.fellowships)


# az beyn fasele haye gandalf ta yar ha, max begirim
def heu2(state):
    max_distance = 0
    for fellowship in state.fellowships:
        distance = abs(fellowship[0] - state.gandalf.position[0]) + abs(fellowship[1] - state.gandalf.position[1])
        if distance > max_distance:
            max_distance = distance

    return max_distance


def heu3(state):
    to_final = abs(utils.FINAL_POSITION[0] - state.gandalf.position[0]) + abs(utils.FINAL_POSITION[1] - state.gandalf.position[1])
    for idx, fellowship in enumerate(state.fellowships):
        dist = abs(fellowship[0] - state.fellowships_destination[idx][0]) + abs(fellowship[1] - state.fellowships_destination[idx][1])
        to_final += dist
    return to_final


def AStar(initial_state, heuristic_function, alpha):
    explored = set()
    frontier = []
    state = initial_state
    while True:
        if state.goal_test():
            return state
        
        if state not in explored:
            
            new_states = state.new_states()
            for new_state in new_states:
                heuristic = heuristic_function(new_state) * alpha
                cost_so_far = len(new_state.path)
                new_state.evaluation = heuristic + cost_so_far
                bisect.insort(frontier, new_state)
        explored.add(state)
        state = frontier.pop(0)


if __name__ == "__main__":
    initial_state = utils.read_from_file(os.sys.argv[1])
    tic = time.time()
    print("Path:", AStar(initial_state, heu1, 1).path)
    toc = time.time()
    print("Time: %f ms" % ((toc - tic) * 1000))
