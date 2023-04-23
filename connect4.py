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
    for i in range(len(big) - len(small) + 1):
        for j in range(len(small)):
            if big[i + j] != small[j]:
                break
        else:
            return True
    return False


class Board:
    def __init__(self, rows=6, columns=6, filler=":blue_square:", team1=":orange_circle:", team2=":green_circle:"):
        self.table = [["_" for i in range(columns)] for _ in range(rows)]
        self.view = {"t1": team1, "t2": team2, "_": filler}
        self.rows = rows
        self.columns = columns
        self.turn = "t1"

    def board_view(self):
        # print(*[[row for row in self.table for t in row]])
        for i in self.table:
            print(i)
        res = ["".join([self.view[t] for t in row]) for row in self.table]
        return "\n".join(res)

    def is_empty(self, row, column):
        return self.table[row][column] == "_"

    def row_check(self, t='t1'):
        t = self.view[t]
        for _ in range(len(self.table)):
            a1 = self.table[_].count(t)
            if a1 >= 4 and self.table[_][self.table[_].index(t):self.table[_].index(t) + 4] == [t, t, t, t]:
                return True
            elif a1 >= 4:
                b = self.table[_].index(t) + self.table[_][b + 1:].index(t)
                if self.table[_][b: min(b + 4, len(self.table[_]))] == [t, t, t, t]:
                    return True
        return False

    def column_check(self, t='t1'):
        t = self.view[t]
        mas = rotate_matrix(self.table)
        for _ in range(len(mas)):
            a1 = mas[_].count(t)
            if a1 >= 4 and mas[_][mas[_].index(t):mas[_].index(t) + 4] == [t, t, t, t]:
                return True
            elif a1 >= 4:
                b = mas[_].index(t)
                c = mas[_][b + 1:].index(t)
                b = b + c

                if mas[_][b: min(b + 4, len(mas[_]))] == [t, t, t, t]:
                    return True
        return False

    def diagonal_check(self, t='t1'):
        t = self.view[t]
        digs = get_matrix_diagonal(self.table)
        digs = [i for i in digs if i.count(t) >= 4]
        for i in digs:
            if [t, t, t, t] in i:
                return True

        return False

    def win_row(self, t='t1'):
        a = self.view[t]
        for i in self.table:
            if contains([t, t, t, t], i):
                return True
        return False

    def win_column(self, t='t1'):
        mas = rotate_matrix(self.table)
        a = self.view[t]
        for i in mas:
            if contains([t, t, t, t], i):
                return True
        return False

    def diagonal_win(self, t='t1'):
        a = self.view[t]
        mas = get_matrix_diagonal(self.table)
        mas = [i for i in mas if len(i) >= 4]
        for i in mas:
            if i == [t, t, t, t]:
                return True
            else:
                if contains(i, [t, t, t, t]):
                    return True
        return False

    def win(self, t='t1'):
        return self.win_row(t) or self.win_column(t) or self.diagonal_win(t)

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
        self.switch_turn()

    def filled_check(self):
        a = [self.find_empty(i) for i in range(self.columns)]
        return set(a) == {-1}

    def switch_turn(self):
        if self.turn == "t1":
            self.turn = "t2"
        else:
            self.turn = "t1"


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
        if t != "tt":
            return f"""Connect4 by Popusk-bot
    
Popusk 1 : {self.player1}
Popusk 2 : {self.player2}
{self.players[t]} ! WON !
{self.board_view()}"""
        else:
            return f"""Connect4 by Popusk-bot
Popusk 1 : {self.player1}
Popusk 2 : {self.player2}
!DRAW!
the field is full
{self.board_view()}"""

    def move(self, column, t):
        super().move(column, t)

        if self.win(t):
            self.on_win(t)

    def game_over(self):
        if self.t1win() or self.t2win() or self.filled_check():
            return True

    def on_game_over(self):
        if self.t1win():
            self.on_win("t1")
        elif self.t2win():
            self.on_win("t2")
        else:
            self.on_win("tt")

    def force_win(self, t="t1"):
        self.on_win(t)

    def edit_players(self, p1=None, p2=None):
        if p1:
            self.player1 = p1
        if p2:
            self.player2 = p2
        self.players = {"t1": self.player1, "t2": self.player2}


a = Game()

a.table = [["_" for i in range(a.columns)] for _ in range(a.rows)]
