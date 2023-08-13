from collections import deque


class Calculator:
    operators = ['+', '-', '*', '/']
    priority = {'*': 2, '/': 2, '+': 1, '-': 1}

    def __init__(self):
        self.variables = {}
        self.equation = []

    def remove_spaces(self):
        for i in range(len(self.equation) - 1):
            if not ((self.equation[i].isalnum() == self.equation[i + 1].isalnum()) and (self.equation[i].isalnum())):
                if not ((self.equation[i] in self.operators == self.equation[i + 1] in self.operators) and (
                        self.equation[i] in self.operators)):
                    self.equation[i] += ' '
        st = "".join(self.equation)
        self.equation = st.split()

    def process_list(self):
        if self.equation[0] == '-':
            self.equation.insert(0, '0')
        for count, el in enumerate(self.equation):
            if el.isnumeric():
                self.equation[count] = int(el)
            elif set(list(el)).union(set(self.operators)) == set(
                    self.operators):
                if "+" in self.equation[count]:
                    self.equation[count] = "+"
                elif len(self.equation[count]) % 2 == 0 and '-' in self.equation[count]:
                    self.equation[count] = "+"
                elif len(self.equation[count]) % 2 == 1 and '-' in self.equation[count]:
                    self.equation[count] = "-"
            elif el == '(' or el == ')':
                continue
            elif el.isalpha():
                if el in self.variables:
                    self.equation[count] = self.variables[el]
                else:
                    raise ValueError('Unknown variable')
            else:
                raise ValueError('Invalid identifier')

    def to_postfix(self):
        my_deque = deque()
        result = []
        for el in self.equation:
            if type(el) == int:
                result.append(el)
            elif el in self.operators:
                if len(my_deque) == 0 or my_deque[-1] == '(':
                    my_deque.append(el)
                else:
                    while self.priority[el] <= self.priority[my_deque[-1]]:
                        result.append(my_deque.pop())
                        if len(my_deque) == 0 or my_deque[-1] == '(':
                            break
                    my_deque.append(el)
            elif el == '(':
                my_deque.append(el)
            else:
                while my_deque[-1] != '(':
                    result.append(my_deque.pop())
                my_deque.pop()
        while len(my_deque) > 0:
            result.append(my_deque.pop())
        self.equation = result

    def calculate(self):
        my_deque = deque()
        for el in self.equation:
            if type(el) == int:
                my_deque.append(el)
            else:
                b = my_deque.pop()
                a = my_deque.pop()
                if el == '+':
                    my_deque.append(a + b)
                elif el == '-':
                    my_deque.append(a - b)
                elif el == '*':
                    my_deque.append(a * b)
                elif el == '/':
                    my_deque.append(a / b)
        return int(my_deque[-1])

    def start(self):
        if '=' in self.equation:
            self.remove_spaces()
            if self.equation.count('=') > 1:
                print("Invalid assignment")
            elif not self.equation[0].isalpha():
                print("Invalid identifier")
            elif self.equation[2].isnumeric():
                self.variables[self.equation[0]] = int(self.equation[2])
            elif self.equation[2].isalpha():
                if self.equation[2] in self.variables:
                    self.variables[self.equation[0]] = self.variables[self.equation[2]]
                else:
                    print("Unknown variable")
            else:
                print("Invalid assignment")
        else:
            try:
                self.remove_spaces()
                self.process_list()
                self.to_postfix()
                print(self.calculate())
            except ValueError as e:
                print(e.args[0])
            except IndexError:
                print('Invalid expression')


calc = Calculator()
while True:
    calc.equation = list(input().strip())
    if not calc.equation:
        continue
    elif calc.equation[0] == '/':
        if "".join(calc.equation) == '/exit':
            print('Bye!')
            break
        elif "".join(calc.equation) == '/help':
            print('The program calculates the inputted (series of) basic arithmetic operations')
            continue
        else:
            print('Unknown command')
        continue
    calc.start()
