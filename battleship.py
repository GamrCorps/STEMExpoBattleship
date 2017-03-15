#!/usr/bin/env python3

from string import ascii_uppercase
from re import fullmatch
from time import sleep

# Default game presets.
normal_mode_preset = {'height': 10, 'width': 10, '5_ships': 1, '4_ships': 1, '3_ships': 2, '2_ships': 1, '1_ships': 0, 'allow_mines': False, 'allow_moves': False, 'mine_turns': None, 'p_type': 'CPU'}
advanced_mode_preset = {'height': 15, 'width': 15, '5_ships': 2, '4_ships': 2, '3_ships': 2, '2_ships': 1, '1_ships': 0, 'allow_mines': True, 'allow_moves': True, 'mine_turns': 5, 'p_type': 'CPU'}

# Miscellaneous global values.
letters = ascii_uppercase


class Utils(object):
    """
    Utility class used for getting input and other common functions.

    Contains many functions to save space by condensing input and custom string formatting methods into one place.
    All methods are static, and do not modify parameters in-place.
    """
    @staticmethod
    def box_string(string, min_width=-1, print_string=False):
        """
        Place a string into an ASCII box.

        The result is placed inside of a ASCII box consisting of '+' characters for the corners and '-' characters for the edges.

        Parameters
        ----------
        string : str
            String to be boxed.
        min_width : int, optional
            Specifies that the box be of a certain minimum width. Defaults to input string width.
        print_string : bool, optional
            If True, prints the string after building it. Defaults to False.

        Returns
        -------
        str
            Input string with a box around it.

        """
        # Parameters.
        split_string = string.split('\n')
        height = len(split_string)
        length = max(min_width, *[len(x) for x in split_string])

        # String builder.
        result = '+' + '-' * (length + 2) + '+\n'
        for i in range(height):
            result += '| %s |\n' % split_string[i].center(length)
        result += '+' + '-' * (length + 2) + '+'

        # Print and return result.
        if print_string:
            print(result)
        return result

    @staticmethod
    def num_input(question, *choices):
        """
        Take user input based on several different options.

        The input question will be repeated until valid input is given.
        The choices will be displayed in order with a number next to them indicating their id.
        Responses can be given as the choice id or the full choice name.

        Parameters
        ----------
        question : str
            String to be displayed as the input question. Will be boxed with Utils#box_string before printing.
        *choices : *str
            Options for the user to choose from.

        Returns
        -------
        int
            Number of the answer choice, corresponding to the index of the choice in *choices.
        """
        error = ''
        while True:
            # Print question and ask for input.
            Utils.box_string((error + '\n' + question).strip(), print_string=True)
            for i in range(len(choices)):
                print('%d: %s' % (i, choices[i]))
            response = input('Response: ')

            # Test whether input is an integer or string.
            if fullmatch(r'\d+', response.strip()):
                to_int = int(response.strip())
                # Determine if input integer corresponds to one of the answer choices.
                if to_int < len(choices):
                    return to_int
                else:
                    error = 'ERROR: Invalid input! Input integer is not one of the available choices! Please try again.'
                continue
            else:
                # Determine if input string is one of the answer choices.
                for i in range(len(choices)):
                    if response.strip().lower() == choices[i].strip().lower():
                        return i
                error = 'ERROR: Invalid input! Input string is not one of the available choices! Please try again.'
                continue

    @staticmethod
    def string_input(question, condition=r'.+'):
        """
        Take string-based user input.

        The input question will be repeated until valid input is given, determined by the condition regex.

        Parameters
        ----------
        question : str
            String to be displayed as the input question. Will be boxed with Utils#box_string before printing.
        condition : r-string, optional
            Regex to test input string off of.

        Returns
        -------
        str
            Input string.
        """
        error = ''
        while True:
            # Print question and ask for input.
            Utils.box_string((error + '\n' + question).strip(), print_string=True)
            response = input()

            # Test if input is valid.
            if fullmatch(condition, response):
                return response
            else:
                error = 'ERROR: Invalid input! Please try again.'
                continue

    @staticmethod
    def print_settings(settings):
        """
        Pretty-print a settings dictionary.

        Parameters
        ----------
        settings : dict
            The settings dictionary to pretty-print.

        Returns
        -------
            None
        """
        Utils.box_string('Current Settings', print_string=True)

        print('Grid Size:')
        print('\tWidth: %d' % settings['width'])
        print('\tHeight: %d' % settings['height'])

        print('Ship Amount:')
        print('\t5-Long Ships: %d' % settings['5_ships'])
        print('\t4-Long Ships: %d' % settings['4_ships'])
        print('\t3-Long Ships: %d' % settings['3_ships'])
        print('\t2-Long Ships: %d' % settings['2_ships'])
        print('\t1-Long Ships: %d' % settings['1_ships'])

        print('Special Abilities:')
        print('\tShip Moving: %s' % str(settings['allow_moves']))
        print('\tMines: %s' % str(settings['allow_mines']))
        if settings['allow_mines']:
            print('\tTurns Between Mines: %d' % settings['mine_turns'])

        print('Game Type: Player vs. %s' % settings['p_type'])

    @staticmethod
    def grid_pos_input(height, width, question='Enter a Position:'):
        """
        Take user-input in coordinate form.

        The input question will be repeated until valid input is given.
        The input must be a valid coordinate in battleship form (r'[A-Z]\d+').
        The input coordinate must be inside of the grid defined by height and width.

        Parameters
        ----------
        height : int
            Specifies the height of the grid.
        width : int
            Specifies the width of the grid.
        question : str, optional
            String to be displayed as the input question. Will be boxed with Utils#box_string before printing. Defaults to 'Enter a Position'.

        Returns
        -------
        tuple
            Contains the following:
                int
                    Height-aligned position (y-position) of input.
                int
                    Width-aligned position (x-position) of input.
        """
        error = ''
        while True:
            # Print the question and ask for input.
            Utils.box_string((error + '\n' + question).strip(), print_string=True)
            loc = input()

            # Test if input is a valid coordinate and is in the grid.
            if not fullmatch(r'[A-Z][1-2]?[0-9]', loc):
                error = 'ERROR: Invalid input! Input string is not a valid coordinate! Please try again.'
                continue
            elif loc[0] in letters[:height] and 0 < int(loc[1:]) <= width:
                return letters.index(loc[0]), int(loc[1:]) - 1
            else:
                error = 'ERROR: Invalid input! Input string is not in the grid! Please try again.'
                continue


