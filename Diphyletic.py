import random


E, M, F = range(3)  # empty, males, females


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

    def evolve(self):
        self.check_borders()
        self.generation += 1


if __name__ == '__main__':
    main()
