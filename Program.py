from Actions import Actions
from Tokenizer import Tokenizer
from Error import Error


class Program:
    def __init__(self, text: str, regex: str = r'\s*(".*"|[A-Za-z0-9\.]+|.?)'):
        self._act = Actions()
        #print("Program: " + text)
        self._tok = Tokenizer(text, regex)
        self._stmt_funcs = {
            'if': self.__if,
            'while': self.__while,
            'do': self.__do,
            'for': self.__for,
            'print': self.__print,
            'set': self.__set
        }
        self._binary_cond_funcs = {
            'EQ': self._act.eq,
            'NEQ': self._act.neq,
            'GEQ': self._act.geq,
            'LEQ': self._act.leq,
            'GT': self._act.gt,
            'LT': self._act.lt,
        }

    def values(self):
        return self._act.values()

    def __exec_stmts(self, fake=False):
        nxt = self._tok.peek()
        while nxt in ("if", "while", "do", "for", "print", "set"):
            self.stmt(fake)
            nxt = self._tok.peek()

    def __exec_conditional_stmts(self, then_error: str, stmt_error: str, fake: bool):
        self._tok.consume(x="then", error=f"ERROR: {then_error}")
        if self._tok.peek() not in ("if", "while", "do", "for", "print", "set"):
            print(f"ERROR: {stmt_error}")
            exit(1)
        self.__exec_stmts(fake)

    def __eval_binary_cond(self, prev_outcome=True, logic_op=''):
        left_expr = self.expr()
        cond_op = self._tok.peek()
        self._tok.consume(cond_op)
        if cond_op not in self._binary_cond_funcs:
            print(f"ERROR: {Error.OP_ERR.value} (Specified condition operator: {cond_op}).")
            exit(1)
        right_expr = self.expr()
        if logic_op == 'AND':
            return prev_outcome and self._binary_cond_funcs[cond_op](left_expr, right_expr)
        elif logic_op == 'OR':
            return prev_outcome or self._binary_cond_funcs[cond_op](left_expr, right_expr)
        else:
            return self._binary_cond_funcs[cond_op](left_expr, right_expr)

    def __print(self, fake=False):
        result = self.expr()
        if not fake:
            if isinstance(result, str):
                result = result.replace('"', '')
            self._act.print(result)
        return result

    def __cond(self):
        outcome = self.__eval_binary_cond()
        logic_op = self._tok.peek()
        while logic_op in ('AND', 'OR'):
            self._tok.consume(logic_op)
            outcome = self.__eval_binary_cond(prev_outcome=outcome, logic_op=logic_op)
            logic_op = self._tok.peek()
        return outcome

    def __set(self, fake=False):
        name = self._tok.peek()
        # print(f"DEBUG: name={name}")
        self._tok.consume(name)
        if not name.isalpha():
            print(f"ERROR: {Error.INV_VAR.value} (Variable name: {name}).")
            exit(1)
        self._tok.consume(x="=", error=f"ERROR: {Error.EQ_MISS.value} (Variable name: {name}).")
        value = self.expr()
        # print(f"DEBUG: stmt SET (var={name}, val={value}) (fake={fake}):")
        if not fake and not self._act.set(name, value):
            print(f"ERROR: Error during variable assignment (variable name: {name})")
            exit(1)

    def __for(self, fake=False):
        self._tok.consume(x="set", error=f"ERROR: {Error.SET_MISS.value}")
        tmp_var = self._tok.peek()
        self._tok.consume(tmp_var)
        if self._act.var(tmp_var) is not None:
            print(f"ERROR: {Error.FOR_VAR.value} (Variable name: {tmp_var}")
            exit(1)
        self._tok.consume(x="in", error=f"ERROR: {Error.IN_MISS.value}")
        self._tok.consume(x="range", error=f"ERROR: {Error.RANGE_MISS.value}")
        self._tok.consume(x="(", error=f"ERROR: {Error.LBRACKET_MISS.value}")
        start = self._tok.peek()
        if start.isalpha() and self._act.var(start) is None:
            print(f"ERROR: {Error.UNSET_VAR_FOR.value} (Variable name: {start}")
            exit(1)
        self._tok.consume(start)
        self._tok.consume(x=",", error=f"ERROR: {Error.COMMA_MISS.value}")
        end = self._tok.peek()
        if end.isalpha() and self._act.var(end) is None:
            print(f"ERROR: {Error.UNSET_VAR_FOR.value} (Variable name: {end}")
            exit(1)
        self._tok.consume(end)
        self._tok.consume(x=")", error=f"ERROR: {Error.RBRACKET_MISS.value}")
        self._tok.consume(x="then", error=f"ERROR: {Error.THEN_FOR.value}")
        point = self._tok.get_point()
        start = int(self._act.var(start)) if self._act.var(start) is not None else int(start)
        end = int(self._act.var(end)) if self._act.var(end) is not None else int(end)
        # print(f"DEBUG: Inizio stmt FOR per {tmp_var} in ({start}, {end}) (fake={fake}):")
        # count = 1
        for tmp_value in range(start, end):
            self._tok.set_point(point)
            self._act.set(tmp_var, tmp_value)
            # print(f"DEBUG: Inizio exec stmts in FOR (fake={fake}): CICLO {count}")
            self.__exec_stmts(fake)
            if fake:
                break
            # count += 1
        self._act.unset(tmp_var)
        self._tok.consume(x="endfor", error=f"ERROR: {Error.END_FOR.value}")
        # print(f"DEBUG: Fine stmt FOR (fake={fake}):")

    def __do(self, fake=False):
        point = self._tok.get_point()
        self.__exec_stmts(fake)
        self._tok.consume(x="whiledo", error=f"ERROR: {Error.WHILE_DO.value}")
        while self.__cond():
            if fake:
                break
            self._tok.set_point(point)
            self.__exec_stmts(fake)
            self._tok.consume(x="whiledo", error=f"ERROR: {Error.WHILE_DO.value}")

    def __while(self, fake=False):
        # print(f"DEBUG: Inizio stmt while (fake={fake}):")
        point = self._tok.get_point()
        # count = 1
        while self.__cond():
            self._tok.consume(x="then", error=f"ERROR: {Error.THEN_WHILE.value}")
            # print(f"DEBUG: Inizio exec stmts in while (fake={fake}): CICLO {count}")
            self.__exec_stmts(fake)
            self._tok.set_point(point)
            # count += 1
            if fake:
                self.__cond()
                break
        self._tok.consume(x="then", error=f"ERROR: {Error.THEN_WHILE.value}")
        # print(f"DEBUG: Inizio stmts di terminazione while (fake=True):")
        self.__exec_stmts(fake=True)
        self._tok.consume(x="endwhile", error=f"ERROR: {Error.END_WHILE.value}")
        # print(f"DEBUG: Fine stmt while (fake={fake}).")

    def __if(self, fake=False):
        # print(f"DEBUG: Inizio stmt IF (fake={fake}):")
        satisfied_condition = self.__cond()
        if fake:
            satisfied_condition = False
        # print(f"DEBUG: stmt IF: cond_soddisfatta={satisfied_condition} (fake={fake}):")
        # print(f"DEBUG: Inizio exec stmt condizionali IF (fake={not satisfied_condition}):")
        self.__exec_conditional_stmts(then_error=Error.THEN_IF.value,
                                      stmt_error=Error.STMT_IF.value,
                                      fake=not satisfied_condition)
        # print(f"DEBUG: Fine exec stmts condizionali IF (fake={not satisfied_condition}).")
        must_else = False
        nxt = self._tok.peek()
        while nxt == "elseif":
            must_else = True
            self._tok.consume(nxt)
            condition = (not satisfied_condition) and self.__cond()
            if condition:
                satisfied_condition = True
            if fake:
                condition = False
            self.__exec_conditional_stmts(then_error=Error.THEN_ELSEIF.value,
                                          stmt_error=Error.STMT_ELSEIF.value,
                                          fake=not condition)
            nxt = self._tok.peek()
        if must_else or self._tok.peek() == "else":
            self._tok.consume(x="else", error=f"ERROR: {Error.ELSE.value}")
            if fake:
                satisfied_condition = True
            # print(f"DEBUG: Inizio stmt else di IF (cond_soddisfatta={satisfied_condition}) (fake={fake}):")
            # print(f"DEBUG: Inizio exex stmts ELSE (fake={satisfied_condition}):")
            self.__exec_stmts(fake=satisfied_condition)
            # print(f"DEBUG: Fine stmt else di IF e fine IF (fake={fake}).")
        self._tok.consume(x="endif", error=f"ERROR: {Error.END_IF.value}")

    # mainBlock = 'main' '{' {stmt} '}'
    def mainBlock(self):
        self._tok.consume(x="main", error=f"ERROR: {Error.INV_MAIN.value}")
        self._tok.consume(x="{", error=f"ERROR: {Error.LBRACE.value}")
        # print(f"DEBUG: Inizio stmts mainBlock:")
        self.__exec_stmts()
        # print(f"DEBUG: Fine stmts mainBlock.")
        self._tok.consume(x="}", error=f"ERROR: {Error.RBRACE.value}")
        return self._tok.end()

    def stmt(self, fake=False):
        nxt = self._tok.peek()
        self._tok.consume(nxt)
        # print(f"DEBUG: *IN STMT FUNC* Inizio stmt {nxt} (fake={fake}):")
        if nxt in self._stmt_funcs:
            self._stmt_funcs[nxt](fake)
        else:
            print(f"ERROR: Invalid syntax found during statement parsing (parsed: {nxt}).")
            exit(1)
        # print(f"DEBUG: Fine stmt {nxt}.")
        return True

    # expr = term {( '+' | '-' ) term}
    def expr(self):
        x = self.term()
        nxt = self._tok.peek()
        while nxt in ('+', '-'):
            self._tok.consume(nxt)
            y = self.term()
            if nxt == '+':
                x = self._act.add(x, y)
            else:
                x = self._act.sub(x, y)
            nxt = self._tok.peek()
        return x

    # term = factor {( '*' | '/' | '%') factor}
    def term(self):
        x = self.factor()
        nxt = self._tok.peek()
        while nxt in ('*', '/', '%'):
            self._tok.consume(nxt)
            y = self.factor()
            if nxt == '*':
                x = self._act.mul(x, y)
            elif nxt == '/':
                x = self._act.div(x, y)
            else:
                x = self._act.mod(x, y)
            nxt = self._tok.peek()
        return x

    # factor = '-' factor | '(' expr ')' | string | var | num
    def factor(self):
        nxt = self._tok.peek()
        #print(f"DEBUG: Inizio parsing factor (fake=False):{nxt}")
        if nxt == '-':
            self._tok.consume('-')
            x = self.factor()
            return self._act.opp(x)
        elif nxt == '(':
            self._tok.consume('(')
            x = self.expr()
            self._tok.consume(')')
            return x
        elif nxt.startswith('"') and nxt.endswith('"'):
            self._tok.consume(nxt)
            x = self._act.string(nxt)
            return x
        elif nxt=='[':
            self._tok.consume('[')
            x=[]
            while self._tok.peek() != ']':
                x.append(self.expr())
                if self._tok.peek() == ',':
                    self._tok.consume(',')
            self._tok.consume(']')
            return x
        elif nxt.startswith('[') and nxt.endswith(']'):
            self._tok.consume(nxt)
            x = self._act.list(nxt)
            return x
        elif nxt.isalpha():
            self._tok.consume(nxt)
            x = self._act.var(nxt)
            if x is None:
                print(f"ERROR: {Error.INV_VAR.value} (Variable name: {nxt}).")
                exit(1)
            return x
        else:
            #print(f"DEBUG: Inizio parsing num (fake=False):{nxt}")
            self._tok.consume(nxt)
            x = self._act.num(nxt)
            return x


def prova():
    print("prova")
    return 1
