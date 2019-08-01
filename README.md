# assemblyRunner
Basic program to run an assembly like program in the style of the ['TIS 100'](http://www.zachtronics.com/tis-100/) Zachtronics in-game language. I have made the enhancement of adding a DAT storage register on top of the standard ones that come along with the TIS 100 language, as in my version there is only one processor available. I also only have one IN and OUT registers to specify input and then write to console, rather than the TIS 100 four directional inputs and outputs.

# Running
To run, point the PATH variable in main.py at your file of choice and then run 'python3 main.py'. You can add optional input in the constructor of the Interpretor class, which can be read in one at a time by your program.

# Features
Labels for code jumping and flow control can be specified by using a name followed by a colon, e.g. 'MAIN:'.

There are the following registers:
- ACC = The accumalator register, can be directly accessed and used for jump commands
- BAK = A storage register, cannont be directly accessed, only accessable through SAV and SWP commands
- DAT = A data storage register, can be directly accessed to store values
- IN = A register to read input values out of if present
- OUT = A register you can write to, in order to print values to console

There are the following commands:
- MOV \<src\> \<dst\> = Move value specified as 'src' (either int or a register) into 'dst' register
- ADD \<val\> = Add the interger or register specified as 'val' to the ACC register
- SUB \<val\> = Subtract the interger or register specified as 'val' from the ACC register
- JMP \<label\> = Jump execution to the specified label
- JEZ \<label\> = Jump execution to the specified label if the value in ACC is equal to zero
- JGZ \<label\> = Jump execution to the specified label if the value in ACC is greater than zero
- JLZ \<label\> = Jump execution to the specified label if the value in ACC is less than zero

Comments can be made my starting a line witn a \# symbol.

# Example 
The following code takes a zero terminated sequence 
```
LOOP:
MOV IN DAT
MOV DAT ACC
JEZ END
ADD DAT
MOV ACC OUT
JMP LOOP
END:
```
Example input:
```
1,3,5,0
```
Example output:
```
2,5,10
```

# Code Walkthrough
The code is structured with specific enums for commands and registers in the 'command.py' and 'register.py' files. The 'main.py' file simply sets up the interpreter and points it to a file. The action happens in the 'interpreter.py' file. 

On initialisation Interpreter sets up the data by splitting the file on new lines
```
self.file = [line.rstrip('\n') for line in open(self.path)]
```
and then loading in any input data.

It then reads through the file in the 'parse' function to pull out any labels for blocks of code, storing them in a dictionary for later use, along with their line numbers so that we can easily jump to each label. To detect a label we use the simple unil
```
def __is_label(self, line:str) -> bool:
    return line[-1] == ":"
```
and then add to the ditionary once found.

After this it is just a case of iterating through the provided file line by line. At each line we evaluate what the command is and act accordingly. This all happens in the 'run' function. In particular the important code is
```
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
```
where we first handle label definitions, then any jump/flow control commands, and then finally any commands to move data around. I extracted logic to handle jump and data commands into their own functions 'parse_move' and 'parse_command' respectively. Each function is simply a switch statement in effect, extracting the command from the line and then handing it off to a handler funtion. For example this is the 'parse_command' function
```
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
```
which will then hand off the actual handling of each command to dedicated functions if required to keep this code clean.

The code will continue looping until either it is interrupted by the user or reaches the end of the file.