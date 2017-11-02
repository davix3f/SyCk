#lang:CPP
#v:0.7

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
    pass



class WhileClass:
    pass



class DoWhileClass:
    pass


class SwitchClass:
    pass



#List of all langclasses. Keep it updated.

lang_classes = [ ForClass, WhileClass, DoWhileClass, SwitchClass, FunctionClass ]


Function = {"init_pattern": r"(?P<return_type>(int|bool|char|string|void))[\s]+(?P<f_name>\w+)[\s]*\(((int|bool|char|string)(.+)?)?\)[\s]*[\{]*",
                    "final_pattern": r"}$"}


For = {
    "init_pattern" : r"^for\(",
    "mid_pattern" : {"init_condition":r"(int [\w]+[\s]?\=[\s]?[\d]+\;)|(\;[\s]*)", #initial statement
			                       "final_condition":r"((int)?[\w]+(\==|\<|\>|!=|\>=|\<=)[\d]+\;)|(\;[\s]*)", #final condition to stop for
			                       "increment_operator":r"(([\w]+)?[\s]?(\++|\--|\+=[\d]+|\-=[\d]+|\/=[\d]+|\*=[\d]+)\))?" #incrementing operator [ex x++]
                                   },
    	"final_pattern" : r"\)[\s]?\{.+\}" # something){codecodecode} -- detector
}


While = {
    "init_pattern" : r"while[\s]?\(",

    "mid_pattern" : r"(([\w]+[\s]?(\==|\<|\>|!=|\>=|\<=)?[\d]*)|[\w]+)",

    "final_pattern" : r"\)[\s]?\{.+\}"
}


DoWhile = {
    "init_pattern" : r"do \{.+\}",
    "final_pattern" : r"while\((([\s]*\([\w]+[\s]?(\==|\<|\>|!=|\>=|\<=)?[\d]*)|[\w])+\)"
}


Switch = {
    "init_pattern" : r"switch[\s]*\(([\w]+|[\d]+)\)[\s]*\{",
    "mid_pattern" : r"case ([\w]+|[\d]+)\:[\n]([\t]*(.*)[\n]*)*break;",
    "final_pattern" : r"break;((\n)*)(\s*)?\}"
}

lang_index = [Function, For, While, DoWhile, Switch]
