#!/usr/bin/env python3
from battleship import *

if __name__ == '__main__':
    #print(Utils.grid_pos_input(15,15))
    advanced_mode_preset = {'height': 15, 'width': 15, '5_ships': 2, '4_ships': 2, '3_ships': 2, '2_ships': 1, '1_ships': 0, 
                        'allow_mines': True, 'allow_moves': True, 'mine_turns': 5, 'p_type': 'CPU'}
    print(Utils.box_string('test'))
    print(BattleshipGame(advanced_mode_preset).print_board(0))