#!/usr/bin/env python3

import sys
sys.path.append("../Languages")

import re
import syckIO
import operator
import brackets
import argparse
from time import sleep
from time import ctime


#######CLI design
parser = argparse.ArgumentParser(prog="syck.py")
parser.add_argument("language",  help="Load chosen language")
parser.add_argument("filename", help="File to perform the check", metavar="/docs/main.lang")
parser.add_argument("--loops", "-l", help="Execute loop_detector", action="store_true")
parser.add_argument("--functions", "-f", help="Execute function_detector", action="store_true")
parser.add_argument("--closed","-c", help="Try to find where function and loops close", action="store_true")
parser.add_argument("--log", help="Log <on/off> display logs of various functions", metavar="on|off")

arguments=parser.parse_args()

if arguments.language:
    language_str=arguments.language
    try:
        exec("import %s" %language_str)
        print("\n",ctime(),"\n")
        print("-- %s language successfully loaded --\n"%arguments.language.upper())
    except ImportError:
        print("The language module %s has not been found in SyCk/Languages" %language_str)
        exit()
    exec("language=%s" %language_str) #language=[language chosen in cli command]
    for item in language.lang_classes:
        print(item)

if arguments.filename:
    syckIO.filename=arguments.filename
    brackets.filename=arguments.filename
    print("\nFile:",syckIO.filename,"\n")
elif arguments.filename==None:
    raise ImportError("\'None\' is not a valid file")

#######


lines = syckIO.lines
syckIO.reader()
brackets.BracketFinder()

class Elements:

    constructs = {
        "function" : {},
        "switch" : {},
        "if" : {},
        "else": {},
        "for_loop" : {},
        "dowhile" : {},
        "while_loop" : {}
    }

    loop_l=[]
    function_l=[]
    closed_l=[]

    def loop_list(explicit_list=False):
        Elements.loop_l=[]
        for item in ("switch", "for_loop", "dowhile", "while_loop", "if", "else"):
            for i,d in enumerate(Elements.constructs[item]):
                Elements.loop_l.append( (Elements.constructs[item][d].name,
                                                                Elements.constructs[item][d].start) )
                                                                
        Elements.loop_l=sorted(Elements.loop_l, key=operator.itemgetter(1))
        if explicit_list==True:
            print(Elements.loop_l)

    def function_list(explicit_list=False):
        Elements.function_l=[]
        for i,d in enumerate(Elements.constructs["function"]):
            Elements.function_l.append( (Elements.constructs["function"][d].name,
                                                                    Elements.constructs["function"][d].start) )
        Elements.function_l.sort()
        if explicit_list==True:
            print(Elements.function_l)

    def closed_list(explicit_list=False):
        Elements.closed_l=[]
        for i,d in enumerate(brackets.found["closed"]):
            Elements.closed_l.append(brackets.found["closed"][d].line)
        Elements.closed_l.sort()
        if explicit_list==True:
            print(Elements.closed_l)

    def kwfind(value):
        for i,d in enumerate(Elements.constructs):
            for item in Elements.constructs[d]:
                if item==value:
                    return("Elements.constructs[\"%s\"][\"%s\"]" %(d, item), #0
                                Elements.constructs[d][item], #1
                                item) #2

    def nearer_closer(list_a, list_b):
        #list_a[0][0] = function/loop name
        #list_a[0][1] = function/loop line(int)
        while len(list_a)!=0:
                for i,d in enumerate(list_b):
                    if list_a[-1][1]<d:
                        print(list_a[-1][0],"starts at", list_a[-1][1],"and closes at line",d)
                        Elements.kwfind(list_a[-1][0])[1].end=d
                        list_a.remove(list_a[-1]) #no pop(0) for clearer meaning
                        list_b.remove(d)
                        break

    parent = []

    counter = {
        "function":0,
        "switch":0,
        "for_loop":0,
        "dowhile":0,
        "if":0,
        "else":0,
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
                        if d >= item:
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

def loop_detector(log=False):
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
                                if d >= item:
                                    if log==True:
                                        print(brackets.found["open"]["b%so"%i].code,
                                            "[foundlist item", i,  "located at line "+str(d)+"]",
                                            "is starting", kind_code, "\n")
                                    return(d) #end of loop_start

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


if arguments.functions:
    print("FUNCTION DETECTOR\nUsing %s language module..\n" %language)
    function_detector(log)

if arguments.loops:
    print("LOOP DETECTOR\nUsing %s language module..\n" %language)
    loop_detector(log)


if arguments.closed:
    print("-- Executing loop/function closer --\n")
    function_detector()
    loop_detector()
    Elements.function_list()
    Elements.loop_list()
    Elements.closed_list()

    Elements.nearer_closer(Elements.loop_l, Elements.closed_l)
    Elements.nearer_closer(Elements.function_l, Elements.closed_l)

if not arguments.functions and arguments.loops and arguments.closed:
    print("No command specified -- stopping")
    exit()
