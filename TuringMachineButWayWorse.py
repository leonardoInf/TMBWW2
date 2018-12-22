import sys

tape = []
pointer = 0
state = '0'

if sys.stdin.isatty():
	tape = ['0' for i in range(8)]
else:
	for i in sys.stdin.read():
		tape.extend(list("0" * (8 - len(bin(ord(i))[2:])) + bin(ord(i))[2:]))

ins = open(sys.argv[1], 'r').readlines()                                                                               
curval = [] 
curstate = []
replace = []
move = []
gostate = []
pri = []
halt = []

for i in ins:
	j = i.split()
	curval.append(j[0])
	curstate.append(j[1])
	replace.append(j[2])
	move.append(j[3])
	gostate.append(j[4])
	pri.append(j[5])
	halt.append(j[6])

while True:
	for i in ins:
		if tape[pointer] == i.split()[0] and state == i.split()[1]:
			# print(i.replace("\n", ""))
			tape[pointer] = i.split()[2]
			if pointer == 0 and i.split()[3] == '0':
				pointer = len(tape) - 1
			elif pointer == len(tape) - 1 and i.split()[3] == '1':
				pointer = 0
			elif i.split()[3] == '1':
				pointer += 1
			elif i.split()[3] == '0':
				pointer -= 1
				
			state = i.split()[4]
			if i.split()[5] == '1':
				for j in range(0, len(tape), 8):
					if "".join(tape[j:(j+8)]) != "0" * 8:
						sys.stdout.write(chr(int("".join(tape[j:(j+8)]), 2)))
			if i.split()[6] == '1':
				sys.exit(1)
			# print(tape)
			# print(pointer)
				