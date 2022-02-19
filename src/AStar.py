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


def AStar(initial_state, heuristic_function, alpha):
    explored = set()
    frontier = []
    frontier.append(initial_state)
    while True:
        state = frontier.pop(0)
        explored.add(state)

        if state.goal_test():
            return state

        new_states = state.new_states()

        for new_state in new_states:
            if new_state not in explored and new_state not in frontier:
                heuristic = heuristic_function(new_state) * alpha
                cost_so_far = len(new_state.path)
                new_state.evaluation = heuristic + cost_so_far
                bisect.insort(frontier, new_state)



if __name__ == "__main__":
    initial_state = utils.read_from_file(os.sys.argv[1])
    tic = time.time()
    print("Path:", AStar(initial_state, heu2, 1).path)
    toc = time.time()
    print("Time: %f ms" % ((toc - tic) * 1000))
