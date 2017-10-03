import re, cpp, syckIO

from linecache import *

testfile = "testfile"

for item in cpp.lang_classes:
    print(item)


lines=syckIO.lines

syckIO.reader()
#print(lines)

class Elements:
    
    functions={}

    function_attributes = ["name","return_type","extension","args","nested"]


def function_detector():
    
    
    for item in lines:
        
        function_match = re.match(cpp.Function.init_pattern, lines[item])
        if function_match:
    
            print("Matching: ", lines[item])

            Elements.functions[function_match.group("f_name")]=cpp.Function(name=function_match.group("f_name"),
            return_type = function_match.group("return_type"))


