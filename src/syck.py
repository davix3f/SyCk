import re, cpp, syckIO, brackets

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
    parent = []
    function_attributes = ["name", "return_type", "extension", "args", "nested"]

    def getElement(kword):
        for element in Elements.constructs[kword]:
            print(element)


brackets.BracketFinder()

def function_detector():
    for item in lines:

        function_match = re.search(cpp.Function["init_pattern"], lines[item])
        if function_match: #if found a line matching the <type> <function name> ()

            #A new ''function'' object is created, with name, return type and the LINE DETECTED
            # which is different from the line where the function STARTS
            Elements.constructs["functions"][function_match.group("f_name")] = \
                cpp.FunctionClass(name=function_match.group("f_name"),
                        return_type = function_match.group("return_type"),
                        dect_at = item)
            #The detected class name is appended to the ''parent'' list, which is needed for closing detection
            Elements.parent.append(function_match.group("f_name"))
            print("--", function_match.group(3), "is set as parent --")
            print(Elements.parent)

            #If the starting { of the function is not in the line where the function is detected, the program sets it to the nearest found
            if re.search(r'\{' , function_match.group(0)) == None:
                print("-- Function", function_match.group(3), "not starting at", item, "\b!")
                lst = []
                for i, _ in enumerate(brackets.found["open"]):
                    lst.append(brackets.found["open"]["b{0}o".format(i)].line)
                lst.sort()

                def nearest(list=lst):
                    for i, d in enumerate(lst):
                        if d > item:
                            print(brackets.found["open"]["b%so"%i].code,
                                "[foundlist item", i,  "positioned at line "+str(d)+"]",
                                "is starting", function_match.group(3), "\n")
                            return(d)
                #Assigning to the nearest
                exec("Elements.constructs[\'functions\'][\'%s\'].start=%s" %(function_match.group(3), nearest()) )

            else:        # belongs to if: function_match
                #But if the starting { is found in the same line of function detection, then the start is setted at this line
                print("\nFunction", function_match.group(3), " starting at", item, "\n")

def classbased_detector(): #this one work fancily better
    for item in lines:
            if cpp.finder(lines[item]):
                print(item, lines[item])
