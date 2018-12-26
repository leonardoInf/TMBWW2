import sys

tape = []
pointer = 0
state = 0

if not sys.stdin.isatty():
	for i in sys.stdin.read():
		tape += list(map(int, "0" * (8 - len(bin(ord(i))[2:])) + bin(ord(i))[2:]))
tape = tape or [0 for i in range(8)]
length = len(tape)

lookup = {}
with open(sys.argv[1], "r") as file:
	s = file.readline()
	while s:
		i = list(map(int, s.split()))
		if len(i) != 7:
			raise Exception("Expected 7 fields, found %s" % len(i))
		if i[0] != 0 and i[0] != 1:
			raise Exception("Invalid tape current value %s, expected 0 or 1" % i[0])
		if i[2] != 0 and i[2] != 1:
			raise Exception("Invalid tape next value %s, expected 0 or 1" % i[2])
		if i[3] != 0 and i[3] != 1:
			raise Exception("Invalid movement direction %s, expected 0 (left) or 1 (right)" % i[3])
		lookup[(i[0], i[1])] = tuple(i[2:])
		s = file.readline()

while True:
	if not (tape[pointer], state) in lookup:
		raise Exception("Value and state (%s, %s) not in ruleset" % (tape[pointer], state))
	tape[pointer], move, state, do_print, do_halt = lookup[(tape[pointer], state)]
	pointer = (pointer + (1 if move else -1) + length) % length
	if do_print:
		for j in range(0, len(tape), 8):
			if any(tape[j:j+8]):
				c = 0
				for i in range(j, j + 8):
					c <<= 1
					c += tape[i]
				sys.stdout.write(chr(c))
	if do_halt:
		break
