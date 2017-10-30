import re, cpp, syckIO, brackets

from linecache import *

testfile = "testfile"

for item in cpp.lang_classes:
    print(item)


lines = syckIO.lines

syckIO.reader()

class Elements:

    constructs = {
        "functions" : {},
        "switch" : {},
        "if" : {},
        "for" : {},
        "do_while" : {}
    }

    function_attributes = ["name", "return_type", "extension", "args", "nested"]

    last_parent = None

brackets.BracketFinder()

def function_detector():


    for item in lines:

        function_match = re.search(cpp.Function["init_pattern"], lines[item])

        if function_match:

            print("Matching: ", lines[item])

            Elements.constructs["functions"][function_match.group("f_name")] = \
                cpp.FunctionClass(name = function_match.group("f_name"),
                return_type = function_match.group("return_type"),
                extension = (item, None))
            Elements.last_parent = function_match.group("f_name")

            if re.search( r'\{' , function_match.group(0)) == None:
                print("Function",function_match.group(3), "not starting at", item)
                lst = []
                for i, _ in enumerate(brackets.found["open"]):
                    lst.append(brackets.found["open"]["b{0}o".format(i)].line)
                lst.sort()
                print(lst)

                def nearest(list = lst):
                    for i, d in enumerate(lst):
                        if lst[i] > item:
                            #print("Item", i,  "("+str(lst[i])+")", "is littler than", item)
                            print("Item", i,  "("+str(lst[i])+")", "is starting", item)
                            return(None)
                    #print("Item", i, "("+str(lst[i])+")", "bigger than", item)

                #print("Nearest item to line", item, "is bracket on line", lst[0])
                nearest()
                #print("Set Function", function_match.group(3), " start at line", lst[0], ": exec(Elements.constructs[\'functions\'][\'main\'].extension=%s)" % lst[0] )

            else:
                print("Function", function_match.group(3), " starting at", item)
