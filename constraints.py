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
        return

    def get_scope(self):
        return list(self.scope)

    def check_buffer_tuples(self, val):
        return tuple(val) in self.buffer_tuple

    def asmts(self):
        n = 0
        vals = []
        for s in self.scope:
            # needs to improve to check if it is not assigned
            if not s:
                n = n + 1
                vals.append(s)
        return n, vals

    def check_tuple_vaild(self, t):
        check = False
        for x, val in enumerate(self, scope):
            # need to improve
            if val:
                check = True
        return check

    def check_buffer(self, val, value):
        check = False
        if (val, value) in self.buffer_tuple:
            for b in self.buffer_tuple[val, value]:
                if self.check_tuple_vaild(b):
                    check = True
        return check
