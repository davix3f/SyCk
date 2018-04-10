# lang:CPP
# v:0.5
import re


class _functionclass:
    def __init__(self,
                name,
                return_type,
                dect_at,
                start=None,
                args=None,
                end=None):

        self.name = name
        self.return_type = return_type
        self.args = args
        self.dect_at = dect_at
        self.start = start
        self.end = end

    def calculateExtension(start, end):
        self.extension = (start, end, end-start)
        return(self.extension)


class _forclass:
    def __init__(self,
                dect_at,
                name,
                start=None,
                args=None,
                end=None):
        self.name = name
        self.args = args
        self.dect_at = dect_at
        self.start = start
        self.end = end



class _whileclass:
    def __init__(self,
                dect_at,
                name,
                start=None,
                args=None,
                end=None):
        self.name = name
        self.args = args
        self.dect_at = dect_at
        self.start = start
        self.end = end


class _dowhileclass:
    def __init__(self,
                dect_at,
                name,
                start=None,
                args=None,
                end=None):
        self.name = name
        self.args = args
        self.dect_at = dect_at
        self.start = start
        self.end = end

class _switchclass:
    def __init__(self,
                dect_at,
                name,
                start=None,
                args=None,
                end=None):
        self.name = name
        self.args = args
        self.dect_at = dect_at
        self.start = start
        self.end = end

class _ifclass:
    def __init__(self,
                dect_at,
                name,
                start=None,
                args=None,
                end=None):
        self.name = name
        self.args = args
        self.dect_at = dect_at
        self.start = start
        self.end = end

class _elseclass:
    def __init__(self,
                dect_at,
                name,
                start=None,
                args=None,
                end=None):
        self.name = name
        self.args = args
        self.dect_at = dect_at
        self.start = start
        self.end = end

# List of all langclasses. Keep it updated.
lang_classes = [_forclass,
                _whileclass,
                _dowhileclass,
                _switchclass,
                _functionclass,
                _ifclass]

_function = {
            "init_pattern": r"(?P<error>(?:for|if|while|do))*(\s*)(?P<return_type>.+)(\s+)(?P<f_name>\w+)",
            #  if re.search(^, string).group("error") == None -> no for or else is in function title
            "final_pattern": r"}$"
}


_for_loop = {
            "init_pattern": r"(?:\s*\t*)(for)(\s*)\(",
            "mid_pattern": r"(?P<open_p>\s*\t*\()(\s*)"
}

_while_loop = {}
_dowhile_loop = {}
_switch = {}
_if = {}
_else = {}

lang_index = [_function, _for_loop, _while_loop, _dowhile_loop, _switch, _if, _else]


def finder(target, log=False, filter=[]): #change log to True to have things written
    for item in lang_index:
        if re.search(item["init_pattern"], target)!=None:
            if log == True:
                print("-- Matching %s statement--" %item["name"])
            if re.search(r"\{", re.search(item["init_pattern"], target).group(0))==None:
                start_on_line=False
            else:
                start_on_line=True
            return(True, item["name"], start_on_line)
