import sys

variables = {}
functions = {}

def debug_tokens(code):
    lines = code.split("\n")
    linenum = 1
    
    for line in lines:
        tokens = line.split() or line.split("\t")
        print(f"tokens: {tokens}. line: {linenum}")

def interpret(code):
    lines = code.split("\n")
    linenum = 1
    in_func = False
    lineslist = []
    funcname = ""

    for line in lines:
        tokens = line.split() or line.split("\t")
        linenum += 1

        if tokens:
            token = tokens[0]
            if not in_func:
                if token == "msg":
                    if tokens[1] == ">>":
                        listmsg = tokens[2:]
                        outputmsg = " ".join(listmsg)
                        print(outputmsg)
                elif token == "int":
                    varname = tokens[1]
                    if tokens[2] == "=":
                        value = tokens[3]
                        variables[varname] = int(value)
                    else:
                        assert False, f"Error at line: {linenum}. Illegal token: {tokens[2]}"
                elif token == "msgvar":
                    if tokens[1] == ">>":
                        varname = tokens[2]
                        print(variables.get(varname))
                elif token == "@" or token == "" or token == "}":
                    pass
                elif token == "float":
                    varname = tokens[1]
                    if tokens[2] == "=":
                        value = tokens[3]
                        variables[varname] = float(value)
                    else:
                        assert False, f"Error at line: {linenum}. Illegal token: {tokens[2]}"
                elif token == "char":
                    varname = tokens[1]
                    chartype = tokens[2]
                    if chartype == "string":
                        if tokens[3] == "=":
                            stringlist = tokens[4:]
                            value = " ".join(stringlist)
                            variables[varname] = value
                        else:
                            assert False, f"Error at line: {linenum}. Illegal token: {tokens[2]}"
                    elif chartype == "char":
                        if tokens[3] == "=":
                            value = tokens[4]
                            variables[varname] = value
                            if len(value) >= 3 or len(tokens) > 5:
                                assert False, f"Error at line: {linenum}. Use only 1 char to make a char variable"
                        else:
                            assert False, f"Error at line: {linenum}. Illegal token: {tokens[2]}"
                elif token == "function":
                    funcname = tokens[1]
                    if tokens[2] == "{":
                        in_func = True
                        functions[funcname] = ""
                elif token == "call":
                    funcname = tokens[1]
                    interpret(functions.get(funcname))
                else:
                    assert False, f"Error at line: {linenum}. Illegal token: {token}"

            if in_func:
                if token == "function":
                    pass
                elif token == "}":
                    codes = "\n".join(lineslist)
                    functions[funcname] = codes
                    in_func = False
                else:
                    tokenlist = tokens
                    lineslist.append(" ".join(tokenlist))

                
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(f"usage: {sys.argsv[0]} <command>")
        print("commands:")
        print("-t <file>           show all the tokens in your file")
        print("<file>              execute your file")
    else:
        command = sys.argv[1]

        if command == "-t":
            filepath = sys.argv[2]
            if filepath.endswith(".sinp"):
                with open(filepath, "r") as f:
                    content = f.read()
                debug_tokens(content)
        else:
            if command.endswith(".sinp"):
                with open(command, "r") as f:
                    content = f.read()
                interpret(content)
