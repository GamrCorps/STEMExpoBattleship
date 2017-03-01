# Notes:
#   [row][column]
#   Ships: numeric  [5long][4long][3long][2long][1long]
import re


class Utils(object):
    @staticmethod
    def box_string(string, min_width=-1, print_string=False):
        split_string = string.split('\n')
        height = len(split_string)
        length = max(min_width, *[len(x) for x in split_string])
        result = '+' + '-' * (length + 2) + '+\n'
        for i in range(height):
            result += '| %s |\n' % split_string[i].center(length)
        result += '+' + '-' * (length + 2) + '+'
        if print_string:
            print(result)
        return result

    @staticmethod
    def num_input(question, *choices):
        error = ''
        while True:
            print(Utils.box_string((error + '\n' + question).strip()))
            for i in range(len(choices)):
                print('%d: %s' % (i, choices[i]))
            response = input('Response: ')
            if re.fullmatch(r'\d+', response.strip()):
                to_int = int(response.strip())
                if to_int < len(choices):
                    return to_int
                else:
                    error = 'ERROR: Invalid input! Input integer is not one of the avaliable choices! Please try again.'
                continue
            else:
                for i in range(len(choices)):
                    if response.strip().lower() == choices[i].strip().lower():
                        return i
                error = 'ERROR: Invalid input! Input string is not one of the avaliable choices! Please try again.'
                continue

    @staticmethod
    def string_input(question):
        print(Utils.box_string(question.strip()))
        return input()

    @staticmethod
    def print_settings(settings):
        Utils.box_string('Current Settings', print_string=True)
        print('Grid Size:')
        print('\tWidth: %d' % settings['width'])
        print('\tHeight: %d' % settings['height'])


class BattleshipGame(object):
    def __init__(self, height, width, p_type, gm):
        self.height = height
        self.width = width
        self.p1_grid = [[0] * width] * height
        self.p2_grid = [[0] * width] * height
        self.p_type = p_type
        self.gm = gm

    def print_board(self, board):
        result = ''
        for i in range(self.height):
            result += ' '.join([str(x) for x in board[i]]) + '\n'
        print(Utils.box_string(result.strip()))


normal_mode_preset = {'height': 10, 'width': 10, '5_ships': 1, '4_ships': 1, '3_ships': 2, '2_ships': 1, '1_ships': 0,
                      'allow_mines': False, 'allow_moves': False, 'allow_scans': False, 'scan_turns': None}
advanced_mode_preset = {'height': 15, 'width': 15, '5_ships': 2, '4_ships': 2, '3_ships': 2, '2_ships': 1, '1_ships': 0,
                        'allow_mines': True, 'allow_moves': True, 'allow_scans': True, 'scan_turns': 5}


def create_game(gm):
    if gm == 0:
        Utils.box_string('Normal Mode', print_string=True)
        settings = normal_mode_preset
    else:
        Utils.box_string('Advanced Mode', print_string=True)
        settings = advanced_mode_preset
    Utils.box_string('Current Settings', print_string=True)
    if Utils.num_input('Would you like to change the settings?', 'Yes', 'No') == 0:
        while True:
            setting = Utils.num_input('Settings', 'Grid Size', 'Ship Amount', 'Special Abilities', 'Exit')
            if setting == 0:
                settings['width'] = int(Utils.string_input('Grid Width'))
                settings['height'] = int(Utils.string_input('Grid Height'))
            elif setting == 1:
                settings['5_ships'] = int(Utils.string_input('5-Length Ships'))
                settings['4_ships'] = int(Utils.string_input('4-Length Ships'))
                settings['3_ships'] = int(Utils.string_input('3-Length Ships'))
                settings['2_ships'] = int(Utils.string_input('2-Length Ships'))
                settings['1_ships'] = int(Utils.string_input('1-Length Ships'))
            elif setting == 2:
                settings['allow_moves'] = Utils.num_input('Ship Moving', 'Enable', 'Disable') == 0
                if settings['allow_moves']:
                    settings['allow_mines'] = Utils.num_input('Mines', 'Enable', 'Disable') == 0
                settings['allow_scans'] = Utils.num_input('Scanning', 'Enable', 'Disable') == 0
                if settings['allow_scans']:
                    settings['scan_turns'] = int(Utils.string_input('Turns Between Scans'))
            Utils.box_string('Current Settings', print_string=True)
            if setting == 3:
                break
                # bs = BattleshipGame()


if __name__ == '__main__':
    # bt = BattleshipGame(13, 17, 'CPU')
    # bt.print_board(bt.p1_grid)
    # print(Utils.box_string('Player 1\'s Turn', min_width=bt.width*2-1))
    # print(Utils.num_input('Which gamemode would you like to play?', 'Versus Computer', 'Versus Player', 'Extreme Mode'

    # Menu
    Utils.box_string('Welcome to Battleship!', print_string=True)
    gamemode = Utils.num_input('Which gamemode do you want to play?', 'Normal', 'Advanced')
    bs = create_game(gamemode)
