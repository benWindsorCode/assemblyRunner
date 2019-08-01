from interpreter import Interpreter

def run():
    PATH="./scripts/test.txt"
    interpreter = Interpreter(PATH, [1, 4, 7, 11, 0])
    interpreter.run()

if __name__ == "__main__":
    run()