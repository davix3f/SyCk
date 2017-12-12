#lang:CPP
#v:0.10
import re

class FunctionClass:
    def __init__(self,
                        name,
                        return_type,
                        dect_at,
                        start=None,
                        args=None,
                        end=None,
                        nested={}):

        self.name = name
        self.return_type = return_type
        self.args = args
        self.dect_at = dect_at
        self.start = start
        self.end = end
        self.nested = nested

    def calculateExtension(start, end):
        self.extension = (start, end)
        return(self.extension)


class ForClass:
    def __init__(self,
                        dect_at,
                        name,
                        start=None,
                        args=None,
                        end=None,
                        nested={}):
        self.name = name
        self.args = args
        self.dect_at = dect_at
        self.start = start
        self.end = end
        self.nested = nested



class WhileClass:
    def __init__(self,
                        dect_at,
                        name,
                        start=None,
                        args=None,
                        end=None,
                        nested={}):
        self.name = name
        self.args = args
        self.dect_at = dect_at
        self.start = start
        self.end = end
        self.nested = nested


class DoWhileClass:
    def __init__(self,
                        dect_at,
                        name,
                        start=None,
                        args=None,
                        end=None,
                        nested={}):
        self.name = name
        self.args = args
        self.dect_at = dect_at
        self.start = start
        self.end = end
        self.nested = nested

class SwitchClass:
    def __init__(self,
                        dect_at,
                        name,
                        start=None,
                        args=None,
                        end=None,
                        nested={}):
        self.name = name
        self.args = args
        self.dect_at = dect_at
        self.start = start
        self.end = end
        self.nested = nested

#List of all langclasses. Keep it updated.

lang_classes = [ ForClass, WhileClass, DoWhileClass, SwitchClass, FunctionClass ]


Function = {"name" : "Function",
                    "init_pattern": r"(?P<return_type>(int|bool|char|string|void))[\s]+(?P<f_name>\w+)[\s]*\(((int|bool|char|string)(.+)?)?\)[\s]*[\{]*",
                    "final_pattern": r"}$"}


For_loop = {
    "name" : "For_loop",
    "init_pattern" : r"for([\s]*)\(",
    "mid_pattern" : {"init_condition":r"(int [\w]+[\s]?\=[\s]?[\d]+\;)|(\;[\s]*)", #initial statement
			                       "final_condition":r"((int)?[\w]+(\==|\<|\>|!=|\>=|\<=)[\d]+\;)|(\;[\s]*)", #final condition to stop for
			                       "increment_operator":r"(([\w]+)?[\s]?(\++|\--|\+=[\d]+|\-=[\d]+|\/=[\d]+|\*=[\d]+)\))?" #incrementing operator [ex x++]
                                   },
    	"final_pattern" : r"\)[\s]?\{.+\}" # something){codecodecode} -- detector
}


While_loop = {
    "name" : "While_loop",
    "init_pattern" : r"while[\s]?\(",

    "mid_pattern" : r"(([\w]+[\s]?(\==|\<|\>|!=|\>=|\<=)?[\d]*)|[\w]+)",

    "final_pattern" : r"\)[\s]?\{.+\}"
}


DoWhile = {
    "name" : "DoWhile",
    "init_pattern" : r"do([\s]*)\{.+\}",
    "final_pattern" : r"while\((([\s]*\([\w]+[\s]?(\==|\<|\>|!=|\>=|\<=)?[\d]*)|[\w])+\)"
}


Switch = {
    "name" : "switch",
    "init_pattern" : r"(switch)([\s]*)\(([\w]+|[\d]+)\)([\s]*)(\{)*",
    "mid_pattern" : r"case ([\w]+|[\d]+)\:[\n]([\t]*(.*)[\n]*)*break;",
    "final_pattern" : r"break;((\n)*)(\s*)?\}"
}

lang_index = [Function, For_loop, While_loop, DoWhile, Switch]

def finder(target, log=False): #change log to True to have things written
    for item in lang_index:
        if re.search(item["init_pattern"], target)!=None:
            if log != False:
                print("-- Matching %s statement--" %item["name"])
            return(True, item["name"])
