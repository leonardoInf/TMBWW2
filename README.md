# Turing-Machine-But-Way-Worse
A programming language which is based off of Turing Machines but supports I/O

**NOTE: THIS ASSUMES THAT YOU DO KNOW WHAT A TURING MACHINE IS**

A tutorial on Turing Machines can be found [here](https://www.youtube.com/watch?v=dNRDvLACg5Q)

## Syntax

                 0/1                                     <any char>                                  0/1                     
    if the robot sees the number 0/1                and state is <any char>                  replace the number with 0/1
    
                 0/1                                      <any char>                                 0/1
    move left/right, respectively                    go to state <any char>               print (will be explained in more detail)
    
                 0/1
    Stop/halt the program if this is 1
    
For example,

    0 0 1 1 a 0 1

Would be `if the number the robot is seeing is 0 and the robot is in state 0, replace the number with 1, move right, go to state a, don't print, and halt the program (stop the program)`

## Printing

Let's say that the tape is

    <... infinite zeros ...> 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 <... infinite zeros ...>
                                     ^
and you decide to print.

First, the program would seperate the tape into seperate pieces of length 8:

    <... infinite zeros ...>|0 1 0 1 0 1 0 1|0 1 0 1 0 1 0 1|0 1 0 1 0 1 0 1|<... infinite zeros ...>
                                     ^
The eight bits that the robot is in is `0 1 0 1 0 1 0 1`

Converting that to base-10, we get `85`, and that in ASCII is `U`.

Congratulations, you have printed the character `U`.

**Note: Turing Machine But Way Worse doesn't append a trailing newline to the output (printing A and then B would result in AB, not A\nB)**

## Input

Let's say that the input is `hi`.

Taking the ASCII values of these gives us `['01101000', '01101001']`.

Concatenating the list gives us `0110100001101001`.

Therefore, the tape is `<... infinite zeros ...>0 1 1 0 1 0 0 0 0 1 1 0 1 0 0 1<... infinite zeros ...>`.

If there is no input, the tape is `<... infinite zeros ...>0 0 0 0 0 0 0 0<... infinite zeros ...>`.


## Challenge Programs

 - Print "H"
 - Make a cat program
 - Make an infinite loop
 - Output infinite "a"s
