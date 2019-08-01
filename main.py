from interpreter import Interpreter

def run():
    PATH="./scripts/test.txt"
    interpreter = Interpreter(PATH)
    interpreter.run()

if __name__ == "__main__":
    run()