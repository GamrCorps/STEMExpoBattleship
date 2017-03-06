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
                    error = 'ERROR: Invalid input! Input integer is not one of \
                        the avaliable choices! Please try again.'
                continue
            else:
                for i in range(len(choices)):
                    if response.strip().lower() == choices[i].strip().lower():
                        return i
                error = 'ERROR: Invalid input! Input string is not one of the \
                    avaliable choices! Please try again.'
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


class BattleshipGame(object):
    def __init__(self, settings):
        self.settings = settings
        self.height = settings['height']
        self.width = settings['width']
        self.p1_grid = [[0] * self.width] * self.height
        self.p2_grid = [[0] * self.width] * self.height
        self.p_type = settings['p_type']

    def print_board(self, board):
        result = ''
        for i in range(self.height):
            result += ' '.join([str(x) for x in board[i]]) + '\n'
        print(Utils.box_string(result.strip()))


normal_mode_preset = {'height': 10, 'width': 10, '5_ships': 1, '4_ships': 1,
                      '3_ships': 2, '2_ships': 1, '1_ships': 0,
                      'allow_mines': False, 'allow_moves': False,
                      'mine_turns': None, 'p_type': 'CPU'}
advanced_mode_preset = {'height': 15, 'width': 15, '5_ships': 2, '4_ships': 2,
                        '3_ships': 2, '2_ships': 1, '1_ships': 0
                        'allow_mines': True, 'allow_moves': True,
                        'mine_turns': 5, 'p_type': 'CPU'}


def create_game(gm):
    if gm == 0:
        Utils.box_string('Normal Mode', print_string=True)
        settings = normal_mode_preset
    else:
        Utils.box_string('Advanced Mode', print_string=True)
        settings = advanced_mode_preset
    Utils.print_settings(settings)
    if Utils.num_input('Would you like to change the settings?', 'No', 'Yes') == 1:
        while True:
            setting = Utils.num_input('Settings', 'Grid Size', 'Ship Amount', 'Special Abilities', 'Game Type', 'Exit')
            if setting == 0:
                settings['width'] = int(Utils.string_input('Grid Width'))
                settings['height'] = int(Utils.string_input('Grid Height'))
            elif setting == 1:
                settings['5_ships'] = int(Utils.string_input('5-Long Ships'))
                settings['4_ships'] = int(Utils.string_input('4-Long Ships'))
                settings['3_ships'] = int(Utils.string_input('3-Long Ships'))
                settings['2_ships'] = int(Utils.string_input('2-Long Ships'))
                settings['1_ships'] = int(Utils.string_input('1-Long Ships'))
            elif setting == 2:
                settings['allow_moves'] = Utils.num_input('Ship Moving', 'Enable', 'Disable') == 0
                if settings['allow_moves']:
                    settings['allow_mines'] = Utils.num_input('Mines', 'Enable', 'Disable') == 0
                if settings['allow_mines']:
                    settings['mine_turns'] = int(Utils.string_input('Turns Between Mines'))
            elif setting == 3:
                settings['p_type'] = ['CPU', 'Player'][Utils.num_input('Game Type', 'CPU', 'Player')]
            Utils.print_settings(settings)
            if setting == 4:
                break
    bs = BattleshipGame(settings)


if __name__ == '__main__':
    Utils.box_string('Welcome to Battleship!', print_string=True)
    gamemode = Utils.num_input('Which gamemode do you want to play?', 'Normal', 'Advanced')
    bs = create_game(gamemode)
