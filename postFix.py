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
            raise Exception("Tumpukan sudah kosong. Tidak bisa diambil lagi")
        data = self.top.data
        self.top = self.top.next
        return data
    
    def peek(self):
        if self.empty():
            return None
        return self.top.data

class PostfixEvaluator:
    def __init__(self):
        self.stack_operand = []
        self.stack_operator = LinkedStack()

    def _priority(self, symbol):
        if symbol == '(': return 1
        if symbol == ')': return 2
        if symbol in ('+', '-'): return 3
        if symbol in ('*', '/', '%'): return 4
        if symbol == '^': return 5
        return 0

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
        self.stack_operator = LinkedStack()
        postfix = ""
        self.stack_operator.push('(')
        infix_str += ')'

        i = 0
        while i < len(infix_str):
            symbol = infix_str[i]

            if symbol == ' ':
                i += 1
                continue

            if symbol.isdigit():
                angka = ''
                while i < len(infix_str) and infix_str[i].isdigit():
                    angka += infix_str[i]
                    i += 1
                postfix += angka + ' '
                continue

            priority = self._priority(symbol)

            if priority == 1:  # '('
                self.stack_operator.push(symbol)
            elif priority == 2:  # ')'
                while True:
                    char = self.stack_operator.pop()
                    if char == '(':
                        break
                    postfix += char + ' '
            elif priority in [3, 4, 5]:
                while True:
                    top = self.stack_operator.peek()
                    if top is None or self._priority(top) < priority:
                        break
                    postfix += self.stack_operator.pop() + ' '
                self.stack_operator.push(symbol)
            else:
                postfix += symbol + ' '

            i += 1

        return postfix.strip()


    def eval_postfix(self, postfix_str):
        stack = []
        tokens = postfix_str.split()

        for token in tokens:
            if token.isdigit():
                stack.append(int(token))
            else:
                if len(stack) < 2:
                    raise Exception("Ekspresi postfix tidak valid. Kurang operand.")
                op2 = stack.pop()
                op1 = stack.pop()
                result = self._calculate(token, op1, op2)
                stack.append(result)
            
        if len(stack) != 1:
            raise Exception("Ekspresi postfix tidak valid. Terlalu banyak operand.")
        return stack.pop()

    def eval_infix(self, infix_str):
        postfix = self.get_result(infix_str)
        print("Postfix =", postfix)
        result = self.eval_postfix(postfix)
        return result

# Contoh penggunaan:
start = "ya"
while start == "ya":
    evaluator = PostfixEvaluator()
    infix_expr = input(str("Masukkan ekspresi infix : "))
    print("Infix =", infix_expr)
    result = evaluator.eval_infix(infix_expr)
    print("Hasil evaluasi =", result)

    start = input("Apakah kamu ingin tetap melanjutkannya? [Ketik ya / tidak] : ").lower()
    
if start == "tidak":
    print("Terima Kasih")
else:
    print("Input tidak valid, program dihentikan.")