import sys
import os

#TODO: allow multiple choice for one single state in macros

class TuringMachineButWorse():
    def __init__(self, *args, **kwargs):
        self.neg_tape = []
        self.tape = []
        self.includedLines = []
        self.includeIndex = 0
        self.macros = {}
        self.pointer = 0
        self.state = '0'
        self.filename = ""    
        self.filename2 = ""    
        self.lookup = {}
        self.lineCounter = 0
        self.currentLine = ""
        self.blockComment = False
    
    def __del__(self): 
        os.remove(self.filename2)    #remove temp file 

        
    def launch(self):
        self.getTMW()
        self.getTape()
        self.preProcess()
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

    def retrieveIncludes(self):
        self.filename2 = "temp" + self.filename
        with open(self.filename2, "w") as fobj:
            for line in self.includedLines:
                fobj.write(line)
            with open(self.filename, "r") as fobj2:
                fobj2.readline()        # skip the line which features the include
                fobj.write("\n")        # add newline
                fobj.write(fobj2.read())
                
    def parseTMW(self):
        #try:
            self.retrieveIncludes()
            with open(self.filename2, "r") as file:
                self.currentLine = file.readline()
                while self.currentLine:
                    self.lineCounter += 1
                    self.checkForMacro(file)
                    if self.currentLine:
                        self.setLine(self.currentLine)
                        self.currentLine = file.readline()       # read next line           
        #except: 
            #exit("Error while parsing")
            
    def getLine(self, file):
        if file == 0:
            if self.includeIndex < len(self.includedLines):
                self.currentLine = self.includedLines[self.includeIndex]
                self.includeIndex += 1
        else:
            self.currentLine = file.readline()
        self.lineCounter += 1
        #print("Got: {}".format(self.currentLine))
        
    def setLine(self, line):
        print("Adding the following line: {}".format(line))
        if line[:7] == "include" or line[:3] == "def" or line[:3] == "end":
            return
        if line[:2] == "/*":                       # allow block comments
            self.blockComment = True
            return
        if line[:2] == "*/":
            self.blockComment = False
            return
        if line.strip() == "" or line[0] == "#" or line[0:2] == "//" or self.blockComment: #ignore blank lines and comments
            return
        i = [int(x) if (j!=1 and j!=4) else x for j,x in enumerate(line.split()[:7])]
        if len(i) != 7:
            #print(i)
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
            if(len(i) < 2 or len(i) > 5):
                exit("Syntax error: Illegal macro definition at line {}".format(self.lineCounter))
            macro = []
            name = i[1]
            begin = -1
            end = -1
            formal_marg  = ""
            if len(i) >= 4:
                begin = i[2]
                end = i[3]
                if len(i) == 5:
                    formal_marg = i[4]
            elif len(i) == 3:
                formal_marg = i[2]
            
            self.getLine(file)          #current line is in self.currentLine
            
            
            while self.currentLine[0:3] != "end":
                macro.append(self.currentLine)
                self.getLine(file)
                
            self.macros[name] = (macro, (begin, end, formal_marg))
            #print("Macro {} has been added: {}".format(name, self.macros[name]))
            
            if self.currentLine:        #move on to next line if there are any
                self.getLine(file)
                if self.currentLine[0:3] == "def" or self.currentLine[0:3] == "use":
                    self.checkForMacro(file)
        
        if self.currentLine[0:3] == "use":
            i = self.currentLine.split()
            if len(i) <  2 or len(i) > 5:
                exit("Syntax error: Illegal macro definition at line {}".format(self.lineCounter))
            name = i[1]
            marg = ""
            margs = ()
            if len(i) == 3:
                marg = i[2]
                margs = (-1,-1,-1)
            if len(i) == 4:
                margs = (i[2], i[3], 1)
            elif len(i) == 5:
                margs = (i[2], i[3], i[4])
                marg = margs[2]
            try:
                m = self.macros[name]
                macro_len = len(m[0])
            except:
                exit("Syntax error: Macro '{}' has not been defined".format(name))
            for i,l in enumerate(m[0]):
                line = ""
                #print(margs[2])
                if m[1][2] != "" and not marg:
                    #print("formal: {}, tatsächlich: {}".format(m[1], marg))
                    exit("Syntax error: Argument for Macro {} has not been provided".format(name))
                if marg != margs[2]:
                    if marg[0] == "|":
                        marg = marg[1:]
                        line = self.insertSingleMacroArg(l, m[1][2], marg, i==0)
                    else:
                        line = self.insertSingleIndex(l, m[1][2], marg, i==0)
                        
                elif len(margs) == 2:
                    line = self.insertMacroArgWithoutVal(l, m[1], margs, macro_len, i==0)
                        
                elif len(margs) == 3:
                    line = self.insertMacroArg(l, m[1], margs, macro_len, i==0)
                        
                else:       #keine margs
                    line = l
                self.setLine(line)
            
            if self.currentLine:
                self.getLine(file)
                if self.currentLine[0:3] == "def" or self.currentLine[0:3] == "use":
                    self.checkForMacro(file)
                    
    def preProcess(self):
        with open(self.filename, "r") as file:
            self.currentLine = file.readline()
            while self.currentLine:
                if self.currentLine != " ":
                    i = self.currentLine.split()
                    if i:
                        if i[0] == "include":
                            if len(i) != 2:
                                exit("Syntax error: Illegal include directive at line {}".format(self.lineCounter))
                            if not os.path.isfile(i[1]):
                                exit("Include error: File '{}' could not be found".format(i[1]))
                            with open(i[1], "r") as file2:
                                self.currentLine = file2.readline()
                                while self.currentLine:
                                    self.includedLines.append(self.currentLine)
                                    self.currentLine = file2.readline()
                        self.currentLine = file.readline()
                        self.lineCounter += 1
                
        self.currentLine = ""
        self.lineCounter = 0
     
    macroIndexCounter = 0 
    def insertMacroArg(self, in_, formal_list, mArg_list, macro_len, new_macro=False):
        splitLine = in_.split()
        
        if new_macro:                       
            self.macroIndexCounter = 0
        for i in range(2):                         #set marg indices = formal_list[0:2]
             occurences = [j for j,x in enumerate(splitLine) if x == formal_list[i]]
             for j in occurences:
                index_val = self.convert_to_index(mArg_list[0])
                if i == 0:                          #the first index gets incremented while the second does not
                    index_val += self.macroIndexCounter
                if i == 1:
                    if self.macroIndexCounter == macro_len-1:
                        index_val = self.convert_to_index(mArg_list[1])
                    else:
                        index_val += self.macroIndexCounter + 1
                #print(index_val)
                splitLine[j] = self.convert_to_char(index_val) 
        
        binaryMArg = bin(ord(mArg_list[2]))[2:]      #set marg value = formal_list[2]
        while len(binaryMArg) < 8:      #add preceding zeroes to make one byte
            binaryMArg = "0" + binaryMArg
        occurences = [j for j,x in enumerate(splitLine) if x == formal_list[2]] #list comprehension
        for j in occurences:
            splitLine[j] = binaryMArg[self.macroIndexCounter]
            
        
        self.macroIndexCounter += 1
        return " ".join(splitLine)
       
    
    withoutValCounter = 0
    def insertMacroArgWithoutVal(self, in_, formal_list, indices_list, macro_len, new_macro=False):
        splitLine = in_.split()
        
        if new_macro:                       
            self.withoutValCounter = 0
        for i in range(2):                         #set marg indices = formal_list[0:2]
            occurences = [j for j,x in enumerate(splitLine) if x == formal_list[i]]
            for j in occurences:
                index_val = self.convert_to_index(indices_list[0])
                if i == 0:                          #the first index gets incremented while the second does not
                    index_val += self.withoutValCounter
                if i == 1:
                    if self.macroIndexCounter == macro_len-1:
                        index_val = self.convert_to_index(indices_list[1])
                    else:
                        index_val += self.withoutValCounter + 1
                #print(index_val)
                splitLine[j] = self.convert_to_char(index_val)
            self.withoutValCounter += 1
        return " ".join(splitLine)
    
    singleMacroIndexCounter = 0
    def insertSingleMacroArg(self, in_, formal, mArg, new_macro=False):
        if new_macro:
            self.singleMacroIndexCounter = 0
    
        splitLine = in_.split() 
        binaryMArg = bin(ord(mArg))[2:]      #set marg value = formal_list[2]
        while len(binaryMArg) < 8:      #add preceding zeroes to make one byte
            binaryMArg = "0" + binaryMArg
        occurences = [j for j,x in enumerate(splitLine) if x == formal] #list comprehension
        for j in occurences:
            splitLine[j] = binaryMArg[self.singleMacroIndexCounter]
            
        self.singleMacroIndexCounter += 1
        return " ".join(splitLine)
        
    singleIndexCounter = 0
    def insertSingleIndex(self, in_, formal, index, new_macro=False):
        splitLine = in_.split()
        if new_macro:                       
            self.singleIndexCounter = 0
        occurences = [j for j,x in enumerate(splitLine) if x == formal]
        for j in occurences:
            splitLine[j] = self.convert_to_char(self.convert_to_index(index) + self.singleIndexCounter)
        self.singleIndexCounter += 1
        return " ".join(splitLine)
        
        
    def convert_to_index(self, char):
        val = 0
        if char.isdigit():
            val = int(char)
        else:                               
            val = ord(char)-87    # convert letters to indices, a = 10
        return val
    
    def convert_to_char(self, num):
        if num <= 9:
            return str(num)
        return chr(num+87)
        
    
if __name__ == "__main__":
    tmw = TuringMachineButWorse()
    tmw.launch()