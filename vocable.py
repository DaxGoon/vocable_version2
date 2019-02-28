"""vocable.py
contains the game logic, ui, main function and other essential elements.

"""

import datetime
import enchant

from classes import Player

# record start time
playtime = datetime.datetime.now()

# create a player_list list to hold player names before we convert them into Player objects
player_list = []
players_data = []

# create a dictionary placeholder for word validation
dictionary_to_use = None

# create the word length placeholder
game_level_word_length = 0


# function to initiate the welcome screen
def welcome_screen():
    # welcome statement
    print(f"""
    -----***** Welcome to VOCABLE *****-----
    Current time: {playtime}

    HERE ARE SOME RULES FOR THE GAME
    --------------------------------
    1. Start with spelling a valid unique word in your chosen language
    2. Your opponent must spell a word starting with the end character of your word
    3. The game continues in a loop
    4. If you enter an invalid word or used word, 1 pass will be taken from your account
    5. You have 3 passes, when the 3rd is taken, you're out of the game
    6. Last remaining person wins the game

    PLEASE REMEMBER THAT WE WILL USE openoffice.org's DICTIONARY. SOME WORDS MIGHT NOT BE AVAILABLE SO BE CERTAIN
    BEFORE USING A WORD.

    Respect your opponent & enjoy the game!

    """)


# function to decide the level of the game the player wants to play and word length according to the game level
def game_level_choice():
    """decides what level of game the player wants to play """
    global game_level_word_length
    print("\nGame difficulty level:")
    print("""
    1. Beginner: any valid words allowed
    2. Advance: only words with minimum 4 characters allowed
    3. Expert: only words with minimum 6 characters allowed
    """)
    while not game_level_word_length:
        game_level_chosen = input("Choose the game level(type: 1, 2 or 3) ")
        if game_level_chosen == "1":
            game_level_word_length = 2
        elif game_level_chosen == "2":
            game_level_word_length = 4
        elif game_level_chosen == "3":
            game_level_word_length = 6
        else:
            print("\nPlease enter a valid number.\n")
            game_level_word_length = 0
            continue
        return game_level_word_length


# function to validate words according to the chosen level
def word_sanitation(input_word, game_level_word_length):
    """:param game_level_word_length: int
    :param input_word: str
    :return: boolean
    """
    if len(input_word) >= game_level_word_length:
        return True
    return False


# function to ask the number of players
def take_player_number():
    """decides player number for registration

    :return: player_number
    :rtype: int
    """
    invalid_number = True
    while invalid_number:
        try:
            player_number = int(input("How many players are you (min. 2)? "))
            if player_number >= 2:
                invalid_number = False
                return player_number
            else:
                invalid_number = True
                print("\nOnly 2 or more people can play this game.")
                continue
        except ValueError:
            print("\nDid you enter a valid number?\nI guess not. Please enter a valid number.\n")
            continue


# function to create a list of players
def create_player_list(player_number):
    """instantiate Player objects as many as player_number

    :param player_number: return value from take_player_number() function.
    :type player_number: int
    """
    global player_list
    for num in range(player_number):
        names_entered = input(f"what is the name of player {num + 1}: ")
        player_list.append(names_entered)
    return player_list


# function to create player objects for players in the list
def create_player_objects(player_list):
    """creates Player objects for each names in player_list and puts them in a new list.

    :param player_list: list containing player names.
    :type player_list: list
    """
    global players_data
    players_data = [Player(name) for name in player_list]
    return players_data


# Create enchant dictionary objects based on language choice of players
def language_choice():
    global dictionary_to_use
    print("\n1. US English\n2. UK English\n3. German(Germany)\n4. French (France)")
    while not dictionary_to_use:
        language_choice_taken = input("Choose a dictionary for words in the game (choose: 1, 2, 3 or 4) ")
        if language_choice_taken == "1":
            dictionary_to_use = enchant.Dict("en_US")
        elif language_choice_taken == "2":
            dictionary_to_use = enchant.Dict("en_GB")
        elif language_choice_taken == "3":
            dictionary_to_use = enchant.Dict("de_DE")
        elif language_choice_taken == "4":
            dictionary_to_use = enchant.Dict("fr_FR")
        else:
            print("\nPlease enter a valid number.\n")
            dictionary_to_use = None
            continue
        return dictionary_to_use


# create word validation logic using enchant
def word_validation(word_to_check):
    """pass a string and returns either True or False. True if the string found in the dictionary_to_use object"""
    return dictionary_to_use.check(word_to_check)


