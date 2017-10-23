import re
import cpp
from linecache import *

class Bracket:

    def __init__(self, code, type, line, column):

            self.code = code
            self.type = type
            self.line = line
            self.column = column
            self.all = ("Code: %s\nType: %s\nLine: %s\nColumn: %s" %(code,type,line,column))

found={"open":{}, "closed":{}}

length = 0

f = open("testfile","r")
for line in f:
    length+=1

def BracketFinder():
    selected_line=1
    num_open=0
    num_close=0
    while selected_line <= length:
        #print(selected_line)
        match_open=re.search(r"{", getline("testfile",selected_line))

        match_close=re.search(r"}", getline("testfile",selected_line))
        #print("{",match_open)
        #print("}",match_close)

        if (match_open != None) == True:
            print("0--", match_open)
            print("b{0}o=Bracket(b{0}o, curly, line:{1}, column:{2}\n".format(num_open,selected_line, match_open.span()[1]))
            exec("b{0}o=Bracket(\"b{0}o\", \"curly\", {1}, {2}); found[\"open\"][b{0}o.code]=b{0}o".format(num_open,selected_line, match_open.span()[1]))
            num_open+=1


        if (match_close != None) == True:
            print("--0", match_close)
            print("b{0}c=Bracket(b{0}c, curly, line:{1}, column:{2}\n".format(num_close,selected_line, match_close.span()[1]))
            exec("b{0}c=Bracket(\"b{0}c\", \"curly\", {1}, {2}); found[\"closed\"][b{0}c.code]=b{0}c".format(num_close,selected_line, match_close.span()[1]))
            num_close+=1

        clearcache()
        selected_line+=1
