import re

class Parser:
    def __init__(self):
        # Table and headers as given
        self.headerList = ['State', 'id', '+', '*', '(', ')', '$', 'E', 'T', 'F']
        self.table = [
            ['State', 'id', '+', '*', '(', ')', '$', 'E', 'T', 'F'],
            [0, 'S5', 0, 0, 'S4', 0, 0, 1, 2, 3],
            [1, 0, 'S6', 0, 0, 0, 'accept', 0, 0, 0],
            [2, 0, 'R2', 'S7', 0, 'R2', 'R2', 0, 0, 0],
            [3, 0, 'R4', 'R4', 0, 'R4', 'R4', 0, 0, 0],
            [4, 'S5', 0, 0, 'S4', 0, 0, 8, 2, 3],
            [5, 0, 'R6', 'R6', 0, 'R6', 'R6', 0, 0, 0],
            [6, 'S5', 0, 0, 'S4', 0, 0, 0, 9, 3],
            [7, 'S5', 0, 0, 'S4', 0, 0, 0, 0, 10],
            [8, 0, 'S6', 0, 0, 'S11', 0, 0, 0, 0],
            [9, 0, 'R1', 'S7', 0, 'R1', 'R1', 0, 0, 0],
            [10, 0, 'R3', 'R3', 0, 'R3', 'R3', 0, 0, 0],
            [11, 0, 'R5', 'R5', 0, 'R5', 'R5', 0, 0, 0]
        ]

        # Convert table to dictionary
        self.dictionary = {}
        for row in self.table[1:]:
            key = row[0]
            value = row[1:]
            self.dictionary[key] = value

        # Grammar rules
        self.grammar = {
            'R1': ('E', ['E', '+', 'T']),
            'R2': ('E', ['T']),
            'R3': ('T', ['T', '*', 'F']),
            'R4': ('T', ['F']),
            'R5': ('F', ['(', 'E', ')']),
            'R6': ('F', ['id'])
        }

        self.stack = []
        self.buffer = []
        self.actions = []

    def findAction(self):
        stackLast = self.stack[-1]
        bufferFirst = self.headerList.index(self.buffer[0]) - 1
        return self.dictionary[stackLast][bufferFirst]

    def shift(self, action):
        if self.buffer:
            temp = self.buffer.pop(0)
            self.stack.append(temp)
            self.stack.append(int(action[1:]))

    def reduce(self, action):
        self.stack.pop()
        rule = self.grammar[action]

        # This logic remains the same as the original code
        if len(rule[1]) == 1:
            # Single symbol reduction
            temp = rule[1][0]
            convert = rule[0]
            tempIndex = self.stack.index(temp)
            self.stack[tempIndex] = convert

        elif len(rule[1]) == 3:
            # Three-symbol production
            convert = rule[0]
            # Find the positions of the three symbols
            s1, s2, s3 = rule[1]
            index1 = self.stack.index(s1)
            valIndex = self.stack.index(s2)
            index2 = self.stack.index(s3)

            if index1 < valIndex < index2:
                self.stack = self.stack[:index1] + [convert] + self.stack[index2 + 1:]

        # Perform goto step if needed
        if len(self.stack) >= 2:
            if isinstance(self.stack[-1], str):
                goto_val = self.dictionary[self.stack[-2]][self.headerList.index(self.stack[-1]) - 1]
                self.stack.append(goto_val)

    def applyAction(self, action):
        if action.startswith('S'):
            self.shift(action)
        else:
            self.reduce(action)

    def parse(self, inputText):
        # Reset stacks and actions for each parse
        self.stack = [0]
        self.actions = []

        # Tokenize input and append $
        self.buffer = re.findall(r'[\w]+|[\+\-\*\(\)/]', inputText)
        self.buffer.append('$')

        while True:
            action = self.findAction()
            self.actions.append(action)
            if action == 0:
                return "INVALID string entered. SYNTAX ERROR!"
            elif action == 'accept':
                return "VALID string entered. ACCEPTED!"
            else:
                self.applyAction(action)


if __name__ == "__main__":
    parser = Parser()
    while True:
        user_input = input("Enter your string:\n")
        if user_input.lower() == 'q':
            break
        result = parser.parse(user_input)
        print(result)
