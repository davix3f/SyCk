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

    function_attributes = ["name", "return_type", "extension", "args", "nested"]

    def getElements(kword):
        for element in Elements.constructs[kword]:
            print(element)

    parent = []

brackets.BracketFinder()

def function_detector():


    for item in lines:

        function_match = re.search(cpp.Function["init_pattern"], lines[item])


        if function_match:

            #print("Matching: ", lines[item])

            Elements.constructs["functions"][function_match.group("f_name")] = \
                cpp.FunctionClass(name=function_match.group("f_name"),
                        return_type = function_match.group("return_type"),
                        start = item)
            Elements.parent.append(function_match.group("f_name"))

            if re.search(r'\{' , function_match.group(0)) == None:
                print("Function", function_match.group(3), "not starting at", item)
                lst = []
                for i, _ in enumerate(brackets.found["open"]):
                    lst.append(brackets.found["open"]["b{0}o".format(i)].line)
                lst.sort()

                def nearest(list=lst):
                    for i, d in enumerate(lst):
                        if list[i] > item:
                            print("Item", i,  "("+str(lst[i])+")", "is starting", function_match.group(3))
                            return(list[i])

                print("Set Function", function_match.group(3), " start at line", lst[i], ": exec(Elements.constructs[\'functions\'][%s].start=%s)\n" %(function_match.group(3), nearest()) )


            else:
                print("Function", function_match.group(3), " starting at", item, "\n")
