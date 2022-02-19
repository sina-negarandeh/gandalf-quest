import utils
import time
import os


def DFS(state, max_depth, cost, explored):
    if max_depth <= 0:
        return None

    if state.goal_test():
        return state

    new_states = state.new_states()
    for new_state in new_states:
        if (new_state not in explored) or (new_state in explored and explored[new_state] > cost):
            explored[new_state] = cost
            result = DFS(new_state, max_depth - 1, cost + 1, explored)
            if result is not None:
                return result

    
def IDS(initial_state):
    depth = 0
    while True:
        explored = dict()
        explored[initial_state] = 0
        result = DFS(initial_state, depth, 0, explored)
        if result is not None:
            return result
        depth += 1



if __name__ == "__main__":
    initial_state = utils.read_from_file(os.sys.argv[1])
    tic = time.time()
    print("Path:", IDS(initial_state).path)
    toc = time.time()
    print("Time: %f ms" % ((toc - tic) * 1000))
