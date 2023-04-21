import sys


nums = {0: ':zero:', 1: ':one:', 2: ':two:', 3: ':three:', 4: ':four:', 5: ':five:', 6: ':six:', 7: ':seven:', 8: ':eight:', 9: ':nine:'}


def within(num, x, y):
    return 0 <= x < num and 0 <= y < num


class checkers_Board:
    def __init__(self, size=10, ir=2, v=':black_large_square:', f=':white_circle:', t1=':blue_circle:', t2=':green_circle:', t1k=':blue_square:', t2k=':green_square:'):
        self.nem = {1: 2, 2: 1}
        self.tot = {1: (t1, t1k), 2: (t2, t2k)}
        self.d = {1: 1, 2: -1}
        self.promr = {1: 9, 2: 0}
        self.kings = {1: t1k, 2: t2k}
        self.tkings = {t1: t1k, t2: t2k}
        self.pawns = {t1k: t1, t2k: t2}
        self.board = []
        self.s, self.v, self.f, self.p = size, v, f, 1
        self.is_leap = False
        for i in range(size):
            self.board.append([])
            c = t1 if i < ir else t2 if i > size - ir - 1 else f
            for j in range(size):
                self.board[-1].append(v if (i + j) % 2 else c)
        # self.board[1][1] = t1
        # self.board[2][2] = t2
        # self.board[4][4] = t2


    def __repr__(self):
        rows = []
        for i in range(self.s):
            rows.append(f'{nums[i]}' + ''.join([self[j, i] for j in range(self.s)]) + '')
        rows.append(self.v + ''.join([nums[i] for i in range(self.s)]))
        return 'доска ниже:\n' + '\n'.join(rows[::-1])

    def _repr(self):
        return ''.join(''.join(i) for i in self.board)

    def __set__(self):
        return set([''.join(''.join(i) for i in self.board)])

    def __getitem__(self, key):
        if isinstance(key, int):
            key = key % 10, key // 10
        return self.board[key[1]][key[0]]

    def __setitem__(self, key, v):
        self.board[key[1]][key[0]] = v

    def move(self, sx, sy, ex, ey):
        if not all(list(map(lambda x: 0 <= x < self.s, [sx, sy, ex, ey]))):
            return f'координаты не могут быть меньше 0 или выше {self.s}'
        st, et = self[sx, sy], self[ex, ey]
        if st not in self.tot[self.p]:
            return 'На месте начальной координаты нет вашего юнита'
        if et in self.tot[self.p]:
            print(et, self.tot[self.p], et in self.tot[self.p])
            return 'вы не можете направить туда ваш юнит'
        if abs(sx - ex) != 1 and abs(sx - ex) != 1:
            return 'клетки не рядом'
        if ey - sy != self.d[self.p] and st.isnumeric():
            return 'клетки не рядом'
        if et in self.tot[self.nem[self.p]]:
            if not (0 < 2 * ex - sx < self.s and 0 < 2 * ey - sy < self.s):
                return f'координаты не могут быть меньше 0 или выше {self.s} ()'
            if self[2 * ex - sx, 2 * ey - sy] != self.f:
                return 'нельзя перепрыгивать на другие фигуры'
            self[sx, sy] = self.f
            self[ex, ey] = self.f
            self[2 * ex - sx, 2 * ey - sy] = st
            if 2 * ey - sy == self.promr[self.p]:
                self[2 * ex - sx, 2 * ey - sy] = self.kings[self.p]
            print(self)
            self.is_leap = True
            n1, n2, n3, n4, n5, n6 = [
                self[ex, ey + 2 * self.d[self.p]] if within(self.s, ex, ey + 2 * self.d[self.p]) else None,
                self[sx, ey + 3 * self.d[self.p]] if within(self.s, sx, ey + 3 * self.d[self.p]) else None,
                self[3 * ex - 2 * sx, ey + 2 * self.d[self.p]] if within(self.s, 3 * ex - 2 * sx, ey + 2 * self.d[self.p]) else None,
                self[4 * ex - 3 * sx, ey + 3 * self.d[self.p]] if within(self.s, 4 * ex - 3 * sx, ey + 3 * self.d[self.p]) else None,
                self[3 * ex - 2 * sx, ey] if within(self.s, 3 * ex - 2 * sx, ey) and self[ex, ey] in self.kings.values() else None,
                self[4 * ex - 3 * sx, sy] if within(self.s, 4 * ex - 3 * sx, sy) and self[ex, ey] in self.kings.values() else None,
            ]
            a = list(map(lambda x: x[0] in self.tot[self.nem[self.p]] and x[1] == self.f, [[n1, n2], [n3, n4], [n5, n6]]))
            if not any(a):
                self.is_leap = False
            return 'захват шашки прошёл успешно'
        elif not self.is_leap:
            self[sx, sy] = self.f
            self[ex, ey] = st
            if ey == self.promr[self.p]:
                self[ex, ey] = self.kings[self.p]
            print(self)
            return 'движение выполнено'
        else:
            return 'вы не можете передригаться на 1 клетку после препрыгивания'


    # def move(self, channel):
    #     self.is_leap = False
    #     try:
    #         sx, sy, ex, ey = map(
    #             int, input('Введите четыре натуральных числа через запятую без пробелов: ').split(',')
    #         )
    #     except BaseException as be:
    #         print('Нужно четыре натуральных числа')
    #         return 0
    #     mt = self.movepiece(sx, sy, ex, ey, self.is_leap)
    #     print('mt', mt, self.is_win())
    #     if mt == -4:
    #         channel.send('нельзя перепрыгивать на другие фигуры')
    #     elif mt == -3:
    #         channel.send(f'координаты не могут быть меньше 0 или выше {self.s}')
    #     elif mt == -2:
    #         channel.send('На месте начальной координаты нет вашего юнита')
    #     elif mt == -1:
    #         channel.send('вы не можете направить туда ваш юнит')
    #     elif mt == 1:
    #         channel.send('движение выполнено')
    #     elif mt == 3:
    #         channel.send('вы не можете передригаться на 1 клетку после препрыгивания')
    #     elif mt == 0:
    #         channel.send('клетки не рядом')
    #     else:
    #         self.is_leap = True
    #         n1, n2, n3, n4, n5, n6 = [
    #             self[ex, ey + 2 * self.d[self.p]] if within(self.s, ex, ey + 2 * self.d[self.p]) else None,
    #             self[sx, ey + 3 * self.d[self.p]] if within(self.s, sx, ey + 3 * self.d[self.p]) else None,
    #             self[3 * ex - 2 * sx, ey + 2 * self.d[self.p]] if within(self.s, 3 * ex - 2 * sx, ey + 2 * self.d[self.p]) else None,
    #             self[4 * ex - 3 * sx, ey + 3 * self.d[self.p]] if within(self.s, 4 * ex - 3 * sx, ey + 3 * self.d[self.p]) else None,
    #             self[3 * ex - 2 * sx, ey] if within(self.s, 3 * ex - 2 * sx, ey) and self[ex, ey] in self.kings.values() else None,
    #             self[4 * ex - 3 * sx, sy] if within(self.s, 4 * ex - 3 * sx, sy) and self[ex, ey] in self.kings.values() else None,
    #         ]
    #         a = list(map(lambda x: x[0] in self.tot[self.nem[self.p]] and x[1] == self.f, [[n1, n2], [n3, n4], [n5, n6]]))
    #         if not any(a):
    #             self.is_leap = False
    #     if self.is_win():
    #         channel.send('you won!')
    #         return 69
    #     self.p = self.nem[self.p]
    #     channel.send(f'Ход игрока №{self.p}')


    def is_win(self):
        s = set(self._repr())
        return not all(list(map(lambda x: any(list(map(lambda y: y in s, x))), self.tot.values())))
        
# a = checkers_Board()
# print(a)
# while not a.is_win():
#     a.move()