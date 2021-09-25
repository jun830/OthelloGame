import sys
import numpy as np
from time import sleep
import random
import tkinter as tk
from tkinter import messagebox


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
                    if i == j == 1:
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
            # self.turn_attack, self.turn_target = self.turn_target, self.turn_attack

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
            # self.turn_attack, self.turn_target = self.turn_target, self.turn_attack


"""
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
# game()
"""


def judgement(user, com):
    if user > com:
        messagebox.showinfo("COM", "あなたの勝ちです！！")
    elif user < com:
        messagebox.showinfo("COM", "あなたの負けです")
    else:
        messagebox.showinfo("COM", "引き分けです")
    root.destroy()
    sys.exit()


def click_btn(btn):
    global board
    select_x, select_y = map(int, list(btn.widget._name))
    user_put = [select_y + 1, select_x + 1]
    choices = board.attack_check()
    if user_put in choices:
        board.put_stone(user_put[0], user_put[1])
        field_update()
    else:
        messagebox.showinfo("COM", "そこには置けません")
        return
    (user, com, last) = board.count()
    label_tex = "USER:{} COM:{} LAST{}".format(user, com, last)
    info_label = tk.Label(root, text=label_tex, font=("ＭＳゴシック", "15", "bold"))
    info_label.place(x=25, y=25, width=400, height=50)

    if not com or not last:
        judgement(user, com)

    board.turn_attack, board.turn_target = board.turn_target, board.turn_attack

    end_flag = False

    while board.turn_attack == 2:
        choices = board.attack_check()
        if choices:
            com_put = random.choice(choices)
            messagebox.showinfo("COM", "{}{}に置きます".format(com_put[0], com_put[1]))
            board.put_stone(com_put[0], com_put[1])
            field_update()
        else:
            if end_flag:
                judgement(user, com)
            end_flag = True
            messagebox.showinfo("COM", "置けるところがありません")
            field_update()
        (user, com, last) = board.count()
        label_tex = "USER:{} COM:{} LAST{}".format(user, com, last)
        info_label = tk.Label(root, text=label_tex, font=("ＭＳゴシック", "15", "bold"))
        info_label.place(x=25, y=25, width=400, height=50)

        if not user or not last:
            judgement(user, com)

        board.turn_attack, board.turn_target = board.turn_target, board.turn_attack

        choices = board.attack_check()
        if not choices:
            if end_flag:
                judgement(user, com)
            end_flag = True
            messagebox.showinfo("COM", "あなたの置ける場所がありません")
            board.turn_attack, board.turn_target = board.turn_target, board.turn_attack


def field_update():
    global btns
    btns = []
    for x in range(8):
        for y in range(8):
            btn_place = str(x) + str(y)
            if board.field[y + 1][x + 1] == 1:
                btns.append(tk.Button(root, text="●", font=("ＭＳゴシック", "30"),
                                      fg="#001100", anchor="center", name=btn_place))
            elif board.field[y + 1][x + 1] == 2:
                btns.append(tk.Button(root, text="●", font=("ＭＳゴシック", "30"),
                                      fg="#FFDDFF", anchor="center", name=btn_place))
            else:
                btns.append(tk.Button(root, text="", name=btn_place))
            btns[x * 8 + y].place(x=x * 50 + 25, y=y * 50 + 100, width=50, height=50)
            btns[x * 8 + y].configure(bg="#00cc00")


board = OthelloBoard()
(user, com, last) = board.count()

root = tk.Tk()
root.configure(bg="#555555")
root.title("オセロゲーム")
root.geometry("450x500")

field_update()

label_tex = "USER:{} COM:{} LAST{}".format(user, com, last)
info_label = tk.Label(root, text=label_tex, font=("ＭＳゴシック", "15", "bold"))
info_label.place(x=25, y=25, width=400, height=50)

root.bind("<1>", click_btn)

root.mainloop()
