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

    <... infinite zeros ...> 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 <... infinite zeros ...>
                                     ^
and you decide to print.

First, the program would seperate the tape into seperate pieces of length 8:

    <... infinite zeros ...>|0 1 0 1 0 1 0 1|0 1 0 1 0 1 0 1 0|1 0 1 0 1 0 1 0|<... infinite zeros ...>
                                     ^
The eight bits that the robot is in is `0 1 0 1 0 1 0 1`

Converting that to base-10, we get `85`, and that in ASCII is `U`.

Congratulations, you have printed the character `U`.

NOTE: TURING MACHINE BUT WAY WORSE DOESN'T APPEND A TRAILING NEWLINE 


--TO BE CONTINUED--
