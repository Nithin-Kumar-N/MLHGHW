import random

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.inventory = []
        self.score = 0

    def display_status(self):
        print(f"{self.name}'s Health: {self.health}")
        print(f"Inventory: {', '.join(self.inventory)}")
        print(f"Score: {self.score}")

    def heal(self):
        if "Health Potion" in self.inventory:
            self.health += 20
            if self.health > 100:
                self.health = 100
            self.inventory.remove("Health Potion")
            print("You used a Health Potion and healed yourself.")
        else:
            print("You don't have any Health Potions.")

    def use_item(self, item):
        if item in self.inventory:
            if item == "Health Potion":
                self.heal()
            elif item == "Torch":
                print("You use the torch to light up the room.")
                print("The light reveals hidden treasures!")
                self.score += 50
            elif item == "Magic Amulet":
                print("The magic amulet protects you from the next monster encounter.")
                self.inventory.remove("Magic Amulet")
            # Add more item interactions as needed
            else:
                print("You cannot use this item right now.")
        else:
            print("You don't have that item.")

class Room:
    def __init__(self, description, treasure=None, monster=None, healing_item=None, puzzle=None):
        self.description = description
        self.treasure = treasure
        self.monster = monster
        self.healing_item = healing_item
        self.puzzle = puzzle

class Dungeon:
    def __init__(self):
        self.rooms = []
        self.player = None

    def add_room(self, room):
        self.rooms.append(room)

    def set_player(self, player):
        self.player = player

    def explore(self):
        print("Welcome to the dungeon! Let's start exploring...")
        current_room_index = 0

        while True:
            current_room = self.rooms[current_room_index]
            print("\n" + current_room.description)

            if current_room.treasure:
                print(f"You found {current_room.treasure}!")
                self.player.inventory.append(current_room.treasure)
                self.player.score += 100
                current_room.treasure = None

            if current_room.monster:
                if "Magic Amulet" in self.player.inventory:
                    print("The magic amulet protects you from the monster!")
                    self.player.inventory.remove("Magic Amulet")
                else:
                    print("Oh no! You encountered a monster!")
                    self.player.health -= random.randint(10, 30)
                    if self.player.health <= 0:
                        print("Game over! You were defeated by the monster.")
                        break

            if current_room.healing_item:
                print(f"You found a {current_room.healing_item}!")
                self.player.inventory.append(current_room.healing_item)
                current_room.healing_item = None

            if current_room.puzzle:
                print("You encounter a puzzle!")
                if self.solve_puzzle(current_room.puzzle):
                    print("Congratulations! You solved the puzzle!")
                    self.player.score += 150
                else:
                    print("Oops! The puzzle defeated you.")
                    break

            self.player.display_status()

            if current_room_index == len(self.rooms) - 1:
                print("Congratulations! You successfully explored the dungeon and found the exit.")
                print(f"Final Score: {self.player.score}")
                break

            action = input("What will you do? (move/heal/use item): ").lower()
            if action == "move":
                direction = input("Which direction will you go? (left/right/straight/back): ").lower()
                if direction == "back":
                    if current_room_index == 0:
                        print("You cannot go back from here.")
                    else:
                        current_room_index -= 1
                elif direction in ["left", "right", "straight"]:
                    current_room_index += 1
                else:
                    print("Invalid direction! Try again.")
            elif action == "heal":
                self.player.heal()
            elif action == "use item":
                item = input("Which item will you use? ").capitalize()
                self.player.use_item(item)
            else:
                print("Invalid action! Try again.")

    def solve_puzzle(self, puzzle):
        print(f"Here is the puzzle: {puzzle}")
        solution = input("Enter your solution: ").lower()
        return solution == "solve"  # Change this to match your puzzle solution

# Define the player
player_name = input("Enter your name: ")
player = Player(player_name)

# Create the dungeon
dungeon = Dungeon()
dungeon.set_player(player)

# Define rooms
room1 = Room("You are at the entrance of the dungeon.")
room2 = Room("You entered a dark corridor.", monster="Goblin")
room3 = Room("You found a room with a dimly lit torch.", treasure="Gold Coin")
room4 = Room("You see a staircase leading downwards.", healing_item="Health Potion")
room5 = Room("You stumbled upon a chamber filled with ancient artifacts.", puzzle="What word starts with 'e' and ends with 'e' but only has one letter?")

# Add rooms to the dungeon
dungeon.add_room(room1)
dungeon.add_room(room2)
dungeon.add_room(room3)
dungeon.add_room(room4)
dungeon.add_room(room5)

# Start exploring the dungeon
dungeon.explore()
