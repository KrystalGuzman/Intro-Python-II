from room import Room
from player import Player
from item import Item
# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons"),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.  You can always end things here by going "down"."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),

    'abyss':    Room("Abyss", """You realize you are stuck and jump into the abyss. THE END"""),
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['overlook'].d_to = room['abyss']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

# add items to rooms
room['foyer'].add_item(Item("bluepill", "If you swallow it, you remain in blissful ignorance"))
room['foyer'].add_item(Item("redpill", "If you swallow it, it will reveal an unpleasant truth"))
room['overlook'].add_item(Item("gloves", "Common item worn during COVID"))
room['treasure'].add_item(Item("mask", "Common item worn during COVID"))
room['narrow'].add_item(Item("bat", "A dead bat that was lying on the floor makes you feel sick"))

#
# Main
#

def menu():
    print("To move, type 'n', 's', 'e', or 'w'.")
    print("To describe the room, type 'd'.")
    print("To quit, type 'q'.")
    print("To pick up an item, type 'get (item name)' or 'take (item name)'.")
    print("To drop an item, type 'drop (item name).")
    print("To view your inventory, type 'i'.")
    print("To view these instructions again, type 'h'.")

print("Welcome to the Adventure Game")
menu()

direction_abbreviations = {
    "n": "north",
    "s": "south",
    "e": "east",
    "w": "west",
    "down": "down"
}

direction_adj_phrase = {
    "n": "to the north",
    "s": "to the south",
    "e": "to the east",
    "w": "to the west",
    "down": "below"
}

# Make a new player object that is currently in the 'outside' room.

player = Player(room['outside'], "Adventurer #1")

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.

while True:

    # get player's current room
    current_room = player.get_location()
    # prompt for user input
    user_input = input("> ").lower()

    # get all words separated by spaces
    input_words = user_input.strip().split(" ")

    # single-word actions
    if len(input_words) == 1:

        if (user_input == 'q'):
            break

        elif (user_input == 'h'):
            menu()

        elif user_input == "up":
            if current_room == room['outside']:
                player.check_bat()
            else:
                print("There is nothing up there.")

        elif (user_input == 'd'):
            current_room.describe()

        elif (user_input in ['i' , 'inventory']):
            player.show_inventory()

        elif (user_input in direction_abbreviations):

            # check if current room has an exit in the requested direction
            next_room = current_room.get_next_room(user_input)
                
            if next_room:
                # move user to new room
                player.move_to_location(next_room)
                print("You move " + direction_abbreviations[user_input] + ".")
                next_room.describe()
                if user_input == "down":
                    break
                
            else:
                print("There is no exit " + direction_adj_phrase[user_input] + " from here.")
    
    # two-word actions
    elif len(input_words) == 2:

        verb = input_words[0]
        direct_object = input_words[1]

        if (verb in ['get', 'take']):
            player.get_item(direct_object)
        
        elif (verb == 'drop'):
            player.drop_item(direct_object)

        elif (verb == "swallow"):
            player.swallow_item(direct_object)

        # describe item
        if (verb in ['x', 'examine']):
            
            item = player.get_item_by_name(direct_object) or player.current_room.get_item_by_name(direct_object)

            if item:
                print(item.get_description())
            else:
                print("There is no " + direct_object + " here.")

    # print an extra line at the end to separate actions
    print("")