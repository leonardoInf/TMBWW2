import sys
import os

neg_tape = []
tape = []
pointer = 0
state = '0'
filename = ""

try:
    filename = sys.argv[1]
except:
    exit("Error: no .tmw file has been provided")

if not sys.stdin.isatty():      # try to read tape from piped stdin
    tape = list(map(ord, sys.stdin.read()))
    if tape[0] == 65279:       # remove BOM if present
        tape = tape[1:]
else:                           # else try to read tape from file
    try:
        tapeFilename = sys.argv[2]
        with open(tapeFilename, "r") as file:
            tape = list(map(ord, file.read()))
    except:
        if tapeFilename != "":
            exit("Tape file '{}' does not exist or is corrupt".format(tapeFilename))
    
lookup = {}
if os.path.isfile(filename):    #check if file exists
    try:   
        with open(filename, "r") as file:
            s = file.readline()
            while s:
                i = list(s.split())
                i[0], i[2], i[3], i[5], i[6] =  int(i[0]), int(i[2]), int(i[3]), int(i[5]), int(i[6])
                if len(i) != 7:
                    raise Exception("Expected 7 fields, found %s" % len(i))
                if i[0] != 0 and i[0] != 1:
                    raise Exception("Invalid tape current value %s, expected 0 or 1" % i[0])
                if i[2] != 0 and i[2] != 1:
                    raise Exception("Invalid tape next value %s, expected 0 or 1" % i[2])
                if i[3] != 0 and i[3] != 1:
                    raise Exception("Invalid movement direction %s, expected 0 (left) or 1 (right)" % i[3])
                lookup[(i[0], str(i[1]))] = tuple(i[2:])
                s = file.readline()
    except:
        exit("Could not read file '{}'".format(filename))
else:
        exit("File '{}' does not exist".format(filename))

while True:
    debug_tape = "".join(map(lambda c: bin(256 | c)[3:], neg_tape[::-1])) + "".join(map(lambda c: bin(256 | c)[3:], tape))
    debug_pointer = pointer + len(neg_tape) * 8
    index = pointer // 8
    # when pointer = 0 and value is 1, current character is 1XXX XXXX. current character >> 7 = 1. 0 % 8 = 0. 7 - 0 = 7
    # when pointer = 7 and value is 1, current character is XXXX XXX1. current character >> 0 = 1. 7 % 8 = 7. 7 - 7 = 0
    # so that's why we use 7 - (pointer % 8)
    if index >= 0:
        if index >= len(tape):
            tape += [0]
    elif -index > len(neg_tape):
        neg_tape += [0]
    value = (tape[index] if index >= 0 else neg_tape[~index]) >> (7 - pointer % 8) & 1
    if not (value, state) in lookup:
        debug_tape = "".join(map(lambda c: bin(256 | c)[3:], neg_tape[::-1])) + "".join(map(lambda c: bin(256 | c)[3:], tape))
        debug_pointer = pointer + len(neg_tape) * 8
        raise Exception("Value and state (%s, %s) not in ruleset.\nCurrent index: %s\nCurrent tape:\n%s[%s]%s" % (
            value, state, pointer, debug_tape[:debug_pointer], debug_tape[debug_pointer], debug_tape[debug_pointer + 1:]
        ))
    next_value, move, state, do_print, do_halt = lookup[(value, state)]
    if next_value != value:
        if index >= 0:
            tape[index] = (tape[index] & 0xFF ^ (1 << (7 - pointer % 8))) | next_value << (7 - pointer % 8)
        else:
            neg_tape[~index] = (neg_tape[~index] & 0xFF ^ (1 << (7 - pointer % 8))) | next_value << (7 - pointer % 8)
    pointer += 1 if move else -1
    if do_print:
        if index >= 0:
            sys.stdout.write(chr(tape[index]))
        else:
            sys.stdout.write(chr(neg_tape[~index]))
    if do_halt:
        break
    # print(debug_tape,debug_pointer,sep='\n')