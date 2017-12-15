import sys
sys.path.append("../Languages")

import re
import syckIO
import brackets
import argparse


#######CLI design
parser = argparse.ArgumentParser()
parser.add_argument("language",  help="Load language")
parser.add_argument("--loop", "-l", help="execute loop_detector", action="store_true")
parser.add_argument("--function", "-f", help="execute function_detector", action="store_true")

arguments=parser.parse_args()

if arguments.language:
    language_str=arguments.language
    try:
        exec("import %s" %language_str)
        print("-- %s language successfully loaded --"%arguments.language.upper())
    except ImportError:
        print("The language module %s has not been found in SyCk/Languages" %language_str)
        exit()
    exec("language=%s" %language_str) #language=[language chosen in cli command]
#######

for item in language.lang_classes:
    print(item)
print("\n")

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

    loop_l=[]
    function_l=[]
    closed=[]

    def loop_list():
        loops=["switch", "for_loop", "dowhile", "while_loop"]
        for item in loops:
            for i,d in enumerate(Elements.constructs[item]):
                Elements.loop_l.append(Elements.constructs[item][d].dect_at)
        Elements.loop_l.sort()
        print(Elements.loop_l)

    def function_list():
        for i,d in enumerate(Elements.constructs["function"]):
            Elements.function_l.append(Elements.constructs["function"][d].start)
        Elements.function_l.sort()
        print(Elements.function_l)


    parent = []
    parent_structure = []

    counter = {
        "function":0,
        "switch":0,
        "for_loop":0,
        "dowhile":0,
        "while_loop":0 }

    def getElement(kword):
        for element in Elements.constructs[kword]:
            print(element)


brackets.BracketFinder()

def function_detector():
    for item in lines:

        function_match = re.search(language.Function["init_pattern"], lines[item])
        if function_match: #if found a line matching the <type> <function name> ()

            #A new "function" object is created, with name, return type and the LINE DETECTED
            # which is different from the line where the function STARTS
            Elements.constructs["function"][function_match.group("f_name")] = \
                language.FunctionClass(name=function_match.group("f_name"),
                        return_type = function_match.group("return_type"),
                        dect_at = item)
            #The detected class name is appended to the ""parent_function"" list, which is needed for closing detection
            Elements.parent.append(function_match.group("f_name"))
            print("--", function_match.group(3), "is set as parent_function --")
            print(Elements.parent)

            #If the starting { of the function is not in the line where the function is detected, the program sets it to the nearest found
            if re.search(r"\{" , function_match.group(0)) == None:
                print("-- Function", function_match.group(3), "not starting at", item, "\b!")
                lst = []
                for i, _ in enumerate(brackets.found["open"]):
                    lst.append(brackets.found["open"]["b{0}o".format(i)].line)
                    #                                                                  b{0}o i=2  -> b2o
                lst.sort()

                def nearest_start(list=lst):
                    for i, d in enumerate(lst):
                        if d > item:
                            print(brackets.found["open"]["b%so"%i].code,
                                "[foundlist item", i,  "located at line "+str(d)+"]",
                                "is starting", function_match.group(3), "\n")
                            return(d)
                #Assigning to the nearest
                exec("Elements.constructs[\"function\"][\"%s\"].start=%s" %(function_match.group(3), nearest_start()) )

            else:        # belongs to if: function_match
                #But if the starting { is found in the same line of function detection, then the start is setted at this line
                print("\nFunction", function_match.group(3), " starting at", item, "\n")
                exec("Elements.constructs[\"function\"][\"%s\"].start=%s" %(function_match.group(3), item) )

def loop_detector(): #this one work fancily better
    for item in lines:
        try:
            #Here we instatiate and organize loops like for0,for1, while0, ect.
            #Let's put we find a 'For' loop. The classified output has to be 'for0' (if it's the first for found)
            if language.finder(lines[item], True)[0] == True:
                kind = language.finder(lines[item])[1].lower()  # 'For' --> 'for'
                print(kind)
                if kind != "function":
                    kind_code = kind+str(Elements.counter[str(kind)]) #kind_code = 'for'+the its number
                    print(item, lines[item].replace("\t","").replace("\n","")) #log
                    print("Code is %s" %kind_code) #log
                    Elements.counter[str(kind)]+=1 #Update the 'for' counter
                    exec("{0}=language.{1}({2}, \"{0}\")".format(kind_code,
                        kind.title().replace("_Loop","").replace("while", "While")+"Class",
                        item) )
                    #^ for0=language.ForClass(line_where_for_is_detected, for0)
                    exec("Elements.constructs[\"{0}\"][\"{1}\"]={1}".format(kind, kind_code) )
                    Elements.parent.append(kind_code)
                    #^ add the new for0 class to our Elements.constructd["for_loop"]
                    print("\n")
        except TypeError:
            pass


if arguments.loop:
    print("Using %s language module..\n" %language)
    loop_detector()

if arguments.function:
    print("Using %s language module..\n" %language)
    function_detector()
