
# To[e]-Ta[c]-Ti[c]

import sys
import random

import numpy as np


def init_table(table=None):
    return [' ' for i in range(9)]


def mark(table, index, sign):
    if table[index] != ' ':
        return -1
    table[index] = sign
    return 0


def get_choosable_cells(table):
    return [1 if table[i] == ' ' else 0 for i in range(9)]


def judge(table):
    first_list = [0, 3, 6, 0, 1, 2, 0, 2]
    second_list = [1, 4, 7, 3, 4, 5, 4, 4]
    third_list = [2, 5, 8, 6, 7, 8, 8, 6]

    for first, second, third in zip(first_list, second_list, third_list):
        if table[first] != ' ' \
        and table[first] == table[second] \
        and table[first] == table[third]:
            return table[first]  # return loser's sign

    choosable_cells = get_choosable_cells(table)
    if sum(choosable_cells) == 0:
        return 1  # draw

    return 0  # continue


def print_table(table):
    for i in range(3):
        print('|', end='')
        for j in range(3):
            print(table[i*3+j], end='')
            print('|', end='')
        print('')
    print('')


def get_choosable_indecies(table):
    choosable_cells = []
    for i in range(9):
        if table[i] == ' ':
            choosable_cells.append(i)
    return choosable_cells


class ToeTacTic:
    def __init__(self):
        self.table = None
        self.player1sign = 'O'
        self.player2sign = 'X'
        self.turn = 1

    def reset(self):
        self.table = init_table(self.table)
        return self.table

    def render(self):
        print_table(self.table)

    def step(self, action):
        sign = self.player1sign if self.turn > 0 else self.player2sign

        if mark(self.table, action, sign) < 0:
            return None, None, False, []

        self.turn *= -1

        result = judge(self.table)
        if result == sign:
            return None, -1, True, []
        elif result == 1:
            return None, 0, True, []
        elif result == 0:
            return self.table, 0, False, []
        else:
            return None, 1, True, []


def get_deaths(table, my_sign):
    first_list = [0, 3, 6, 0, 1, 2, 0, 2]
    second_list = [1, 4, 7, 3, 4, 5, 4, 4]
    third_list = [2, 5, 8, 6, 7, 8, 8, 6]

    deaths = []
    for first, second, third in zip(first_list, second_list, third_list):
        if table[first] == my_sign and table[second] == my_sign and table[third] == ' ':
            deaths.append(third)
            continue
        if table[first] == my_sign and table[second] == ' ' and table[third] == my_sign:
            deaths.append(second)
            continue
        if table[first] == ' ' and table[second] == my_sign and table[third] == my_sign:
            deaths.append(first)
            continue

    return deaths


def get_dangers(table, my_sign):
    first_list = [0, 3, 6, 0, 1, 2, 0, 2]
    second_list = [1, 4, 7, 3, 4, 5, 4, 4]
    third_list = [2, 5, 8, 6, 7, 8, 8, 6]

    dangers = []
    for first, second, third in zip(first_list, second_list, third_list):
        if table[first] == my_sign and table[second] == ' ' and table[third] == ' ':
            dangers.append(second)
            dangers.append(third)
            continue
        if table[first] == ' ' and table[second] == my_sign and table[third] == ' ':
            dangers.append(first)
            dangers.append(third)
            continue
        if table[first] == ' ' and table[second] == ' ' and table[third] == my_sign:
            dangers.append(first)
            dangers.append(second)
            continue

    return dangers


class NPC:
    def __init__(self):
        pass
    def act(self, table, npc_sign):
        pass


class LowLevelNPC(NPC):
    def act(self, table, npc_sign):
        choosable_indecies = get_choosable_indecies(table)
        return random.choice(choosable_indecies)


class MiddleLevelNPC(NPC):
    def act(self, table, npc_sign):
        choosable_indecies = set(get_choosable_indecies(table))
        deaths = set(get_deaths(table, npc_sign))
        dangers = set(get_dangers(table, npc_sign)) - deaths
        safety = choosable_indecies - deaths - dangers

        if len(safety) > 0:
            return random.choice(list(safety))
        if len(dangers) > 0:
            return random.choice(list(dangers))
        return random.choice(list(deaths))


