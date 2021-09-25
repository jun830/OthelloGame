import numpy as np
from time import sleep
import random


def make_field(f_size):
    f = [[0] * f_size for _ in range(f_size)]
    field = np.pad(f, 1, "constant", constant_values=9)
    field[4, 5] = 1
    field[5, 4] = 1
    field[4, 4] = 2
    field[5, 5] = 2
    return field


class OthelloBoard:
    def __init__(self):
        self.field = make_field(8)
        self.turn_attack = 1
        self.turn_target = 2

    def count(self):
        black = np.sum(self.field == 1)
        white = np.sum(self.field == 2)
        empty = np.sum(self.field == 0)
        return black, white, empty

    def stone_check(self, x, y):
        stone_check_list = []
        if self.field[x, y] == 0:
            for i in range(3):
                for j in range(3):
                    if i == j == 2:
                        continue
                    check_x = x
                    check_y = y
                    direction = (i - 1, j - 1)
                    check_x += direction[0]
                    check_y += direction[1]
                    if self.field[check_x, check_y] == self.turn_target:
                        while True:
                            check_x += direction[0]
                            check_y += direction[1]
                            if self.field[check_x, check_y] == self.turn_target:
                                continue
                            elif self.field[check_x, check_y] == 9 or self.field[check_x, check_y] == 0:
                                break
                            else:
                                stone_check_list.append(direction)
        return stone_check_list

    def attack_check(self, put=False):
        attack_list = []
        for i in range(1, 9):
            for j in range(1, 9):
                if self.stone_check(i, j):
                    attack_list.append([i, j])

        if put:
            return attack_list

        if attack_list:
            if self.turn_attack == 1:
                print("あなたの番です。")
                return attack_list
            else:
                print("相手の番です。")
                return attack_list
        else:
            if self.turn_attack == 1:
                print("あなたの置ける場所がありません。")
            else:
                print("相手の置ける場所がありません。")
            self.turn_attack, self.turn_target = self.turn_target, self.turn_attack

    def put_stone(self, x, y):
        attack_list = self.attack_check(put=True)
        if [x, y] in attack_list:
            direction = self.stone_check(x, y)
            self.field[x, y] = self.turn_attack
            for d in direction:
                ax, ay = x, y
                while True:
                    ax += d[0]
                    ay += d[1]
                    if self.field[ax, ay] == self.turn_target:
                        self.field[ax, ay] = self.turn_attack
                        continue
                    else:
                        break
            self.turn_attack, self.turn_target = self.turn_target, self.turn_attack


def game(sleep_time=1):
    board = OthelloBoard()
    user, com, empty = board.count()
    print(board.field)
    while empty > 0:
        print("------------------------------")
        sleep(sleep_time)
        choices = board.attack_check()
        if not choices:
            continue
        sleep(sleep_time)
        if board.turn_attack == 1:
            print(choices)
            user_put = int(input("置く場所をindexで入れてね！:"))
            sleep(sleep_time)
            board.put_stone(choices[user_put][0], choices[user_put][1])
        else:
            com_put = random.choice(choices)
            print(f"AI:{com_put}")
            sleep(sleep_time)
            board.put_stone(com_put[0], com_put[1])
        user, com, empty = board.count()
        print(board.field)
        sleep(sleep_time)
        print("あなた:{} 相手:{} 残り:{}".format(user, com, empty))
        sleep(sleep_time)

        if user == 0:
            print("あなたの負けです")
            return 0
        elif com == 0:
            print("あなたの勝ちです")
            return 1
    else:
        print("石を置き終わりました")
        user, com, _ = board.count()
        if user > com:
            print("あなたの勝ちです")
            return 0
        elif user < com:
            print("あなたの負けです")
            return 1
        else:
            print("引き分けです")
            return -1


game()
