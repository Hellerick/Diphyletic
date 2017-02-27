import random


E, M, F = range(3)  # empty, males, females

moves = [
    [+1,  0],
    [ 0, +1],
    [-1,  0],
    [ 0, -1],
]


def main():
    colony = Colony()
    colony.random_fill([6, 6])
    while True:
        colony.show()
        colony.evolve()


class Colony:

    def __init__(self):
        self.map = []
        self.generation = 0

    def random_fill(self, size):
        colony_map = []
        for i in range(size[0]):
            line = [random.choice([E, M, F]) for _ in range(size[1])]
            colony_map += [line]
        self.map = colony_map

    def show(self):
        print('Generation', self.generation)
        for line in self.map:
            print(' '.join(' mf'[c] for c in line))
        print()

    def check_borders(self):
        while sum(self.map[0]) == 0:
            self.map = self.map[1:]
        while sum(self.map[-1]) == 0:
            self.map = self.map[:-1]
        while sum([l[0] for l in self.map]) == 0:
            self.map = [l[1:] for l in self.map]
        while sum([l[-1] for l in self.map]) == 0:
            self.map = [l[:-1] for l in self.map]
        self.map = [[0]+l+[0] for l in self.map]
        empty_line = [0] * len(self.map[0])
        self.map = [empty_line] + self.map + [empty_line]

    def neighbors(self, i, j):
        males = 0
        females = 0
        for m in moves:
            if self.map[i+m[0]][j+m[1]] == M:
                males += 1
            elif self.map[i+m[0]][j+m[1]] == F:
                females += 1
        return [males+females, males, females]

    def evolve(self):
        self.check_borders()
        self.generation += 1
        deathlist = []
        birthlist = []
        movelist = []
        for i in range(1, len(self.map)-1):
            for j in range(1, len(self.map[i])-1):
                neighbors = self.neighbors(i, j)
                if self.map[i][j] != 0 and neighbors[0] in [0,4]:
                    deathlist += [[i,j]]
                if (
                        self.map[i][j] == 0 and
                        neighbors[M] == 1 and
                        neighbors[F] == 1
                    ):
                    paircode = ''.join([str(self.map[i+m[0]][j+m[1]]) for m in moves])
                    paircode = [c for c in paircode if c != '0']
                    gender = int(paircode[0])
                    birthlist += [[i,j,gender]]
                if self.map[i][j] != 0 and neighbors[0] == 2:
                    moved = False
                    for m in moves:
                        if not moved:
                            new_neighbors = self.neighbors(i+m[0], j+m[1])
                            if new_neighbors == 1 and new_neighbors[3-self.map[i][j]] == 1:
                                movelist += [i,j,i+m[0],j+m[1]]
                                moved = True
        for b in birthlist:
            self.map[b[0]][b[1]] = b[2]
        for d in deathlist:
            self.map[d[0]][d[1]] = 0
        for m in movelist:
            self.map[m[2]][m[3]] = self.map[m[0]][m[1]]
            self.map[m[0]][m[1]] = 0

if __name__ == '__main__':
    main()
