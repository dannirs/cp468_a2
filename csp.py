class CSP:
    def __init__(self, filename):
        self.variables = [r + c for r in 'ABCDEFGHI' for c in '123456789']
        self.domain = dict(
            (self.variables[i], fullDomain if inp[i] == '0' else inp[i]) for i in range(len(inp)))
        a = [self.colNeighbors(self.variables, i) for i in range(9)]
        b = [self.rowNeighbors(self.variables, i) for i in range(9)]
        c = [self.blockNeighbors(self.variables, i, j)
             for i in range(9) for j in range(9)]
        self.cells = (a + b + c)
        self.cellNeighbors = dict(
            (s, [u for u in self.cells if s in u]) for s in self.variables)
        self.neighbors = dict(
            (s, set(sum(self.cellNeighbors[s], [])) - set([s])) for s in self.variables)
        self.constraints = {(variable, neighbor)
                            for variable in self.variables for neighbor in self.neighbors[variable]}

        def colNeighbors(self, b, col):
            neighbors = []
        for i in range(col, len(b), 9):
            neighbors.append(b[i])

        return neighbors

    def rowNeighbors(self, b, row):
        neighbors = []
        end = (row + 1) * 9
        start = end - 9
        for i in range(start, end, 1):
            neighbors.append(b[i])

        return neighbors

    def blockNeighbors(self, b, row, col):
        neighbors = []
        domRow = row - row % 3
        domCol = col - col % 3
        for j in range(3):
            for i in range(3):
                v = b[(j + domCol) + (i + domRow) * 9]
                neighbors.append(v)

        return neighbors
