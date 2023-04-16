import sys


kings = {'1': 'k', '2': 'q'}


def within(num, x, y):
    return 0 < x < num and 0 < y < num


class checkers_Board:
    def __init__(self, size=10, ir=3, v=' ', f='.', t1='1', t2='2', t1k='k', t2k='q'):
        self.nem = {1: 2, 2: 1}
        self.tot = {1: [t1, t1k], 2: [t2, t2k]}
        self.d = {1: -1, 2: 1}
        self.promr = {1: 9, 2: 0}
        self.board = []
        self.s, self.v, self.f, self.p = size, v, f, 1
        for i in range(size):
            self.board.append([])
            c = t1 if i < ir else t2 if i > size - ir - 1 else f
            for j in range(size):
                self.board[-1].append(v if (i + j) % 2 else c)


    def __repr__(self):
        rows = []
        for i in range(self.s):
            rows.append('___' * self.s)
            rows.append('  |' + '|'.join(['  ' if self[j, i] == self.v else 'le' if self[j, i] == self.f else f'n{self[j, i]}' for j in range(self.s)]) + '|')
            rows.append(f'{i} |' + '|'.join(['  ' if self[j, i] == self.v else 'ti' if self[j, i] == self.f else 'pw' if self[j, i].isnumeric() else 'ki' for j in range(self.s)]) + '|')
        rows.append('--' + '---' * self.s)
        rows.append('  ' + '  '.join([str(i) for i in range(self.s)]))
        rows.append('--' + '---' * self.s)
        return '\n'.join(rows[::-1])

    def __set__(self):
        return set([''.join(''.join(i) for i in self.board)])

    def __getitem__(self, key):
        if isinstance(key, int):
            key = key % 10, key // 10
        return self.board[key[1]][key[0]]

    def __setitem__(self, key, v):
        self.board[key[1]][key[0]] = v

    def movepiece(self, sx, sy, ex, ey, is_leap):
        if not all(list(map(lambda x: 0 < x < self.s, [sx, sy, ex, ey]))):
            return -3
        st, et = self[sx, sy], self[ex, ey]
        if st not in self.tot[self.p]:
            print(st, type(st))
            return -2
        if et in self.tot[self.p]:
            return -1
        if abs(sx - ex) != 1 and abs(sx - ex) != 1:
            return 0
        if ey - sy != self.d[self.p] and not st.isnumeric():
            return 0
        if et in self.tot[self.nem[self.p]]:
            if not (0 < 2 * ex - sx < self.s and 0 < 2 * ey - sy < self.s):
                return -3
            if self[2 * ex - sx, 2 * ey - sy] != self.f:
                return -4
            self[sx, sy] = self.f
            self[ex, ey] = self.f
            self[2 * ex - sx, 2 * ey - sy] = st
            if 2 * ey - sy == self.promr[self.p]:
                self[2 * ex - sx, 2 * ey - sy] = kings[self.p]
            print(self)
            return 2
        elif not is_leap:
            self[sx, sy] = self.f
            self[ex, ey] = st
            if ey == self.promr[self.p]:
                self[ex, ey] = kings[self.p]
            print(self)
            return 1
        else:
            return 3


    def move(self):
        is_leap = False
        while True:
            try:
                sx, sy, ex, ey = map(
                    int, input('Введите четыре натуральных числа через запятую без пробелов: ').split(',')
                )
            except BaseException as be:
                print('Нужно четыре натуральных числа')
                continue
            mt = self.movepiece(sx, sy, ex, ey, is_leap)
            if mt == -4:
                print('нельзя перепрыгивать на другие фигуры')
            elif mt == -3:
                print(f'координаты не могут быть меньше 0 или выше {self.s}')
            elif mt == -2:
                print('На месте начальной координаты нет вашего юнита')
            elif mt == -1:
                print('вы не можете направить туда ваш юнит')
            elif mt == 1:
                print('отлично')
                break
            elif mt == 3:
                print('вы не можете передригаться на 1 клетку после препрыгивания')
            elif mt == 0:
                print('клетки не рядом')
            elif self.is_win():
                print(f'{self.p} wins')
                sys.exit()
            else:
                is_leap = True
                n1, n2, n3, n4, n5, n6 = [
                    self[ex, ey + 2 * self.d[self.p]] if within(self.s, ex, ey + 2 * self.d[self.p]) else None,
                    self[sx, ey + 3 * self.d[self.p]] if within(self.s, sx, ey + 3 * self.d[self.p]) else None,
                    self[3 * ex - 2 * sx, ey + 2 * self.d[self.p]] if within(self.s, 3 * ex - 2 * sx, ey + 2 * self.d[self.p]) else None,
                    self[4 * ex - 3 * sx, ey + 3 * self.d[self.p]] if within(self.s, 4 * ex - 3 * sx, ey + 3 * self.d[self.p]) else None,
                    self[3 * ex - 2 * sx, ey] if within(self.s, 3 * ex - 2 * sx, ey) and self[ex, ey] in kings.values() else None,
                    self[4 * ex - 3 * sx, sy] if within(self.s, 4 * ex - 3 * sx, sy) and self[ex, ey] in kings.values() else None,
                ]
                a = list(map(lambda x: x[0] in self.tot[self.nem[self.p]] and x[1] == self.f, [[n1, n2], [n3, n4], [n5, n6]]))
                if not any(a):
                    is_leap = False
                    break
        self.p = self.nem[self.p]
        print(f'Ход игрока №{self.p}')


    def is_win(self):
        return not any(list(map(lambda x: set(x) not in set(self), self.tot.values())))
        
a = checkers_Board()
while not a.is_win():
    a.move()
