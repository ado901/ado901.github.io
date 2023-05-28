class Actions:
    def __init__(self, values=None):
        if values is None:
            values = dict()
        self._values = values

    def values(self): return self._values

    def eq(self, x, y): return x == y

    def neq(self, x, y): return x != y

    def geq(self, x, y): return x >= y

    def leq(self, x, y): return x <= y

    def gt(self, x, y): return x > y

    def lt(self, x, y): return x < y

    def add(self, x, y):
        if isinstance(x, str) and not isinstance(y, str):
            return x + str(y)
        elif not isinstance(x, str) and isinstance(y, str):
            return str(x) + y
        else:
            return x + y

    def sub(self, x, y):
        if isinstance(x, str) or isinstance(y, str) or isinstance(x, list) or isinstance(y, list):
            print("ERROR: Cannot apply '-' operator to a string or a list.")
            exit(1)
        return x - y

    def mul(self, x, y):
        if isinstance(x, str) or isinstance(y, str) or isinstance(x, list) or isinstance(y, list):
            print("ERROR: Cannot apply '*' operator to a string or a list.")
            exit(1)
        return x * y

    def div(self, x, y):
        if isinstance(x, str) or isinstance(y, str) or isinstance(x, list) or isinstance(y, list):
            print("ERROR: Cannot apply '/' operator to a string or a list.")
            exit(1)
        return x / y

    def mod(self, x, y):
        if isinstance(x, str) or isinstance(y, str) or isinstance(x, list) or isinstance(y, list):
            print("ERROR: Cannot apply '%' operator to a string or a list.")
            exit(1)
        return x % y

    def opp(self, x):
        if isinstance(x, str):#forza peppeeeeeeeeeee
            print("ERROR: Cannot apply '-' operator to a string.")
            exit(1)
        return -x

    def num(self, x):
        return float(x)

    def string(self, x):
        return str(x)

    def list(self, x: str):
        x = map(float, x[1:-1].split(','))
        return list(x)

    def var(self, x):
        return self._values[x] if x in self._values else None

    def set(self, name: str, val):
        if isinstance(val, str):
            val = val[1:-1]
        if name in self._values:
            self._values[name] = val
        else:
            self._values.update({name: val})
        return self._values[name] == val

    def unset(self, name: str):
        if name in self._values:
            self._values.pop(name)

    def print(self, x):
        print(x)


