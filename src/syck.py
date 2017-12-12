import re, cpp, syckIO, brackets

testfile = "testfile"

for item in cpp.lang_classes:
    print(item)

lines = syckIO.lines
syckIO.reader()

class Elements:

    constructs = {
        "function" : {},
        "switch" : {},
        "if" : {},
        "for_loop" : {},
        "dowhile" : {},
        "while_loop" : {}
    }

    parent_function = []
    parent_structure = []

    counter = {
        "function":0,
        "switch":0,
        "for_loop":0,
        "dowhile":0,
        "while_loop":0 }
    function_attributes = ["name", "return_type", "extension", "args", "nested"]
    def getElement(kword):
        for element in Elements.constructs[kword]:
            print(element)


brackets.BracketFinder()

def function_detector():
    for item in lines:

        function_match = re.search(cpp.Function["init_pattern"], lines[item])
        if function_match: #if found a line matching the <type> <function name> ()

            #A new ""function"" object is created, with name, return type and the LINE DETECTED
            # which is different from the line where the function STARTS
            Elements.constructs["function"][function_match.group("f_name")] = \
                cpp.FunctionClass(name=function_match.group("f_name"),
                        return_type = function_match.group("return_type"),
                        dect_at = item)
            #The detected class name is appended to the ""parent_function"" list, which is needed for closing detection
            Elements.parent_function.append(function_match.group("f_name"))
            print("--", function_match.group(3), "is set as parent_function --")
            print(Elements.parent_function)

            #If the starting { of the function is not in the line where the function is detected, the program sets it to the nearest found
            if re.search(r"\{" , function_match.group(0)) == None:
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
                exec("Elements.constructs[\"function\"][\"%s\"].start=%s" %(function_match.group(3), nearest()) )

            else:        # belongs to if: function_match
                #But if the starting { is found in the same line of function detection, then the start is setted at this line
                print("\nFunction", function_match.group(3), " starting at", item, "\n")
                exec("Elements.constructs[\"function\"][\"%s\"].start=%s" %(function_match.group(3), item) )

def loop_detector(): #this one work fancily better
    for item in lines:
        try:
            #Here we instatiate and organize loops like for0,for1, while0, ect.
            #Let's put we find a 'For' loop. The classified output has to be 'for0' (if it's the first for found)
            if cpp.finder(lines[item], True)[0] == True:
                kind = cpp.finder(lines[item])[1].lower()  # 'For' --> 'for'
                if kind != "function":
                    kind_code = kind+str(Elements.counter[str(kind)]) #kind_code = 'for'+the its number
                    print(item, lines[item].replace("\t","").replace("\n","")) #log
                    print("Code is %s" %kind_code) #log
                    Elements.counter[str(kind)]+=1 #Update the 'for' counter
                    exec("{0}=cpp.{1}({2}, \"{0}\")".format(kind_code, kind.title().replace("_Loop","Class"), item) )
                    #^ for0=cpp.ForClass(line_where_for_is_detected, for0)
                    exec("Elements.constructs[\"{0}\"][\"{1}\"]={1}".format(kind, kind_code) )
                    #^ add the new for0 class to our Elements.constructd["for_loop"]
                    print("\n")
        except TypeError:
            pass