class BattleshipGame(object):
    """
    Class that handles game execution and running.

    Controls game setup based off of a certain settings preset.
    Handles all input and output for the game.

    Attributes
    ----------
    settings : dict
        Settings that the game is running based off of.
    height : int
        Height of the grids used for the game.
    width : int
        Width of the grids used for the game.
    p1_grid : list
        Two dimensional list of ints containing player 1's board.
    p1_grid_2 : list
        Two dimensional list of ints containing player 1's guesses.
    p1_ships : list
        List of player 1's ship dicts with position, direction, and size data.
    p2_grid : list
        Two dimensional list of ints containing player 2's board.
    p2_grid_2 : list
        Two dimensional list of ints containing player 2's guesses.
    p2_ships : list
        List of player 2's ship dicts with position, direction, and size data.
    p2_cpu : bool
        True if player 2 is not a human player, False otherwise.
    turn : int
        Current turn number.
    stage : int
        Current game stage:
            0: Setup stage.
            1: Play stage.
            2: Post-play/cleanup stage.
    """
    def __init__(self, settings):
        """
        Constructor for the BattleshipGame class.

        Parameters
        ----------
        settings : dict
            Settings to create the game based off of.
        """
        # Grid attributes.
        self.settings = settings
        self.height = settings['height']
        self.width = settings['width']

        # Player 1 grids.
        self.p1_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.p1_grid_2 = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.p1_ships = []

        # Player 2 grids.
        self.p2_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.p2_grid_2 = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.p2_ships = []

        # Miscellaneous attributes.
        self.p2_cpu = settings['p_type'] == 'CPU'
        self.turn = 0
        self.stage = 0  # Stages: 0=Setup, 1=Play, 2=Post

    def print_board(self, player):
        """
        Pretty-print the current boards of a player.

        Prints both boards for a player, along with coordinate references, titles, and boxes around the grids.

        Parameters
        ----------
        player : int
            Determines which player's grids to print. Zero-indexed.

        Returns
        -------
        str
            Same as the string that is printed.
        """
        # Characters to use while printing.
        characters = '.' + letters + '*O#'  # 0:Null, 1-26:Ships, 27:Hit, 28:Miss, 29:Mine

        # Place ships into grid, if not already.
        if player == 0:  # Player 1
            board = self.p1_grid
            board_2 = self.p1_grid_2
            for ship in self.p1_ships:
                if ship['direction'] == 0:
                    for i in range(ship['size']):
                        if board[ship['y_pos']][ship['x_pos'] + i] == 0:
                            board[ship['y_pos']][ship['x_pos'] + i] = ship['num'] + 1
                else:
                    for j in range(ship['size']):
                        if board[ship['y_pos'] + j][ship['x_pos']] == 0:
                            board[ship['y_pos'] + j][ship['x_pos']] = ship['num'] + 1
        else:  # Player 2
            board = self.p2_grid
            board_2 = self.p2_grid_2
            for ship in self.p2_ships:
                if ship['direction'] == 0:
                    for i in range(ship['size']):
                        if board[ship['y_pos']][ship['x_pos'] + i] == 0:
                            board[ship['y_pos']][ship['x_pos'] + i] = ship['num'] + 1
                else:
                    for j in range(ship['size']):
                        if board[ship['y_pos'] + j][ship['x_pos']] == 0:
                            board[ship['y_pos'] + j][ship['x_pos']] = ship['num'] + 1
        # Build header.
        result = '    +' + '-' * (self.width * 2 + 1) + '+' + '-' * (self.width * 2 + 1) + '+\n'
        result += '    |' + 'Your Board'.center(self.width * 2 + 1) + '|' + 'Their Board'.center(self.width * 2 + 1) + '|\n'
        result += '    +' + '-' * (self.width * 2 + 1) + '+' + '-' * (self.width * 2 + 1) + '+\n'

        # Build x-coordinate reference.
        if self.width > 9:
            result += '    | ' + ' '.join([str(x + 1).rjust(2)[0] for x in range(self.width)]) + ' | ' + ' '.join([str(x + 1).rjust(2)[0] for x in range(self.width)]) + ' |\n'
        result += '    | ' + ' '.join([str(x + 1).rjust(2)[1] for x in range(self.width)]) + ' | ' + ' '.join([str(x + 1).rjust(2)[1] for x in range(self.width)]) + ' |\n'
        result += '+---+' + '-' * (self.width * 2 + 1) + '+' + '-' * (self.width * 2 + 1) + '+\n'

        # Build y-coordinate reference and grid.
        for i in range(self.height):
            result += '| ' + letters[i] + ' | ' + ' '.join([characters[x] for x in board[i]]) + ' | ' + ' '.join([characters[x] for x in board_2[i]]) + ' |\n'
        result += '+---+' + '-' * (self.width * 2 + 1) + '+' + '-' * (self.width * 2 + 1) + '+\n'

        # Print and return result.
        print(result)
        return result

    def setup_ship(self, pos, direction, player, count, size):
        """
        Create a ship.

        Creates a ship dictionary based on positional, directional, player, and size data and tests if placement is legal.

        Parameters
        ----------
        pos : tuple
            (y,x) coordinate pair of top-left corner of the ship.
        direction : int
            Determines the direction of the ship:
                0: Horizontal.
                1: Vertical.
        player : int
            Determines which player to assign the ship to. Zero-indexed.
        count : int
            Current ship count for internal tracking use.
        size : int
            Length of the ship.

        Returns
        -------
        str
            Error string if an error occurred, None otherwise.
        """
        try:
            # Test if the ship does not overlap another ship.
            if player == 0:  # Player 1
                board = self.p1_grid
                if direction == 0:
                    for i in range(size):
                        if board[pos[0]][pos[1] + i] != 0:
                            return 'ERROR: You cannot place a ship on top of another!'
                else:
                    for j in range(size):
                        if board[pos[0] + j][pos[1]] != 0:
                            return 'ERROR: You cannot place a ship on top of another!'
            else:  # Player 2
                board = self.p2_grid
                if direction == 0:
                    for i in range(size):
                        if board[pos[0]][pos[1] + i] != 0:
                            return 'ERROR: You cannot place a ship on top of another!'
                else:
                    for j in range(size):
                        if board[pos[0] + j][pos[1]] != 0:
                            return 'ERROR: You cannot place a ship on top of another!'
        except IndexError:
            # Catch if ship would be placed out-of-bounds.
            return 'ERROR: You must place a ship inside the grid boundaries!'

        # Create the ship's dictionary and append it to the player's ship list.
        if player == 0:
            self.p1_ships.append({'num': count, 'size': size, 'x_pos': pos[1], 'y_pos': pos[0], 'direction': direction})
        else:
            self.p2_ships.append({'num': count, 'size': size, 'x_pos': pos[1], 'y_pos': pos[0], 'direction': direction})

        return None

    def setup_ships(self, size, player, count):
        """
        Setup all the ships of a particular size for a certain player.

        Sets up all of the length-n size ships for a player.
        Count is not updated in-place.

        Parameters
        ----------
        size : int
            Length of the ships.
        player : int
            Determines which player to assign the ships to. Zero-indexed.
        count : int
            Current ship count for internal tracking use.

        Returns
        -------
        int
            The updated cumulative ship count.
        """
        # Setup number of ships based on value defined in game settings.
        for i in range(self.settings['%d_ships' % size]):
            error = ''
            while True:
                # Print current board for player reference.
                self.print_board(player)

                # Take ship details from player.
                pos = Utils.grid_pos_input(self.height, self.width, question=(error + '\nWhere do you want to place ship \'%s\' (%d-long)' % (letters[count], size)).strip())
                direction = Utils.num_input('Which direction?', 'Horizontal', 'Vertical')

                # Determine if the ship needs to be inputted again.
                error = self.setup_ship(pos, direction, player, count, size)
                if error is None:
                    break
            count += 1

        # Return updated cumulative ship total.
        return count

    def start_game(self):
        """
        Start a new game.

        Starts a game with the settings provided in the constructor.
        All game code is contained here, with relevant helper methods also called here.
        Every game has three stages: Setup, Play, and Post-Play/Cleanup.

        Returns
        -------
        int
            Winning player's number. Zero-indexed.
        """
        # Setup Phase:
        # In this stage, both players choose where to place their ships.
        Utils.box_string('Setup Phase', min_width=self.width * 4 + 5, print_string=True)

        # Test if Player 2 is a human.
        if not self.p2_cpu:
            # Alert Player 2 to look away.
            Utils.box_string('Player 2, please look away.', min_width=self.width * 4 + 5, print_string=True)
            sleep(5)

        # Player 1
        Utils.box_string('Player 1 Setup', min_width=self.width * 4 + 5, print_string=True)
        p1_ship_count = 0
        for i in range(5):
            p1_ship_count = self.setup_ships(i + 1, 0, p1_ship_count)

        # Test if Player 2 is a human.
        if self.p2_cpu:  # Player 2 is Not a Human
            # TODO: SETUP CPU SHIPS
            pass
        else:  # Player 2 is a Human
            # Alert Player 1 to look away.
            Utils.box_string('Player 1, please look away.', min_width=self.width * 4 + 5, print_string=True)
            sleep(5)

            # Player 2
            Utils.box_string('Player 2 Setup', min_width=self.width * 4 + 5, print_string=True)
            p2_ship_count = 0
            for i in range(5):
                p2_ship_count = self.setup_ships(i + 1, 1, p2_ship_count)

        # Update stage number.
        self.stage = 1
        # TODO: PLAY STAGE
        # TODO: POST-PLAY STAGE


