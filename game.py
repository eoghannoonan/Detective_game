################################################################################
# CMPU 2016 OOP – TU 857/2 - Semester 1 Assignment.
# Group: The Elite Coders.
# Members:
# 1, Daragh Moynihan (Student ID: C22366041)
# 2, Shaheer Rauf (Student ID: C22752015)
# 3, Eoghan Noonan (Student ID:   C22437866)
#
# Date: November 25th, 2023.
# Game Expansion Explanation:
# In this expansion of our mystery game, "SHadow Chronicles," The Elite Coders group
# introduces an exciting new expansion to the game. We have added three different
# locations at which you can solve the mysteries.
#
#
# File Strcuture:
# - main_game.py: The main game script
#
#
#
# Running the Game:
# - To play "The Detective's Enigma" with our exciting expansions, run the
#  "main_game.py" file.
#
#
# Enjoy the game and have fun becoming the ultimate detective!
################################################################################

from abc import ABC, abstractmethod


class Loggable:
    """In this solution, the Loggable class is incorporated as an independent
    class used for handling logging functionality, and the Game class is
    enhanced to use it via composition. """

    def __init__(self):
        self.__logs = []

    @property
    def logs(self):
        return self.__logs

    def log(self, message):
        if isinstance(message, str):
            self.__logs.append(message)


class CrimeScene:

    def __init__(self, location):
        self.location = location
        self.__clues = []
        self.__investigated = False

    @property
    def investigated(self):
        return self.__investigated

    @investigated.setter
    def investigated(self, value):
        self.__investigated = value

    def add_clue(self, clue):
        self.__clues.append(clue)

    def review_clues(self):
        """At the moment there are no checks on who can see the clues. We
        might need some further protection here."""
        return self.__clues


class Character(ABC):

    def __init__(self, name, dialogue):
        self._name = name
        self._dialogue = dialogue
        self._interacted = False

    def __str__(self):
        return f"{self.__class__.__name__}: {self._name}"

    def __eq__(self, other):
        if isinstance(other, Character):
            return self._name == other._name
        return False

    def __lt__(self, other):
        if isinstance(other, Character):
            return self._name < other._name
        return False

    @abstractmethod  # Declares an abstract method using a decorator.
    def perform_action(self):
        pass  # Abstract methods never contain any actual logic. The
        # transfer statement "pass" allows for this.

    # An abstract class must contain at least one abstract method.
    # However, "normal" methods may also be contained.
    def interact(self):
        if not self._interacted:
            interaction = f"{self._name}: {self._dialogue}"
            self._interacted = True
        else:
            interaction = f"{self._name} is no longer interested in talking."

        return interaction


class Suspect(Character):

    def __init__(self, name, dialogue, alibi):
        super().__init__(name, dialogue)
        self._alibi = alibi

    def __repr__(self):
        return f"Suspect('{self._name}', '{self._dialogue}', '{self._alibi}')"

    def provide_alibi(self):
        return f"{self._name}'s Alibi: {self._alibi}"

    def perform_action(self):  # Implement the abstract method for Suspect
        return (f"Suspect {self._name} nervously shifts and avoids eye "
                f"contact.")


class Witness(Character):

    def __init__(self, name, dialogue, observation):
        super().__init__(name, dialogue)
        self._observation = observation

    def __add__(self, other):
        if isinstance(other, Witness):
            combined_observation = f"{self._observation} and {other._observation}"
            combined_name = f"{self._name} and {other._name}"
            return Witness(combined_name, "Combined observations",
                           combined_observation)

    def share_observation(self):
        return (f"{self._name}'s Observation: {self._observation}")

    def perform_action(self):  # Implement the abstract method for Witness
        return (f"Witness {self._name} speaks hurriedly and glances around "
                f"anxiously.")


class NPC(Character):
    """
    A class that implements the abstract class Character.
    The perform_action method must provide logic.
    The purpose of this class is to provide characters that are not
    essential for the mystery.
    """

    def perform_action(self):
        return f"{self._name} decides to hang around and see what will happen."

    def interact(self):
        super().interact()
        return "\nI know nothing!"


class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return f"{self.name}: {self.description}"


class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        """Add an item to the inventory."""
        self.items.append(item)
        print(f"Added '{item.name}' to inventory.")

    def remove_item(self, item_name):
        """Remove an item from the inventory by name."""
        for item in self.items:
            if item.name == item_name:
                self.items.remove(item)
                print(f"Removed '{item_name}' from inventory.")
                return
        print(f"Item '{item_name}' not found in inventory.")

    def list_items(self):
        """List all items in the inventory."""
        if not self.items:
            return "Inventory is empty."
        return '\n'.join(str(item) for item in self.items)


