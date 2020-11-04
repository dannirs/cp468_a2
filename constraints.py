class Constraints:
    def __init__(self, name):
        self.name = name
        self.scope = list(scope)
        self.satisfied_tuple = dict()
        self.buffer_tuple = dict()

    def add_tuple(self, tuple):
        for i in tuple:
            t = tuple(i)
            if not t in self.satisfied_tuple:
                self.satisfied_tuple[t] = True

        for j, value in enumerate(t):
            val = self.scope[j]
            if not (val, value) in self.buffer_tuple:
                self.buffer_tuple[(val, value)] = []
            self.buffer_tuple[(val, value)].append(t)

    def get_scope(self):
        return list(self.scope)

    def check_buffer_tuples(self, val):
        return tuple(val) in self.buffer_tuple

    def check_asmt(self):
