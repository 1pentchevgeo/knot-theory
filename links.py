import ast
from copy import deepcopy


class Link:

    def __init__(self, gc, writhe):
        self.gc = gc
        self.writhe = writhe

    def __repr__(self):
        return "Link(gc={}, writhe={})".format(self.gc, self.writhe)

    @classmethod
    def from_egc(cls, egc):
        concat = egc[0] if len(egc) == 1 else egc[0] + egc[1]
        order = list(dict.fromkeys([abs(i) for i in concat]))
        writhe = []
        for i in sorted(order):
            matches = [j for j, k in enumerate(concat) if abs(k) == i]
            writhe += [1] if concat[matches[1]] > 0 else [-1]
        for i in order:
            matches = [j for j, k in enumerate(concat) if abs(k) == i]
            concat[matches[1]] = -1 * concat[matches[0]]
        gc = [concat] if len(egc) == 1 else [concat[:len(egc[0])], concat[len(egc[0]):]]
        return cls(gc, writhe)

    def relabel(self):
        if len(self.gc) == 1:
            big = max(self.gc[0]) if len(self.gc[0]) > 0 else 1
            self.gc[0] = [i * big for i in self.gc[0]]
            order = list(dict.fromkeys([abs(i) for i in self.gc[0]]))
            for i in range(len(order)):
                self.gc[0][self.gc[0].index(order[i])] = i + 1
                self.gc[0][self.gc[0].index(-1 * order[i])] = -1 * (i + 1)
        elif len(self.gc) == 2:
            concat = self.gc[0] + self.gc[1]
            big = max(concat)
            concat = [i * big for i in concat]
            order = list(dict.fromkeys([abs(i) for i in concat]))
            for i in range(len(order)):
                concat[concat.index(order[i])] = i + 1
                concat[concat.index(-1 * order[i])] = -1 * (i + 1)
            self.gc[0], self.gc[1] = concat[:len(self.gc[0])], concat[len(self.gc[0]):]
        self.writhe = [self.writhe[i] for i in [order.index(i) for i in sorted(order)]]

    def r1(self):
        for j in range(len(self.gc)):
            for i in range(len(self.gc[j])):
                if self.gc[j][i] == -1 * self.gc[j][i - 1]:
                    self.writhe[abs(self.gc[j][i]) - 1] = 0
                    self.gc[j][i] = self.gc[j][i - 1] = 0
            self.gc[j] = [i for i in self.gc[j] if i != 0]
            self.writhe = [i for i in self.writhe if i != 0]
        self.relabel()

    def r2(self):
        for k in range(len(self.gc)):
            for i in range(len(self.gc[k])):
                if self.gc[k][i] * self.gc[k][i - 1] > 0:
                    for j in range(len(self.gc[k])):
                        if ((self.gc[k][j] == -1 * self.gc[k][i]
                            and self.gc[k][j - 1] == -1 * self.gc[k][i - 1])
                                or (self.gc[k][j - 1] == -1 * self.gc[k][i]
                                    and self.gc[k][j] == -1 * self.gc[k][i - 1])):
                            self.writhe[abs(self.gc[k][i]) - 1] = self.writhe[abs(self.gc[k][i-1]) - 1] = 0
                            self.gc[k][i] = self.gc[k][i - 1] = self.gc[k][j] = self.gc[k][j - 1] = 0
            self.gc[k] = [i for i in self.gc[k] if i != 0]
            self.writhe = [i for i in self.writhe if i != 0]
        if len(self.gc) == 2:
            for i in range(len(self.gc[0])):
                if self.gc[0][i] * self.gc[0][i - 1] > 0:
                    for j in range(len(self.gc[1])):
                        if ((self.gc[1][j] == -1 * self.gc[0][i]
                             and self.gc[1][j - 1] == -1 * self.gc[0][i - 1])
                                or (self.gc[1][j - 1] == -1 * self.gc[0][i]
                                    and self.gc[1][j] == -1 * self.gc[0][i - 1])):
                            self.writhe[abs(self.gc[0][i]) - 1] = self.writhe[abs(self.gc[0][i-1]) - 1] = 0
                            self.gc[0][i] = self.gc[0][i - 1] = self.gc[1][j] = self.gc[1][j - 1] = 0
            self.gc[0] = [i for i in self.gc[0] if i != 0]
            self.gc[1] = [i for i in self.gc[1] if i != 0]
            self.writhe = [i for i in self.writhe if i != 0]
        self.relabel()

    def simplify(self):
        a, b = self.gc[:], self.writhe[:]
        self.r1()
        self.r2()
        while (a, b) != (self.gc, self.writhe):
            a, b = self.gc[:], self.writhe[:]
            self.r1()
            self.r2()

    def remove(self, crossing):
        if len(self.gc) == 1:
            a, b = self.gc[0].index(crossing), self.gc[0].index(-1 * crossing)
            if a > b:
                a, b = b, a
            self.gc = [self.gc[0][:a] + self.gc[0][(b + 1):], self.gc[0][(a + 1):b]]
        elif len(self.gc) == 2:
            a, b = [abs(i) for i in self.gc[0]].index(crossing),  [abs(i) for i in self.gc[1]].index(crossing)
            self.gc = [self.gc[0][:a] + self.gc[1][(b + 1):] + self.gc[1][:b] + self.gc[0][(a + 1):]]
            # What if the crossing you are trying to remove occurs entirely in the first component?
        del self.writhe[crossing - 1]
        self.relabel()

    deg = 10

    @classmethod
    def set_deg(cls, x):
        cls.deg = x

    def conway(self):
        def c(gc, writhe):
            link = Link(gc, writhe)
            link.simplify()
            if len(link.gc) == 1 and len(link.gc[0]) == 6:
                return [1, 0, 1] + [0] * (link.deg - 2)
            elif len(link.gc) == 2 and len(link.gc[0] + link.gc[1]) == 4:
                return [0, link.writhe[0]] + [0] * (link.deg - 1)
            elif len(link.gc[0]) == 0:
                return [1] + [0] * link.deg
            else:
                opp = deepcopy(link)
                if len(opp.gc) == 1:
                    a = opp.gc[0].index(1)
                    b = opp.gc[0].index(-1)
                    opp.gc[0][a], opp.gc[0][b] = opp.gc[0][b], opp.gc[0][a]
                elif len(opp.gc) == 2:
                    concat = opp.gc[0] + opp.gc[1]
                    a = concat.index(1)
                    b = concat.index(-1)
                    concat[a], concat[b] = concat[b], concat[a]
                    opp.gc[0], opp.gc[1] = concat[:len(opp.gc[0])], concat[len(opp.gc[0]):]
                opp.writhe[0] *= -1
                opp.simplify()
                zero = deepcopy(link)
                zero.remove(1)
                zero.simplify()
                if link.writhe[0] == 1:
                    return [i + j for i, j in zip(
                        c(opp.gc, opp.writhe),
                        [0] + c(zero.gc, zero.writhe)[:-1]
                    )]
                elif link.writhe[0] == -1:
                    return [i - j for i, j in zip(
                        c(opp.gc, opp.writhe),
                        [0] + c(zero.gc, zero.writhe)[:-1]
                    )]
        return c(self.gc, self.writhe)