def create_game(gm):
    """
    Configure and create a game.

    Creates a game with base settings equivalent to one of the default presets.
    Allows user to customize the settings before starting the game.

    Parameters
    ----------
    gm : int
        Game type to replicate:
            0: Normal mode.
            1: Advanced mode.

    Returns
    -------
    BattleshipGame
        Game instance with user-chosen settings.
    """
    # Choose and print default settings.
    if gm == 0:
        Utils.box_string('Normal Mode', print_string=True)
        settings = normal_mode_preset
    else:
        Utils.box_string('Advanced Mode', print_string=True)
        settings = advanced_mode_preset

    # Print current settings.
    Utils.print_settings(settings)

    # Change settings, if applicable.
    if Utils.num_input('Would you like to change the settings?', 'No', 'Yes') == 1:
        while True:
            # Determine which setting group to modify.
            setting = Utils.num_input('Settings', 'Grid Size', 'Ship Amount', 'Special Abilities', 'Game Type', 'Exit')

            # Modify setting groups.

            if setting == 0:  # Grid Size
                # Take grid dimensions.
                settings['width'] = int(Utils.string_input('Grid Width (5-26)', condition=r'^[5-9]$|^1[0-9]$|^2[0-6]$'))
                settings['height'] = int(Utils.string_input('Grid Height (5-26)', condition=r'^[5-9]$|^1[0-9]$|^2[0-6]$'))

            elif setting == 1:  # Ship Amount
                while True:
                    # Take ship amounts.
                    settings['5_ships'] = int(Utils.string_input('5-Long Ships (0-9)', condition=r'[0-9]'))
                    settings['4_ships'] = int(Utils.string_input('4-Long Ships (0-9)', condition=r'[0-9]'))
                    settings['3_ships'] = int(Utils.string_input('3-Long Ships (0-9)', condition=r'[0-9]'))
                    settings['2_ships'] = int(Utils.string_input('2-Long Ships (0-9)', condition=r'[0-9]'))
                    settings['1_ships'] = int(Utils.string_input('1-Long Ships (0-9)', condition=r'[0-9]'))

                    # Test if ship amounts are valid.
                    count = settings['5_ships'] + settings['4_ships'] + settings['3_ships'] + settings['2_ships'] + settings['1_ships']
                    if count == 0:
                        Utils.box_string('You must have at least one ship!', print_string=True)
                    elif count > 26:
                        Utils.box_string('You have put in too many ships! (max 26)', print_string=True)
                    else:
                        break

            elif setting == 2:  # Special Abilities
                # Take abilities.
                settings['allow_moves'] = Utils.num_input('Ship Moving', 'Enable', 'Disable') == 0
                if settings['allow_moves']:
                    settings['allow_mines'] = Utils.num_input('Mines', 'Enable', 'Disable') == 0
                if settings['allow_mines']:
                    settings['mine_turns'] = int(Utils.string_input('Turns Between Mines'))

            elif setting == 3:  # Game Type
                # Take game type.
                settings['p_type'] = ['CPU', 'Player'][Utils.num_input('Game Type', 'CPU', 'Player')]

            # Print updated settings.
            Utils.print_settings(settings)

            if setting == 4:  # Exit
                break

    return BattleshipGame(settings)


if __name__ == '__main__':
    Utils.box_string('Welcome to Battleship!', print_string=True)
    gamemode = Utils.num_input('Which gamemode do you want to play?', 'Normal', 'Advanced')
    bs = create_game(gamemode)
    bs.start_game()

# TODO: SWITCH %-FORMATTING TO STRING.FORMAT
