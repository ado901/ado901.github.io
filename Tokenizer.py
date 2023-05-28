import re


class Tokenizer:
    def __init__(self, text, regex):
        #print("Tokenizer: " + text)
        self._text = text.rstrip()
        self._point = 0
        self._token_re = re.compile(regex)

    def get_point(self):
        return self._point

    def set_point(self, point):
        self._point = point

    def peek(self):
        #print("peek: " + str(self._token_re.match(self._text, self._point).group(1)))
        return self._token_re.match(self._text, self._point).group(1)

    def consume(self, x, error=None):
        #print("consume: " + str(self._token_re.match(self._text, self._point).group(1)))
        m = self._token_re.match(self._text, self._point)
        if m.group(1) != x:
            print(("ERROR: Expected " + x) if error is None else error)
            exit(1)
        self._point = m.end()

    def end(self):
        if self._point < len(self._text):
            print("Extra stuff after 'main' block.")
            return False
        return True
