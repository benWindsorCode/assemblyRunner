# assemblyRunner
Basic program to run an assembly like program in the style of the ['TIS 100'](http://www.zachtronics.com/tis-100/) Zachtronics in-game language. I have made the enhancement of adding a DAT storage register on top of the standard ones that come along with the TIS 100 language, as in my version there is only one processor available.

# Running
To run, point the PATH variable in main.py at your file of choice and then run 'python3 main.py'. You can add optional input in the constructor of the Interpretor class, which can be read in one at a time by your program.

# Features
There are the following registers:
- ACC = The accumalator register, can be directly accessed and used for jump commands
- BAK = A storage register, cannont be directly accessed, only accessable through SAV and SWP commands
- DAT = A data storage register, can be directly accessed to store values

There are the following commands:
- MOV \<src\> \<dst\>