# create repetitive word check function to allow one word only once
def no_repetition(input_word, players_data):
    """takes input_word from game_logic and players_data (Player objects) from create_player_objects.
    Player objects in player_data (a list) contain word_list (a list) attributes.
    :returns: Boolean
    """
    input_word = input_word.lower()  # lowercase the words for comparison
    for player_data in players_data:
        for word in player_data.word_list:
            if word.lower() == input_word:
                return False
    return True


# run the main game logic
def game_logic(players_data):
    """takes in players data and initiates the game logic.

    :param players_data: contains Player objects with name, word_list and pass_taken as attributes.
    :type players_data: list containing dictionaries as items.
    """
    game_switch = True
    valid_word = False
    start_letter = ""
    foul_message = "\n!!¡¡ FOUL¡¡!!!!¡¡ FOUL¡¡!!!!¡¡ FOUL¡¡!!\nThe word was not recognised as a valid word."
    repetition_warning = "\n!!¡¡ WORD REPEATED!!¡¡ WORD REPEATED¡¡!!!!¡¡!!¡¡ WORD REPEATED¡¡!!!!¡¡" \
                         "\nA WORD CAN BE USED ONLY ONCE"
    while game_switch:
        player_turn = players_data[0].name
        if not players_data:  # iff empty list
            print("Something went wrong. I could not find players! Please restart the game.")
            break
        elif len(players_data) == 1:  # when one person is left
            print(f"\n{players_data[0].name.upper()} wins.\nCongratulations!\n°°*°°*°°*°°*°°*°°*° ")
            print(f"Your winning words were:\n"
                  f"{'[%s]' % ', '.join(map(str, players_data[0].word_list))}\nYou must be a wordsmith, Sir/Madam!")
            print(f"beat all opponents in: {(datetime.datetime.now() - playtime).total_seconds()} seconds\n°*°°*°°*°\n")
            break
        else:
            print(f"\nIt is {player_turn.upper()}'s turn")
            # add a copy of first element to the end
            players_data.append(players_data[0])
            # remove the first element so that next turn is next ones'
            players_data.remove(players_data[0])
            # start the game
            while not valid_word:
                if not start_letter:
                    input_word = input(f"please enter a valid word to begin: ")
                    if word_validation(input_word) and word_sanitation(input_word, game_level_word_length):
                        players_data[-1].word_list.append(input_word)
                        start_letter = input_word[-1].upper()
                        print(f"\nStarting letter for next player is: {start_letter}")
                        break
                    else:
                        players_data[-1].pass_taken += 1
                        print(f"\n" + foul_message + f"\nPenalty: 1 pass({3 - players_data[-1].pass_taken} left)\n")
                        print("Turn goes to your opponent.")
                        valid_word = False
                        if players_data[-1].pass_taken >= 3:
                            print(f"LOST!\n{players_data[-1].name.upper()} is out of the game")
                            players_data.pop()
                            continue
                else:
                    input_word = input(f"please enter a valid word beginning with letter {start_letter}: ")
                    if word_validation(input_word) and word_sanitation(input_word, game_level_word_length) and \
                            input_word[0].upper() == start_letter and no_repetition(input_word, players_data):
                        players_data[-1].word_list.append(input_word)
                        start_letter = input_word[-1].upper()
                        print(f"\nStarting letter for next player is: {start_letter}")
                        break
                    elif word_validation(input_word) and word_sanitation(input_word, game_level_word_length) and \
                            input_word[0].upper() == start_letter and not no_repetition(input_word, players_data):
                        players_data[-1].pass_taken += 1
                        print(f"\n" + repetition_warning + f"\nPenalty: 1 pass({3 - players_data[-1].pass_taken} left)")
                        print("\nTurn goes to your opponent.")
                        valid_word = False
                        if players_data[-1].pass_taken >= 3:
                            print(f"LOST!\n{players_data[-1].name.upper()} is out of the game")
                            players_data.pop()
                        break
                    else:
                        players_data[-1].pass_taken += 1
                        print(f"\n" + foul_message + f"\nPenalty: 1 pass({3 - players_data[-1].pass_taken} left)\n")
                        print("Turn goes to your opponent.")
                        valid_word = False
                        if players_data[-1].pass_taken >= 3:
                            print(f"LOST!\n{players_data[-1].name.upper()} is out of the game")
                            players_data.pop()
                        break


# define the main function
def main():
    # show the welcome screen
    welcome_screen()

    # ask number of players
    player_number = take_player_number()

    # create a list of players
    create_player_list(player_number)

    # instantiate Player objects
    create_player_objects(player_list)

    # instantiate the language dictionary to use
    language_choice()

    # decide the game level2
    game_level_choice()

    # initiate the game logic
    game_logic(players_data)


# run the game
if __name__ == "__main__":
    main()
