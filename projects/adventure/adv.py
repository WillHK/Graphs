from room import Room
from player import Player
from world import World
from util import Stack

import random
from collections import deque
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

def get_exits(room):
    valid_exits = []
    exits = room.get_exits()
    for exit in exits:
        full_room = room.get_room_in_direction(exit)
        valid_exits.append((full_room, exit))
    return valid_exits

def DFT(room, traversal_path):
    path = [room]
    stack = [path]
    visited = set()

    while stack:
        path = stack.pop()
        new_room = path[-1][0]
        # print(new_room)
        if new_room.id not in visited:
            visited.add(new_room.id)

            neighbors = get_exits(new_room)

            if all([neighbor_room.id in [path_room.id for path_room, _ in path] for neighbor_room, _ in neighbors]):
                # print("DFT no new rooms:", path)
                return path[1:]
            for neighbor in neighbors:
                if neighbor[0].id not in [trav_room.id for trav_room, _ in traversal_path]:
                    new_path = [*path, neighbor]
                    stack.append(new_path)
    return path

def BFT(room, traversal_path):
    path = [room]
    visited = set()
    queue = deque()
    queue.append(path)

    while queue:
        path = queue.popleft()
        new_room = path[-1][0]
        if new_room.id not in visited:
            visited.add(new_room.id)

            neighbors = get_exits(new_room)

            if any(neighbor_room.id not in [trav_room.id for trav_room, _ in traversal_path] for neighbor_room, _ in neighbors):
                # print("BFT found unvisited room:", path)
                return path[1:]
            for neighbor in neighbors:
                new_path = [*path, neighbor]
                queue.append(new_path)

def traversal(start):
    traversal_path = [(start, '')]
    while True:
        test_path = traversal_path.copy()

        depth_first_path = DFT(test_path[-1], test_path)

        test_path = [*test_path, *depth_first_path]
        traversal_path = test_path.copy()

        breadth_first_path = BFT(test_path[-1], test_path)

        if not breadth_first_path:
            return [direction for _, direction in traversal_path[1:] if direction != '']
        test_path = [*test_path, *breadth_first_path]
        traversal_path = test_path.copy()

# TRAVERSAL TEST
visited_rooms = set()
incomplete_nodes = []
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

traversal_path = traversal(player.current_room)
print(traversal_path)
player = Player(world.starting_room)
visited_rooms = set()
for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
