import sys
import os

class TuringMachineButWorse():
    def __init__(self, *args, **kwargs):
        self.neg_tape = []
        self.tape = []
        self.macros = {}
        self.pointer = 0
        self.state = '0'
        self.filename = ""    
        self.lookup = {}
        self.lineCounter = 0
        self.currentLine = ""
        self.blockComment = False
        
    def launch(self):
        self.getTMW()
        self.getTape()
        self.parseTMW()
        self.run()

    def getTMW(self):
        try:
            self.filename = sys.argv[1]
        except:
            exit("Error: no .tmw file has been provided")
        if not os.path.isfile(self.filename):    #check if file exists    
            exit("File '{}' does not exist".format(self.filename))

    def getTape(self):
        tapeFilename = ""
        if not sys.stdin.isatty():      # try to read self.tape from piped stdin
            self.tape = list(map(ord, sys.stdin.read()))
            if self.tape[0] == 65279:       # remove BOM if present
                self.tape = self.tape[1:]
        else:                           # else try to read tape from file
            try:
                tapeFilename = sys.argv[2]
                with open(tapeFilename, "r") as file:
                    self.tape = list(map(ord, file.read()))
            except:
                if tapeFilename != "":
                    exit("Tape file '{}' does not exist or is corrupt".format(tapeFilename))
                    
    def parseTMW(self):
        try:
            with open(self.filename, "r") as file:
                self.currentLine = file.readline()
                while self.currentLine:
                    self.lineCounter += 1
                    self.checkForMacro(file)
                    if self.currentLine:
                        self.setLine(self.currentLine)
                        self.currentLine = file.readline()       # read next line
                    
        except: 
            exit("Error while parsing file '{}'".format(self.filename))
        
    def setLine(self, line):
        if line[0:2] == "/*":                       # allow block comments
            self.blockComment = True
            return
        if line[0:2] == "*/":
            self.blockComment = False
            return
        if line.strip() == "" or line[0] == "#" or line[0:2] == "//" or self.blockComment: #ignore blank lines and comments
            return
        i = [int(x) if (j!=1 and j!=4 and j<7) else x for j,x in enumerate(line.split())]
        if len(i) != 7:
            raise Exception("Expected 7 fields, found %s" % len(i))
        if i[0] != 0 and i[0] != 1:
            raise Exception("Invalid tape current value %s, expected 0 or 1" % i[0])
        if i[2] != 0 and i[2] != 1:
            raise Exception("Invalid tape next value %s, expected 0 or 1" % i[2])
        if i[3] != 0 and i[3] != 1:
            raise Exception("Invalid movement direction %s, expected 0 (left) or 1 (right)" % i[3])
        self.lookup[(i[0], str(i[1]))] = tuple(i[2:])       #add dictionary entry

    def run(self):
        while True:
            debug_tape = "".join(map(lambda c: bin(256 | c)[3:], self.neg_tape[::-1])) + "".join(map(lambda c: bin(256 | c)[3:], self.tape))
            debug_pointer = self.pointer + len(self.neg_tape) * 8
            index = self.pointer // 8
            # when pointer = 0 and value is 1, current character is 1XXX XXXX. current character >> 7 = 1. 0 % 8 = 0. 7 - 0 = 7
            # when pointer = 7 and value is 1, current character is XXXX XXX1. current character >> 0 = 1. 7 % 8 = 7. 7 - 7 = 0
            # so that's why we use 7 - (self.pointer % 8)
            if index >= 0:
                if index >= len(self.tape):
                    self.tape += [0]
            elif -index > len(self.neg_tape):
                self.neg_tape += [0]
            value = (self.tape[index] if index >= 0 else self.neg_tape[~index]) >> (7 - self.pointer % 8) & 1
            if not (value, self.state) in self.lookup:
                debug_tape = "".join(map(lambda c: bin(256 | c)[3:], self.neg_tape[::-1])) + "".join(map(lambda c: bin(256 | c)[3:], self.tape))
                debug_pointer = self.pointer + len(self.neg_tape) * 8
                raise Exception("Value and state (%s, %s) not in ruleset.\nCurrent index: %s\nCurrent tape:\n%s[%s]%s" % (
                    value, self.state, self.pointer, debug_tape[:debug_pointer], debug_tape[debug_pointer], debug_tape[debug_pointer + 1:]
                ))
            next_value, move, self.state, do_print, do_halt = self.lookup[(value, self.state)]
            if next_value != value:
                if index >= 0:
                    self.tape[index] = (self.tape[index] & 0xFF ^ (1 << (7 - self.pointer % 8))) | next_value << (7 - self.pointer % 8)
                else:
                    self.neg_tape[~index] = (self.neg_tape[~index] & 0xFF ^ (1 << (7 - self.pointer % 8))) | next_value << (7 - self.pointer % 8)
            self.pointer += 1 if move else -1
            if do_print:
                if index >= 0:
                    sys.stdout.write(chr(self.tape[index]))
                else:
                    sys.stdout.write(chr(self.neg_tape[~index]))
            if do_halt:
                break
            # print(debug_tape,debug_pointer,sep='\n')
            
    def checkForMacro(self, file):
        if self.currentLine[0:3] == "def": 
            i = self.currentLine.split()
            if(len(i) !=  2):
                exit("Syntax error: Illegal macro definition at line {}".format(self.lineCounter))
            name = i[1]
            macro = []
            self.currentLine = file.readline()
            while self.currentLine[0:3] != "end":
                macro.append(self.currentLine)
                self.currentLine = file.readline()
                self.lineCounter += 1
                
            self.macros[name] = macro
            if self.currentLine:
                self.currentLine = file.readline()
                self.lineCounter += 1
        
        if self.currentLine[0:3] == "use":
            i = self.currentLine.split()
            if(len(i) !=  2):
                exit("Syntax error: Illegal macro definition at line {}".format(self.lineCounter))
            name = i[1]
            try:
                macro = self.macros[name]
            except:
                exit("Syntax error: Macro '{}' has not been defined".format(name))
            for line in macro:
                self.setLine(line)
            if self.currentLine:
                self.currentLine = file.readline()
                self.lineCounter += 1                
        
            
    
if __name__ == "__main__":
    tmw = TuringMachineButWorse()
    tmw.launch()