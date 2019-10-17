# TMBWW2
A programming language which is based on Turing Machines but supports I/O.

This is a fork of [this repo](https://github.com/MilkyWay90/Turing-Machine-But-Way-Worse) by [MilkyWay90](https://github.com/MilkyWay90) which seems to be dead.

The new features of TMBWW2 are:

    - Macros
    
    - Include (at the top)

    - Provide separate .tape file
    
    - Object oriented code

**NOTE: THIS ASSUMES THAT YOU DO KNOW WHAT A TURING MACHINE IS**

A tutorial on Turing Machines can be found [here](https://www.youtube.com/watch?v=dNRDvLACg5Q)

## Usage
The TMBWW2 interpreter is a Python script which can be invoked as follows:

``python TMBWW2.py <.tmw file>, (<.tape file>)``

## Syntax
Each TMBWW instruction has the following form:

        Number to be read (0/1), Current State (0-9|a-z), Write (0/1),
        Move (0 = left, 1 = right), Goto state (0-9|a-z), Print (0 = no, 1 = yes), Exit = (0/1)
    
For example,

    0 0 1 1 a 0 1

Would be `if the number the robot is seeing is 0 and the robot is in state 0, replace the number with 1, move right, go to state a, don't print, and halt the program (stop the program)`

These instructions constitute a TMBWW program. There are usually kept in .tmw files.

## Printing
To print, you need to set the sixth bit of an TMBWW instruction. This will print the current byte.

Let's say that the tape is

    <... infinite zeros ...> 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 <... infinite zeros ...>
                                     ^
and you decide to print.

First, the program would seperate the tape into seperate bytes:

    <... infinite zeros ...>|0 1 0 1 0 1 0 1|0 1 0 1 0 1 0 1|0 1 0 1 0 1 0 1|<... infinite zeros ...>
                                     ^
The eight bits that the robot is in are `0 1 0 1 0 1 0 1`

Converting that to base-10, we get `85`, and that in ASCII is `U`.

Congratulations, you have printed the character `U`.

**Note: Turing Machine But Way Worse doesn't append a trailing newline to the output (printing A and then B would result in AB, not A\nB)**

## Input
The input which is used as the tape for the Turing machine can be either provided as the second argument of the TMBWW2 interpreter or via piping.
TMBWW2 tapes are usually kept in .tape files.

Let's say that the input is `hi`.

Taking the ASCII values of these gives us `['01101000', '01101001']`.

Concatenating the list gives us `0110100001101001`.

Therefore, the tape is `<... infinite zeros ...>0 1 1 0 1 0 0 0 0 1 1 0 1 0 0 1<... infinite zeros ...>`.

If there is no input, the tape is `<... infinite zeros ...>0 0 0 0 0 0 0 0<... infinite zeros ...>`.
