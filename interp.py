import sys
import numbers
import functools


#
# Read an sexpr line by line from the a file
#
# f - a file
#
def read_sexpr(f):
    slist = ''
    for line in f:
        slist += line
    f.close()
    return parse(slist)


#
# Turn a string into a list of tokens that are separated by a space
#
# char - a string of characters
#
def tokenize(chars):
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()


#
# Turn a string representation of an sexpr into a python list representation
#
# program - an sexpr in a string
#
def parse(program):
    return read_from_tokens(tokenize(program))


#
# Turn a string of tokens into a python list
#
# tokens - a string of tokens
#
def read_from_tokens(tokens):
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)  # pop off ')'
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)


#
# Convert a string token into a number or leave as a string
#
# token - a sequence of characters
#
def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return token


#
# Print out a python list as a scheme list
#
# l - a python list
#
def slist(l):
    return str(l).replace('[', '(').replace(']', ')').replace(',', '').replace('\'', '')


#
# Return a builtin function representation
#
# func - a Python function
#
def makebuiltin(func):
    return [">builtin", func]


#
# Return true if parameter is a builtin function representation
#
# l - anything
#
def isbuiltin(l):
    return isinstance(l, list) and len(l) > 0 and l[0] == ">builtin"


#
# Add a list of numbers
#
# args - a list of numbers
#
def plus(args):
    return functools.reduce(lambda a, b: a + b, args)


def first(args):
    return args[0]


#
# Add a name, value pair to the base dictionary
#
# n - name
# v - value
#
def addbaseenv(n, v):
    base[n] = v


#
# Create the base environment
#
# names - base names
# vals - base values
#
def makebase(names, vals):
    if (names):
        base[names[0]] = vals[0]
        return makebase(names[1:len(names)], vals[1:len(vals)])
    else:
        return base


# add #f and first to the bas environment
base = {}  # base environment dictionary
basenames = ["#t", "+", "#f", "first"]  # names in base environment
basevals = [True, makebuiltin(plus), False, makebuiltin(first)]  # corresponding values

globalenv = [makebase(basenames, basevals)]  # the global environment


#
# Lookup an id in an environment
#
# env - a stack of dictionaries
# id - a program id
#
def lookup(env, id):
    if not env:
        return None
    else:
        rec = env[0]
        val = rec.get(id)
        if val is None:
            return lookup(env[1:len(env)], id)
        else:
            return val


def applyFn(v, args):
    if v == plus:
        if len(args) < 1:
            raise RuntimeError
        else:
            for x in args:
                if not isinstance(x, numbers.Number):
                    raise RuntimeError

            return plus(args)

    if v == first:
        if len(args) < 1:
            raise RuntimeError
        args = args[0]
        if len(args) < 1:
            raise RuntimeError
        else:
            return first(args)


#
# Interpret a Scheme expression in an environment
#
# exp - an sexpr
# env - a stack of dictionaries
#
def interp(exp, env):
    if isinstance(exp, numbers.Number):
        return exp
    elif isinstance(exp, str):
        return lookup(env, exp)
    elif isinstance(exp, list):
        if exp[0] == "quote":
            return exp[1]
        elif exp[0] == "if":
            if interp(exp[1], env):
                return interp(exp[2], env)
            else:
                return interp(exp[3], env)
        else:
            if lookup(env, exp[0])[0] == ">builtin":
                args = []
                for y in exp[1:len(exp)]:
                    args.append(interp(y, env))

                return applyFn(lookup(env, exp[0])[1], args)
            else:
                raise RuntimeError("Invalid Scheme Expression")
    else:
        raise RuntimeError("Invalid Scheme Expression")


#
# Interpret an expression in the global environment
#
# exp - an sexpr
#
def interpret(exp):
    return slist(interp(parse(exp), globalenv))


def main(argv):
    f = open(argv[1], "r")
    slist = read_sexpr(f)
    interpret(slist)




if __name__ == '__main__':
    main(sys.argv)
