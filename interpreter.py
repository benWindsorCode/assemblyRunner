from typing import List, Dict
from command import Command
from register import Register


class Interpreter:
    def __init__(self, path):
        self.path: str = path
        self.file: List[str] = []
        self.labels: Dict[str, int] = {}
        self.registers: Dict[Register, int] = { Register.ACC: 0, Register.BAK: 0, Register.IN: None, Register.OUT: None }
        self.load_data()
        self.parse()

    def load_data(self):
        self.file = [line.rstrip('\n') for line in open(self.path)]

    # Iterate through code and pick out any labels and their locations
    def parse(self):
        for i in range(len(self.file)):
            if self.__is_label(self.file[i]):
                label = self.file[i][:-1]
                if label in self.labels:
                    raise Exception("Label {} already defined".format(label))
                else:
                    self.labels[label] = i
        
    def run(self):
        terminated = False
        current_line = 0

        while terminated is not True:
            line: str = self.file[current_line]
            if self.__is_label(line):
                current_line += 1
                pass
            else:
                command: Command = self.extract_command(line)
                self.parse_command(command, line)
                current_line += 1

    # Given we know the line is not a label we return the enum of its command
    def extract_command(self, line: str) -> Command:
        first_word = line.split(" ")[0]
        return Command[first_word]
    
    def parse_command(self, command: Command, line: str):
        if command == Command.MOV:
            second_word: str = line.split(" ")[1]
            third_word: str = line.split(" ")[2]
            self._handle_mov(second_word, third_word)
            print(self.registers)
    
    def _handle_mov(self, src: str, dst: str):
        if self.__is_int(src):
            val = int(src)
            self.registers[Register[dst]] = val
        else:
            val = self.registers[Register[src]]
            self.registers[Register[dst]] = val

    def __is_label(self, line):
        return line[-1] == ":"

    def __is_int(self, word: str):
        if word[0] in ('-', '+'):
            return word[1:].isdigit()
        return word.isdigit()
