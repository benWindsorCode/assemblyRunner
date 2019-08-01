from typing import List
from typing import Dict
from command import Command
from register import Register


class Interpreter:
    def __init__(self, path: str, input: List[int] = None):
        self.path: str = path
        self.input: List[int] = input
        self.input_pos: int = None
        self.file: List[str] = []
        self.labels: Dict[str, int] = {}
        self.registers: Dict[Register, int] = { Register.ACC: 0, Register.BAK: 0, Register.DAT: 0, Register.IN: None, Register.OUT: None }
        self.load_data()
        self.parse()

    # Read in file and setup any input
    def load_data(self) -> None:
        self.file = [line.rstrip('\n') for line in open(self.path)]
        if self.input is not None:
            self.registers[Register.IN] = self.input[0]
            self.input_pos = 0

    # Iterate through code and pick out any labels and their locations
    def parse(self) -> None:
        for i in range(len(self.file)):
            if self.__is_label(self.file[i]):
                label = self.file[i][:-1]
                if label in self.labels:
                    raise Exception("Label {} already defined".format(label))
                else:
                    self.labels[label] = i
        
    # Iterate over the file, terminating when current_line reachse the end of the file
    def run(self) -> None:
        terminated = False
        current_line = 0
        # Handle labels, jump commands and register manipulations commands separately
        while terminated is not True:
            line: str = self.file[current_line]
            if self.__is_label(line) or self.__is_comment(line):
                current_line += 1
                pass
            elif self.__is_move(line):
                command: Command = self.extract_command(line)
                label = line.split(" ")[1]
                current_line = self.parse_move(command, label, current_line)
            else:
                command: Command = self.extract_command(line)
                self.parse_command(command, line)
                current_line += 1
                # print(self.registers) use this for debugging purposes to see all registers

            if current_line >= len(self.file):
                terminated = True


    # Given we know the line is not a label we return the enum of its command
    def extract_command(self, line: str) -> Command:
        first_word = line.split(" ")[0]
        return Command[first_word]
    
    # Process a given register manipulation command
    def parse_command(self, command: Command, line: str) -> None:
        if command == Command.MOV:
            second_word: str = line.split(" ")[1]
            third_word: str = line.split(" ")[2]
            self._handle_mov(second_word, third_word)
        elif command == Command.ADD:
            second_word: str = line.split(" ")[1]
            self._handle_add(second_word)
        elif command == Command.SUB:
            val = int(line.split(" ")[1])
            self.registers[Register.ACC] = self.registers[Register.ACC] - val
        elif command == Command.SAV:
            self._handle_sav()
        elif command == Command.SWP:
            self._handle_swp()

    # Given a jump command return the next line to execute
    def parse_move(self, command: Command, label: str, current_line: int) -> int:
        if command == Command.JMP:
            return self.labels[label]
        elif command == Command.JEZ:
            if self.registers[Register.ACC] == 0:
                return self.labels[label]
            else:
                return current_line + 1
        elif command == Command.JGZ:
            if self.registers[Register.ACC] > 0:
                return self.labels[label]
            else:
                return current_line + 1
        elif command == Command.JLZ:
            if self.registers[Register.ACC] < 0:
                return self.labels[label]
            else:
                return current_line + 1
    
    def _handle_mov(self, src: str, dst: str):
        if self.__is_int(src):
            val = int(src)
            self.registers[Register[dst]] = val
        else:
            val = self.registers[Register[src]]
            if Register[src] == Register.IN:
                self.__next_input()
            self.registers[Register[dst]] = val

        if Register[dst] == Register.OUT:
            print(self.registers[Register.OUT])

    def _handle_add(self, second_word: str):
        val = None
        if self.__is_int(second_word):
            val = int(second_word)
        else:
            val = self.registers[Register[second_word]]
        self.registers[Register.ACC] = self.registers[Register.ACC] + val

    def _handle_sav(self) -> None:
        self.registers[Register.BAK] = self.registers[Register.ACC]

    def _handle_swp(self) -> None:
        tmp = self.registers[Register.BAK]
        self.registers[Register.BAK] = self.registers[Register.ACC]
        self.registers[Register.ACC] = tmp

    def __is_label(self, line:str) -> bool:
        return line[-1] == ":"

    def __is_comment(self, line: str) -> bool:
        return line.startswith('#')

    def __is_move(self, line: str) -> bool:
        first_word: str = line.split(" ")[0]
        if Command[first_word] in (Command.JMP, Command.JEZ, Command.JGZ, Command.JLZ):
            return True
        else:
            return False

    def __is_int(self, word: str) -> bool:
        if word[0] in ('-', '+'):
            return word[1:].isdigit()
        return word.isdigit()
    
    def __next_input(self) -> None:
        self.input_pos += 1
        if self.input_pos >= len(self.input):
            self.registers[Register.IN] = None
        else:
            self.registers[Register.IN] = self.input[self.input_pos]
