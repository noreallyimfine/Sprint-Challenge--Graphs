from room import Room
from player import Player
from world import World
from util import Stack, Queue

import random
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


def reverse(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'w':
        return 'e'
    elif direction == 'e':
        return 'w'

def new_entry(room, visited_rooms):
    visited_rooms[room.id] = {}
    for direction in room.get_exits():
        visited_rooms[room.id][direction] = "?"

def bfs(player, visited_rooms):
    room = player.current_room
    q = Queue()
    q.enqueue([room.id])
    visited = set()
    
    while q.size() > 0:
        path = q.dequeue()
        last = path[-1]
        if last not in visited:
            visited.add(last)
            for direction in visited_rooms[last]:
                if visited_rooms[last][direction] == "?":
                    return path
                elif visited_rooms[last][direction] not in visited:
                    path_copy = path.copy()
                    path_copy.append(visited_rooms[last][direction])
                    q.enqueue(path_copy)
    return path


traversal_path = []

visited_rooms = {}
while len(visited_rooms) < len(room_graph):
    if player.current_room.id not in visited_rooms:
        new_entry(player.current_room, visited_rooms)
    
    new_exits = []
    for direction in visited_rooms[player.current_room.id]:
        if visited_rooms[player.current_room.id][direction] == "?":
            new_exits.append(direction)

    if len(new_exits) > 0:
        new_exit = random.choice(new_exits)
        traversal_path.append(new_exit)
        new_room = player.current_room.get_room_in_direction(new_exit)
        visited_rooms[player.current_room.id][new_exit] = new_room.id 
        if new_room.id not in visited_rooms:
            new_entry(new_room, visited_rooms)
        
        reverse_dir = reverse(new_exit)
        visited_rooms[new_room.id][reverse_dir]
        player.travel(new_exit)
    
    else:
        path = bfs(player, visited_rooms)
        for id in path:
            for direction in visited_rooms[player.current_room.id]:
                if direction in visited_rooms[player.current_room.id]:
                    if visited_rooms[player.current_room.id][direction] == id and player.current_room.id != id:
                        traversal_path.append(direction)
                        new_room = player.current_room.get_room_in_direction(direction)
                        visited_rooms[player.current_room.id][direction] = new_room.id 
                        if new_room.id not in visited_rooms:
                            new_entry(new_room, visited_rooms)
                        
                        reverse_dir = reverse(direction)
                        visited_rooms[new_room.id][reverse_dir] = player.current_room.id
                        player.travel(direction)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

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
