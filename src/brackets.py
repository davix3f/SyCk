import re
import linecache
import syckIO
filename=""
class Bracket:

    def __init__(self, code, type, line, column, starts=None, ends = None):

            self.code = code
            self.type = type
            self.line = line
            self.column = column
            self.all = ("Code: %s\nType: %s\nLine: %s\nColumn: %s\n" %(code,type,line,column))

found = { "open":{}, "closed":{} }

length = 0


def BracketFinder(output_log = 0):
    selected_line = 1
    num_open = 0
    num_close = 0
    while selected_line <= syckIO.file_length(filename):

        match_open = re.search(r"{", linecache.getline(filename, selected_line))

        match_close = re.search(r"}", linecache.getline(filename, selected_line))

        if match_open != None:
            if output_log == 1:
                print("0--", match_open)
            if output_log == 1:
                print("b{0}o=Bracket(b{0}o, curly, line:{1}, column:{2}\n".format(num_open,selected_line, match_open.span()[1]))
            exec("b{0}o=Bracket(\"b{0}o\", \"curly\", {1}, {2}); found[\"open\"][b{0}o.code]=b{0}o".format(num_open,selected_line, match_open.span()[1]))
            num_open+=1


        if match_close != None:
            if output_log == 1:
                print("--0", match_close)
            if output_log == 1:
                print("b{0}c=Bracket(b{0}c, curly, line:{1}, column:{2}\n".format(num_close, selected_line, match_close.span()[1]))
            exec("b{0}c=Bracket(\"b{0}c\", \"curly\", {1}, {2}); found[\"closed\"][b{0}c.code]=b{0}c".format(num_close, selected_line, match_close.span()[1]))
            num_close+=1

        linecache.clearcache()
        selected_line += 1
    return(num_open, num_close)
