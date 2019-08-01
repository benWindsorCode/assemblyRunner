from typing import List, Dict
from registers import Registers


class Interpreter:
    def __init__(self, path):
        self.path: str = path
        self.file: List[str] = []
        self.labels: Dict[str, int] = {}
        self.data: Dict[Registers, int] = { Registers.ACC: 0, Registers.BAK: 0 }
        self.current_line = 0
        self.load_data()
        self.parse()

    def load_data(self):
        self.file = [line.rstrip('\n') for line in open(self.path)]

    # Iterate through code and pick out any labels and their locations
    def parse(self):
        for i in range(len(self.file)):
            if self.file[i][-1] == ":":
                label = self.file[i][:-1]
                if label in self.labels:
                    raise Exception("Label {} already defined".format(label))
                else:
                    self.labels[label] = i
        
    def run(self):
        pass
    def execute(self):
        pass
