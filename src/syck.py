import sys
sys.path.append("../Languages")

import re
import syckIO
import brackets
import argparse


#######CLI design
parser = argparse.ArgumentParser()
parser.add_argument("language",  help="Load language")
parser.add_argument("--loop", "-l", help="Execute loop_detector", action="store_true")
parser.add_argument("--function", "-f", help="Execute function_detector", action="store_true")
parser.add_argument("--close","-c", help="Try to find where function and loops close", action="store_true")
parser.add_argument("--log", help="Log <on/off> display logs of various functions")

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
brackets.BracketFinder()

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
    closed_l=[]

    def loop_list(explicit_list=False):
        for item in ("switch", "for_loop", "dowhile", "while_loop"):
            for i,d in enumerate(Elements.constructs[item]):
                Elements.loop_l.append( (Elements.constructs[item][d].name,
                Elements.constructs[item][d].dect_at) )
        Elements.loop_l.sort()
        if explicit_list==True:
            print(Elements.loop_l)

    def function_list(explicit_list=False):
        for i,d in enumerate(Elements.constructs["function"]):
            Elements.function_l.append( (Elements.constructs["function"][d].name,
            Elements.constructs["function"][d].start) )
        Elements.function_l.sort()
        if explicit_list==True:
            print(Elements.function_l)

    def closed_list(explicit_list=False):
        for i,d in enumerate(brackets.found["closed"]):
            Elements.closed_l.append(brackets.found["closed"][d].line)
        Elements.closed_l.sort()
        if explicit_list==True:
            print(Elements.closed_l)

    def nearer_closer(list_a, list_b):
        while len(list_a)!=0:
            for item in list_a:
                print("Value:",item[1])
                for i,d in enumerate(list_b):
                    if d>item[1]:
                        print(item[0],"closes at line",d)
                        list_a.pop(0)
                        list_b.remove(d)
                        break

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

#====================================================================
def function_detector(log=False):
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
            if log==True:
                print("--", function_match.group(3), "is set as parent_function --")
                print(Elements.parent)

            #If the starting { of the function is not in the line where the function is detected, the program sets it to the nearest found
            if re.search(r"\{" , function_match.group(0)) == None:

                def function_start():
                    open_l = []
                    for i, _ in enumerate(brackets.found["open"]):
                        open_l.append(brackets.found["open"]["b{0}o".format(i)].line)
                        #                                                                  b{0}o i=2  -> b2o
                    open_l.sort()
                    for i, d in enumerate(open_l):
                        if d > item:
                            if log==True:
                                print(brackets.found["open"]["b%so"%i].code,
                                    "[foundlist item", i,  "located at line "+str(d)+"]",
                                    "is starting", function_match.group(3), "\n")
                            return(d)
                #Assigning to the nearest
                exec("Elements.constructs[\"function\"][\"%s\"].start=%s" %(function_match.group(3), function_start()) )

            else:        # belongs to if: function_match
                #But if the starting { is found in the same line of function detection, then the start is setted at this line
                if log==True:
                    print("\nFunction", function_match.group(3), " starting at", item, "\n")
                exec("Elements.constructs[\"function\"][\"%s\"].start=%s" %(function_match.group(3), item) )

def loop_detector(log=False): #this one work fancily better
    for item in lines:
        try:
            #Here we instatiate and organize loops like for0,for1, while0, ect.
            #Let's put we find a 'For' loop. The classified output has to be 'for0' (if it's the first for found)
            if language.finder(lines[item], log)[0] == True:
                kind = language.finder(lines[item])[1].lower()  # 'For' --> 'for'
                if kind != "function":
                    kind_code = kind+str(Elements.counter[str(kind)]) #kind_code = 'for'+the its number
                    if log==True:
                        print(item, lines[item].replace("\t","").replace("\n","")) #log
                        print("Code is %s\n" %kind_code) #log
                    Elements.counter[str(kind)]+=1 #Update the 'for' counter

                    if language.finder(lines[item])[2]!=True:
                        def loop_start():
                            open_l=[]
                            for i,d in enumerate(brackets.found["open"]):
                                open_l.append(brackets.found["open"][d].line)
                            open_l.sort()
                            for i,d in enumerate(open_l):
                                if d > item:
                                    if log==True:
                                        print(brackets.found["open"]["b%so"%i].code,
                                            "[foundlist item", i,  "located at line "+str(d)+"]",
                                            "is starting", kind_code, "\n")
                                    return(d)

                    exec("{0}=language.{1}({2}, \"{0}\", start={3})".format(kind_code,
                        kind.title().replace("_Loop","").replace("while", "While")+"Class",
                        item,
                        loop_start()) )
                    #^ for0=language.ForClass(line_where_for_is_detected, for0)
                    exec("Elements.constructs[\"{0}\"][\"{1}\"]={1}".format(kind, kind_code) )
                    Elements.parent.append(kind_code)
                    #^ add the new for0 class to our Elements.constructd["for_loop"]
                    if log==True:
                        print("\n")
        except TypeError:
            pass



#    STILL CLI

if arguments.log == "on":
    log=True
elif arguments.log == "off":
    log=False
else:
    #print("%s is not a valid <log> setting. FALSE will be set\n" %arguments.log)
    log=False

if arguments.loop:
    print("Using %s language module..\n" %language)
    loop_detector(log)

if arguments.function:
    print("Using %s language module..\n" %language)
    function_detector(log)

if arguments.close:
    function_detector(log)
    loop_detector(log)
    Elements.function_list()
    Elements.loop_list()
    Elements.closed_list()

    for item in (Elements.loop_l, Elements.function_l):
        Elements.nearer_closer(item, Elements.closed_l)
