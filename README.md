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
Example input \[1,3,5,0\]
Example output \[2,5,10\]