class HighLevelNPC(NPC):
    def act(self, table, npc_sign):
        choosable_indecies = set(get_choosable_indecies(table))
        if len(choosable_indecies) == 9:
            return 4
        elif len(choosable_indecies) == 8:
            if 4 in choosable_indecies:
                return 4
            else:
                return 0
        else:
            deaths = set(get_deaths(table, npc_sign))
            dangers = set(get_dangers(table, npc_sign)) - deaths
            safety = choosable_indecies - deaths - dangers

            if len(safety) > 0:
                return random.choice(list(safety))
            if len(dangers) > 0:
                return random.choice(list(dangers))
            return random.choice(list(deaths))


class ToeTacTicEnvironment(ToeTacTic):
    def __init__(self):
        self.table = None
        self.player_sign = 'O'
        self.npc_sign = 'X'
        self.npc = MiddleLevelNPC()

    def reset(self):
        self.table = init_table(self.table)

        if random.random() < 0.5:
            npc_action = self.npc.act(self.table, self.npc_sign)
            mark(self.table, npc_action, self.npc_sign)

        return self.table

    def step(self, action):
        if mark(self.table, action, self.player_sign) < 0:
            return None, None, False, []

        result = judge(self.table)
        if result == self.player_sign:
            return None, -1, True, []
        elif result == 1:
            return None, 0, True, []

        npc_action = self.npc.act(self.table, self.npc_sign)
        mark(self.table, npc_action, self.npc_sign)

        result = judge(self.table)
        if result == self.npc_sign:
            return None, 1, True, []
        elif result == 1:
            return None, 0, True, []
        elif result == 0:
            return self.table, 0, False, []


def play():
    env = ToeTacTicEnvironment()
    env.reset()
    env.render()

    done = False
    while not done:
        action = int(input('Player )) '))
        if action < 0 or action > 8:
            continue
        _, reward, done, _ = env.step(action)
        env.render()

    if reward > 0:
        print('Victory!')
    elif reward < 0:
        print('Defeat...')
    else:
        print('Draw')


class ToeTacTicPlayground(ToeTacTic):
    def __init__(self, level=1, turnable=True, post=False, visualize=True):
        self.table = None
        self.player_sign = 'O'
        self.npc_sign = 'X'

        if level == 0:
            self.npc = LowLevelNPC()
        elif level == 1:
            self.npc = MiddleLevelNPC()
        else:
            self.npc = HighLevelNPC()

        self.turnable = turnable
        self.post = post
        self.visualize = visualize

    def reset(self):
        self.table = init_table(self.table)

        if self.post or self.turnable and random.random() < 0.5:
            npc_action = self.npc.act(self.table, self.npc_sign)
            mark(self.table, npc_action, self.npc_sign)
            if self.visualize:
                print('NPC ))', npc_action)
                self.render()

        return self.table

    def step(self, action):
        if mark(self.table, action, self.player_sign) < 0:
            return None, None, False, []

        if self.visualize:
            self.render()

        result = judge(self.table)
        if result == self.player_sign:
            return None, -1, True, []
        elif result == 1:
            return None, 0, True, []

        npc_action = self.npc.act(self.table, self.npc_sign)
        mark(self.table, npc_action, self.npc_sign)

        if self.visualize:
            print('NPC ))', npc_action)
            self.render()

        result = judge(self.table)
        if result == self.npc_sign:
            return None, 1, True, []
        elif result == 1:
            return None, 0, True, []
        elif result == 0:
            return self.table, 0, False, []

    def play(self):
        self.reset()

        done = False
        while not done:
            action = int(input('Player )) '))
            if action < 0 or action > 8:
                continue
            _, reward, done, _ = self.step(action)

        if reward > 0:
            print('Victory!')
        elif reward < 0:
            print('Defeat...')
        else:
            print('Draw')



if __name__ == '__main__':
    # play()
    level = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    playground = ToeTacTicPlayground(level)
    playground.play()
