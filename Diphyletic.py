import random
import re


E, M, F = range(3)  # empty, males, females

rules = 2

if rules == 1:
    moves = [
        [+1,  0],
        [ 0, +1],
        [-1,  0],
        [ 0, -1],
    ]
elif rules == 2:
    moves = [
        [ 0, +1],
        [+1, +1],
        [+1,  0],
        [+1, -1],
        [ 0, -1],
        [-1, -1],
        [-1,  0],
        [-1, +1],
    ]


def main():
    colony = Colony()
    colony.random_fill([3, 3])

    colony.input_by_map('''
    mf
    mfm
    fmm
    ''')

    colony.input_by_map('''
    m m
    mff
    ''')

    # colony.enter('''
    #  m  fff  m   f
    # m m f   mm  f f
    #  m  ff   m  f f
    # m m   f  m  f f
    #  m  ff  mmm  f
    # ''')

    while colony.alive:
        if True or colony.generation in [0, 8512]:
            colony.show()
        if colony.generation % 100 == 0:
            print(colony.generation, colony.population())
        colony.evolve()
        if not colony.alive:
            colony.show()
        # input('Continue')


class Colony:

    def __init__(self):
        self.map = []
        self.generation = 0
        self.past_states = set()
        self.alive = True

    def random_fill(self, size):
        colony_map = []
        for i in range(size[0]):
            line = [random.choice([E, M, F]) for _ in range(size[1])]
            colony_map += [line]
        self.map = colony_map

    def input_by_map(self, input_map):
        input_map = input_map.split('\n')
        input_map = [
            [{' ': 0, 'm': 1, 'f': 2}[c] for c in line]
            for line in input_map
        ]
        max_length = max([len(line) for line in input_map])
        input_map = [
            line + [0] * (max_length - len(line))
            for line in input_map
        ]
        self.map = input_map

    def show(self):
        print('Generation', self.generation)
        print(self.image())
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
        self.map = [[0]+[0]+l+[0]+[0] for l in self.map]
        self.map = (
            [[0] * len(self.map[0])]
            + [[0] * len(self.map[0])]
            + self.map
            + [[0] * len(self.map[0])]
            + [[0] * len(self.map[0])]
        )

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

        if rules == 1:
            deathlist = []
            birthlist = []
            movelist = []
            for i in range(1, len(self.map)-1):
                for j in range(1, len(self.map[i])-1):
                    neighbors = self.neighbors(i, j)
                    if self.map[i][j] != 0 and neighbors[0] in [0, 4]:
                        deathlist += [[i, j]]
                    if (
                            self.map[i][j] == 0 and
                            neighbors[M] == 1 and
                            neighbors[F] == 1
                    ):
                        paircode = ''.join([
                            str(self.map[i+m[0]][j+m[1]])
                            for m in moves
                        ])
                        paircode = [c for c in paircode if c != '0']
                        gender = int(paircode[0])
                        birthlist += [[i, j, gender]]
                    if self.map[i][j] != 0 and neighbors[0] in [3, 2]:
                        moved = False
                        for m in moves:
                            if not moved:
                                new_neighbors = self.neighbors(i+m[0], j+m[1])
                                if (
                                    new_neighbors[0] in [1, 2]
                                    and new_neighbors[0] < neighbors[0]
                                ):
                                    movelist += [[i, j, i+m[0], j+m[1]]]
                                    moved = True
            for b in birthlist:
                self.map[b[0]][b[1]] = b[2]
            for d in deathlist:
                self.map[d[0]][d[1]] = 0
            for m in movelist:
                self.map[m[2]][m[3]] = self.map[m[0]][m[1]]
                self.map[m[0]][m[1]] = 0

        if rules == 2:
            deathlist = []
            birthlist = []
            for i in range(1, len(self.map)-1):
                for j in range(1, len(self.map[i])-1):
                    neighbors = self.neighbors(i, j)
                    if (
                        self.map[i][j] > 0
                        and (neighbors[0] < 2 or neighbors[0] > 3)
                    ):
                        deathlist += [[i, j]]
                    if (
                        self.map[i][j] == 0
                        and neighbors[1] == 3 and neighbors[1] != 2
                    ):
                        birthlist += [[i, j, 1]]
                    if (
                        self.map[i][j] == 0
                        and neighbors[2] == 3 and neighbors[1] != 2
                    ):
                        birthlist += [[i, j, 2]]
                    if neighbors == [2, 1, 1]:
                        index = [0, 0]
                        for n, m in enumerate(moves):
                            if self.map[i+m[0]][j+m[1]] == M:
                                index[0] = n
                            if self.map[i+m[0]][j+m[1]] == F:
                                index[1] = n
                        birthlist += [[i, j, (index[0]-index[1]) % 2 + 1]]
            for b in birthlist:
                self.map[b[0]][b[1]] = b[2]
            for d in deathlist:
                self.map[d[0]][d[1]] = 0

        if hash(self.image()) in self.past_states:
            self.alive = False
        else:
            self.past_states |= {hash(self.image())}
        if sum([sum(i) for i in self.map]) == 0:
            self.alive = False

    def image(self):
        image = '\n'.join([' '.join([' mf'[j] for j in i]) for i in self.map])
        image = re.sub(' +\n', r'\n', image)
        return image

    def population(self):
        males = sum([sum([1 for c in line if c == 1]) for line in self.map])
        females = sum([sum([1 for c in line if c == 2]) for line in self.map])
        total = males+females
        return total, males, females

if __name__ == '__main__':
    main()
