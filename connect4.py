import numpy as np


def get_matrix_diagonal(mas):
    a = np.array(
        mas)
    diags = [a[::-1, :].diagonal(i) for i in range(-a.shape[0] + 1, a.shape[1])]
    diags.extend(a.diagonal(i) for i in range(a.shape[1] - 1, -a.shape[0], -1))
    return [list(n.tolist()) for n in diags]


def rotate_matrix(mas):
    a = np.array(mas)
    b = list(np.rot90(a))
    return [list(_) for _ in b]


def contains(small, big):
    a, b = ''.join(small), ''.join(big)
    if a in b:
        return True


def q(x):
    return x * 4


class Board:
    def __init__(self, rows=6, columns=7, filler=":blue_square:", team1=":orange_circle:", team2=":green_circle:"):
        self.table = [["_" for i in range(columns)] for _ in range(rows)]
        self.view = {"t1": team1, "t2": team2, "_": filler}
        self.rows = rows
        self.columns = columns

    def board_view(self):
        res = ["".join([self.view[t] for t in row]) for row in self.table]
        return "\n".join(res)

    def is_empty(self, row, column):
        return self.table[row][column] == "_"

    def win_row(self, t='t1'):
        for i in self.table:
            print(i)
            if contains(q([t]), i):
                return True
        return False

    def win_column(self, t='t1'):
        mas = rotate_matrix(self.table)
        for i in mas:
            print(i)
            if contains(q([t]), i):
                return True
        return False

    def diagonal_win(self, t='t1'):
        mas = get_matrix_diagonal(self.table)
        mas = [i for i in mas if len(i) >= 4]
        for i in mas:
            print(i)
            if i == q([t]):
                return True
            else:
                if contains(q([t]), i):
                    return True
        return False

    def win(self, t='t1'):
        print('win?')
        a = self.win_row(t) or self.win_column(t) or self.diagonal_win(t)
        print(a)
        return a

    def t1win(self):
        return self.win('t1')

    def t2win(self):
        return self.win('t2')

    def find_empty(self, column):
        a = rotate_matrix(self.table)
        for i in list(range(self.rows))[::-1]:
            if self.is_empty(i, column):
                return i
        else:
            return -1

    def place(self, row, column, t):
        self.table[row][column] = t

    def move(self, column, t):
        cell = self.find_empty(column)
        if cell == -1:
            return
        self.place(cell, column, t)


class Game(Board):
    def __init__(self, rows=6, columns=7, filler=":blue_square:",
                 team1=":orange_circle:", team2=":green_circle:", p1="popusk1", p2="popusk2"):
        super().__init__(rows, columns, filler, team1, team2)
        self.player1 = p1
        self.player2 = p2
        self.players = {"t1": self.player1, "t2": self.player2}

    def draw(self):  # потом заменить имена на теги челов
        return f"""Connect4 by Popusk-bot

Popusk 1 : {self.player1}
Popusk 2 : {self.player2}

{self.board_view()}"""

    def on_win(self, t):
        return f"""Connect4 by Popusk-bot

Popusk 1 : {self.player1}
Popusk 2 : {self.player2}
! DRAW !
{self.board_view()}""" if t == 'draw' else f"""Connect4 by Popusk-bot

Popusk 1 : {self.player1}
Popusk 2 : {self.player2}
{self.players[t]} ! WON !
{self.board_view()}"""

    def move(self, column, t):
        super().move(column, t)
        if self.win(t):
            return self.on_win(t)
        elif self.view['_'] not in self.board_view():
            return self.on_win('draw')
        else:
            return self.board_view()
