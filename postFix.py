class NodeStack:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedStack:
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = NodeStack(data)
        new_node.next = self.top
        self.top = new_node

    def empty(self):
        return self.top is None

    def pop(self):
        if self.empty():
            print("Tumpukan sudah kosong. Tidak bisa diambil lagi")
            return ''
        data = self.top.data
        self.top = self.top.next
        return data

class PostfixEvaluator:
    MAXSIZE = 100

    def __init__(self):
        self.stack_operand = [0] * self.MAXSIZE
        self.top = -1
        self.stack = LinkedStack()

    def _priority(self, symbol):
        if symbol == '(': return 1
        if symbol == ')': return 2
        if symbol in ('+', '-'): return 3
        if symbol in ('*', '/', '%'): return 4
        if symbol == '^': return 5
        return 0

    def _push_operand(self, val):
        if self.top == self.MAXSIZE - 1:
            print("Overflow")
            exit(1)
        self.top += 1
        self.stack_operand[self.top] = val

    def _pop_operand(self):
        if self.top == -1:
            print("Stack kosong")
            exit(1)
        val = self.stack_operand[self.top]
        self.top -= 1
        return val

    def _calculate(self, oper, op1, op2):
        if oper == '^':
            return op1 ** op2
        if oper == '*':
            return op1 * op2
        if oper == '/':
            return op1 // op2
        if oper == '%':
            return op1 % op2
        if oper == '+':
            return op1 + op2
        if oper == '-':
            return op1 - op2

    def get_result(self, infix_str):
        while not self.stack.empty():
            self.stack.pop()

        postfix_str = ''
        infix_str += ')'
        self.stack.push('(')

        for symbol in infix_str:
            priority = self._priority(symbol)
            if priority == 1:  # '('
                self.stack.push(symbol)
            elif priority == 2:  # ')'
                char = self.stack.pop()
                while char != '(':
                    postfix_str += char
                    char = self.stack.pop()
            elif priority in [3, 4, 5]:
                char = self.stack.pop()
                while self._priority(char) >= priority:
                    postfix_str += char
                    char = self.stack.pop()
                self.stack.push(char)
                self.stack.push(symbol)
            else:
                postfix_str += symbol

        return postfix_str

    def eval_postfix(self, postfix_str):
        print("Postfix =", postfix_str)
        for char in postfix_str:
            if char.isdigit():
                self._push_operand(int(char))
            else:
                op2 = self._pop_operand()
                op1 = self._pop_operand()
                result = self._calculate(char, op1, op2)
                self._push_operand(result)

        return self._pop_operand()

    def eval_infix(self, infix_str):
        postfix = self.get_result(infix_str)
        return self.eval_postfix(postfix)

# Contoh penggunaan:
if __name__ == "__main__":
    evaluator = PostfixEvaluator()
    infix_expr = "3+4*2/(1-5)^2"
    print("Infix =", infix_expr)
    result = evaluator.eval_infix(infix_expr)
    print("Hasil evaluasi =", result)