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