class Location:

    def __init__(self, name, doors, npcs, clues, characters):
        self.name = name
        self.doors = doors
        self.npcs = npcs
        self.clues = clues
        self.characters = characters


# Enhanced Game class using advanced error handling
class Game:

    def __init__(self, starting_locations):
        self.locations = starting_locations
        # The Loggable can be used throughout the game to capture important
        # events, interactions between characters, and observations. The key
        # takeaway is that the Loggable class facilitates logging without
        # tightly coupling the game logic with the logging functionality.
        # This promotes modularity and helps in managing dependencies
        # effectively.
        self.__logger = Loggable()

        # A second logger that is specific to any error logs
        self.__error_logger = Loggable()

        # ... from before:
        self.__running = True
        self.__game_started = False
        self.__characters_interacted = False  # no double interactions
        self.__npcs_interacted = False  # no double interactions

        self.inventory = Inventory()  # Initialize Inventory

        self.__crime_scene = CrimeScene("Mansion's Drawing Room")
        self.__suspect = Suspect("Mr. Smith", "I was in the library all "
                                              "evening.", "Confirmed by the butler.")
        self.__witness = Witness(
            "Ms. Parker", "I saw someone near the window "
                          "at the time of the incident.", "Suspicious figure in dark clothing.")
        self.__doors = ["Front door", "Library door", "Kitchen door"];
        self.__doors_checker = [False, False, False]  # avoid using a door again

        self.__clues = []
        self.current_location = None
        self.current_doors = []

    # ---
    # property methods first
    # ---

    @property
    def log(self):
        # to do: think of some appropriate access checks here. For example,
        # only admins are allowed to read out logs.
        return self.__logger

    @property
    def error_log(self):
        return self.__error_logger

    def find_specific_item(self, item_name):
        """Function to find a specific item based on its name."""
        item_descriptions = {
            "Antique Pocket Watch": "An elegantly crafted pocket watch, its hands frozen at the exact time of the crime.",
            "Faded Diary": "An old diary with torn pages, hinting at deep secrets.",
            "Silver Key": "A small, ornate key with mysterious engravings.",
            "Broken Locket": "A locket with a torn photo, possibly of a suspect.",
            "Mysterious Potion": "A vial filled with a shimmering liquid, purpose unknown.",
            "Ancient Map": "A tattered map showing hidden passages within the manor."
        }
        description = item_descriptions.get(item_name, "Unknown item")
        self.find_item(item_name, description)

    def find_item(self, item_name, item_description):
        """Find an item and add it to the inventory."""
        item = Item(item_name, item_description)
        self.inventory.add_item(item)

    def drop_item(self):
        """Drop an item from the inventory."""
        item_name = input("Enter the name of the item to drop: ")
        self.inventory.remove_item(item_name)

    def display_inventory(self):
        """Display the current items in the inventory."""
        print("Inventory:")
        print(self.inventory.list_items())

    # This method has been updated to show error handling. Inspect the log
    # carefully after running the game.
    def run(self):
        # ...
        self.__logger.log("Game started")
        # ...
        print("Welcome to 'The Shadow Chronicles Mystery Game'")
        print("You are about to embark on a thrilling adventure as a detective.")
        print("Your expertise is needed to solve a complex case and unveil the truth.")

        while self.__running:
            try:
                self.update()
            except ValueError as ve:
                self.__error_logger.log(f"Error found:\n {ve}.")
            except Exception as e:
                self.__error_logger.log("Unexpected error from run():\n{e}.")
                print("Unexpected caught error during running of the Game. "
                      "We continue playing...")
            else:
                self.__logger.log("Successfully updating")
            finally:
                self.__logger.log("---")

    def update(self):
        # ...
        self.__logger.log("I'm updating")
        # ...

        if not self.__game_started:
            player_input = input("Press 'q' to quit or 's' to start: ")
            if player_input.lower() == "q":
                self.__running = False
            elif player_input.lower() == "s":
                self.__game_started = True
                self.start_game()
            else:
                raise ValueError("Incorrect user entry.")
        else:
            player_input = input(
                "Press 'q' to quit, 'c' to continue, 'i' to interact, "
                "'e' to examine clues, 'r' to review clues, 'd' to choose a "
                "door, 'inventory' to view inventory: ")

            # Logging the user input to keep a record of what the player is
            # choosing.
            self.__logger.log(f"Player input is {player_input}.")

            if player_input.lower() == "a":
                if hasattr(self, 'current_item') and self.current_location.name == self.current_item_location:
                    self.find_specific_item(self.current_item)
                    del self.current_item  # Remove the attribute after interaction
                    del self.current_item_location  # Remove the location attribute
                else:
                    print("There is nothing to interact with here or you're in the wrong location.")

            if player_input.lower() == "q":
                self.__running = False
            elif player_input.lower() == "c":
                self.continue_game()
            elif player_input.lower() == "i":
                try:
                    self.interact_with_characters()
                except ValueError as ve:
                    self.__error_logger.log(f"Error found:\n {ve}.")
                    print("Invalid character option.")
                except Exception as e:
                    self.__error_logger.log(f"Unexpected exception found for "
                                            f"player input to interact with "
                                            f"characters:\n{e}")
                    print("Unexpected error found for player input to "
                          "interact with character. We continue playing...")
            elif player_input.lower() == "e":
                self.examine_clues()

            elif player_input == "inventory":
                self.display_inventory()
            elif player_input.startswith("find "):
                # Command format: find [item_name]
                item_name = player_input.split(maxsplit=1)[1]
                self.find_item(item_name, "A description of the item")
            elif player_input.startswith("drop "):
                # Command format: drop [item_name]
                item_name = player_input.split(maxsplit=1)[1]
                self.drop_item()
            elif player_input.lower() == "d":
                try:
                    self.choose_door()
                except ValueError as ve:
                    print("This door choice does not exist.")
                    self.__error_logger.log(f"Error found:\n{ve}")
                except Exception as e:
                    self.__error_logger.log(f"Unexpected error found for "
                                            f"player input:\n{e}")
                    print("Unexpected error from player input. We continue "
                          "playing...")
            elif player_input.lower() == "r":
                clues = self.__crime_scene.review_clues()
                if clues:
                    print(clues)
                else:
                    print("You have not found any clues yet.")
            else:
                raise ValueError("Incorrect user game option choice made.")

    def start_game(self):
        # ...
        self.__logger.log("Game is starting")
        # ...

        # from before...
        player_name = input("Enter your detective's name: ")
        print(f"Welcome, Detective {player_name}!")
        print(
            "As the famous detective, you're here to solve the mysterious case of..."
        )

        while True:
            try:
                for idx, location in enumerate(self.locations, start=1):
                    print(f"{idx}. {location.name}")

                user_choice = int(input("Enter the number of the location you want to start at: "))
                if 1 <= user_choice <= len(self.locations):
                    self.current_location = self.locations[user_choice - 1]
                    self.current_doors = self.current_location.doors
                    print(f"You have chosen to start at the {self.current_location.name}. Let the mystery begin!")
                    break
                else:
                    print("Invalid location choice. Please enter a valid number.")
            except ValueError:
                print("Please enter a valid number for location selection.")

    def interact_with_characters(self):
        """The interact_with_characters method within the Game class
        demonstrates the interaction with characters,
        where each character's dialogue and unique actions (e.g., providing
        an alibi, sharing an observation) are displayed. """

        # ...
        self.__logger.log("Interactions happening")
        # ...
        print("You decide to interact with the characters in the room.")
        character = int(
            input("If you want to speak to the witness and a "
                  "suspect, "
                  "choose 1. \nIf you'd like to speak to other people in "
                  "the "
                  "room, choose 2: "))

        if character == 1:
            if not self.__characters_interacted:
                self.__logger.log("Interacting with suspects and witnesses.")
                print("You decide to interact with the witness and suspect in "
                      "the room:")

                clue_suspect = self.__suspect.interact()
                self.__crime_scene.add_clue(clue_suspect)
                print(clue_suspect)  # keep the outputs going

                suspect_alibi = self.__suspect.provide_alibi()
                self.__crime_scene.add_clue(suspect_alibi)
                print(suspect_alibi)

                # use the new abstract method
                print(self.__suspect.perform_action())

                clue_witness = self.__witness.interact()
                self.__crime_scene.add_clue(clue_witness)
                print(clue_witness)

                witness_observation = self.__witness.share_observation()
                self.__crime_scene.add_clue(witness_observation)
                print(witness_observation)

                # use the new abstract method
                print(self.__witness.perform_action())

                self.__characters_interacted = True
            else:
                print("You have already interacted with the characters. They no "
                      "longer wish to speak to you.")
        elif character == 2:
            if not self.__npcs_interacted:
                self.__logger.log("Interating with people standing about.")
                # Creating and interacting with characters
                print("You decide to speak to other people in the room:")
                indifferent_npc = NPC("Beatrice", "How do you do.")
                friendly_npc = NPC("Seamus", "Welcome to our village.")
                hostile_npc = NPC("Evil Goblin", "Leave this place!")

                characters = [indifferent_npc, friendly_npc, hostile_npc]

                for character in characters:
                    print(character.interact())
                    print(character.perform_action())

                self.__crime_scene.add_clue("Three people are hanging around the "
                                            "scene who have nothing to do with the "
                                            "crime.")

                self.__npcs_interacted = True
            else:
                print("People in the room are tied of you. They no longer "
                      "want to speak to you.")
        else:
            raise ValueError("This is not an option for a character.")
            # print("This was not an option.")

    def examine_clues(self):
        # Log examination activity
        self.__logger.log("Examination happening")

        # Check if the clues at the current crime scene have already been investigated
        if not self.__crime_scene.investigated:
            # Determine what happens based on the current location
            if self.current_location.name == "Mysic Manor":
                print("You find a Mysterious Letter near the fireplace.")
                mysterious_letter = Item("Mysterious Letter", "An old, sealed letter with an unbroken wax seal.")
                self.inventory.add_item(mysterious_letter)
                self.__crime_scene.add_clue("Found Mysterious Letter")

            elif self.current_location.name == "Whispering Woods":
                print("You find a Golden Key hidden beneath a fallen tree branch.")
                golden_key = Item("Golden Key", "An intricately designed key, glistening with a golden hue.")
                self.inventory.add_item(golden_key)
                self.__crime_scene.add_clue("Found Golden Key")

            elif self.current_location.name == "Cryptic Crossroads":
                print("You unearth an Engraved Stone buried in the ground.")
                engraved_stone = Item("Engraved Stone", "A small stone with mysterious symbols engraved on it.")
                self.inventory.add_item(engraved_stone)
                self.__crime_scene.add_clue("Found Engraved Stone")

            # Mark the crime scene as investigated
            self.__crime_scene.investigated = True

        else:
            print("You've already examined the crime scene clues.")

    def choose_door(self):
        # ...
        self.__logger.log("Doors are to be chosen")
        # ...

        print("You decide to choose a door to investigate:")

        # nice output to show which door leads to what.
        for i, door in enumerate(self.current_doors, start=1):
            print(f"{i}. {door}")

        door_choice = int(input("Enter the number of the door you want to investigate: "))
        self.__logger.log(f"Player chooses to investigate door {door_choice}.")

        if 0 < door_choice <= len(self.current_doors):
            chosen_door = self.current_doors[door_choice - 1]

            if chosen_door not in self.__crime_scene.review_clues():
                print(f"You investigate the {chosen_door}.")
                self.__crime_scene.add_clue(f"Investigated {chosen_door}")

                if self.current_location.name == "Mysic Manor" and door_choice == 2:
                    print("You enter the library and notice an Antique Pocket Watch.")
                    self.current_item = "Antique Pocket Watch"
                    self.current_item_location = "Mysic Manor"  # Store the location

                elif self.current_location.name == "Whispering Woods":
                    # Handling for bunker door
                    if chosen_door == "Underground Bunker":
                        if any(item.name == "Golden Key" for item in self.inventory.items):
                            print("Using the Golden Key, you unlock the bunker door.")
                            # Additional code to handle bunker exploration
                        else:
                            print("The bunker door is locked. You need a Golden Key to open it.")
                            return  # Prevent adding items if bunker is locked



                # Add conditions for other locations as necessary

            else:
                print(f"You've already investigated the {chosen_door}.")
        else:
            print("Invalid door choice.")

    def continue_game(self):
        print(
            "You continue your investigation, determined to solve the mystery...")
        # ...
        self.__logger.log("Continuing the game.")
        # ...

        # Additional game content and interactions could go here


# Testing the Enhanced Game
if __name__ == "__main__":
    starting_locations = [
        Location("Mysic Manor", ["Front door", "Library door", "Kitchen door"],
                 ["Butler", "Maid"], ["Bloody footprint", "Torn fabric"],
                 ["Detective", "Suspect", "Witness"]),
        Location("Whispering Woods", ["Cabin", "Underground Bunker", "Campsite"],
                 ["Camper", "Soldier"], ["Ancient tome", "Secret passage"],
                 ["Detective", "Suspect", "Witness"]),
        Location("Cryptic Crossroads", ["Dark Alley", "Main Road", "Carpark"],
                 ["Dog walker", "Shady guy"], ["Bloody footprint", "Torn fabric"],
                 ["Detective", "Suspect", "Witness"])
    ]
    game = Game(starting_locations)
    game.run()

    # Using the logger
    print("\nGame Logs:")
    for log in game.log.logs:
        print(log)

    print("\nGame Error Logs:")
    for log in game.error_log.logs:
        print(log)
