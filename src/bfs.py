import utils
import queue
import time
import os


def BFS(initial_state):
    explored = set()
    frontier = queue.Queue()
    frontier.put(initial_state)
    explored.add(initial_state)
    
    while not frontier.empty():
        state = frontier.get()
        if state.goal_test():
            return state

        new_states = state.new_states()

        for new_state in new_states:
            if new_state not in explored:
                frontier.put(new_state)
                explored.add(new_state)
    return None


if __name__ == "__main__":
    initial_state = utils.read_from_file(os.sys.argv[1])
    tic = time.time()
    print("Path:", BFS(initial_state).path)
    toc = time.time()
    print("Time: %f ms" % ((toc - tic) * 1000))
