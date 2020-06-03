# Write a class to hold player information, e.g. what room they are in
# currently.

class Player:

    def __init__(self, starting_room, name):
        self.current_room = starting_room
        self.name = name
        self.inventory = []

    def get_location(self):
        return self.current_room

    def move_to_location(self, next_room):
        self.current_room = next_room

    # return the Item object with the specified name if it exists
    def get_item_by_name(self, name):
        requested_item = [item for item in self.inventory if item.get_name() == name]

        if len(requested_item) == 1:
            return requested_item[0]
        else:
            return None

    def get_item(self, item_name):

        # shortcut for getting everything in the room
        if item_name == "all":

            items_in_room = self.current_room.return_items_in_room()

            if len(items_in_room) > 0:

                # print message saying you picked up everything
                for item in items_in_room:
                    item.on_take()

                self.inventory.extend(items_in_room)
                self.current_room.items = []
            else:
                print("There is nothing to take here.")
        
        # add an individual item
        else:
            # check for existence of item in room
            requested_item = self.current_room.get_item_by_name(item_name)

            # add item to inventory if it exists
            # then remove item from the room
            if requested_item:
                self.inventory.append(requested_item)
                self.current_room.remove_item(requested_item)

                # display take message
                requested_item.on_take()
            else:
                print("There is no " + item_name + " here.")

    def drop_item(self, item_name):

        # shortcut for dropping everything in inventory
        if item_name == "all":

            if len(self.inventory) > 0:

                # print message saying you dropped everything
                for item in self.inventory:
                    item.on_drop()

                self.current_room.items.extend(self.inventory)
                self.inventory = []

            else:
                print("You don't have anything left to drop.")
        
        else:
            # check for existence of item in inventory
            requested_item = self.get_item_by_name(item_name)

            # remove item from inventory if it exists
            # then add it to the room
            if requested_item:
                self.inventory.remove(requested_item)
                self.current_room.add_item(requested_item)

                # display drop message
                requested_item.on_drop()

            else:
                print("You don't have " + item_name + " in your inventory!")

    def show_inventory(self):

        if len(self.inventory) > 0:

            print("You are currently carrying the following:")

            item_names = [item.get_name() for item in self.inventory]
            print(", ".join(item_names))
        else:
            print("You don't have a penny to your name.")
    