import sys,os,string
''' Script to make a glossary out of a LaTeX short macros file'''

DEBUG = False
def parseline(line):
    if "%" == line[0]:  # ignore comments
        return None
    if "command" not in line: # not going to work on multiline
        return None
    if "begin" in line  or "end" in line or "vskip" in line or "item" in line: # skip complicated things
        return None
    keys = line.split("{")  # split at the "{"
    if len(keys) < 3:  # a real macro has two "{" in it minimum
        print ("can't understand ",line)
        return None
    
    # start making a latex description of the macro
    thecommand = "\\verb|%s|"%(keys[1].split("}")[0])
    if DEBUG: print ("thecommand",thecommand)
    if "[" in keys[1]:  # does it have arguments? 
        arguments = "["+keys[1].split("[")[1]
    else:
        arguments = ""
    if arguments == "[0]":
        arguments = ""
    #print (arguments)
    
    whatitdoes = "${"+"{".join(keys[2:]).replace("#","\#")[0:-1] +"$"
    if "\`" in line or "vskip" in line:
        whatitdoes = whatitdoes.replace("$","")
    if DEBUG: print (whatitdoes)
    result = "%s%s &$\gt$& %s\\\\[5pt] \n"%(thecommand,arguments,whatitdoes)
    #print ("%s &\gt& %s\n"%(thecommand,whatitdoes))
    return result

# Actually do it.  Open the list of macros and produce a table file. 
inputfile = "extra_macros.tex"
f = open(inputfile,'r')
g = open("list_of_macros.tex",'w')

# input the header
g.write ("\\input header.tex\n")


text = f.readlines()
g.write("\\begin{tabular}{l l l }\n")

count = 0
max = 24  # this is max lines/page
for line in text:
    new = parseline(line)
    if new is None: continue
    if DEBUG: print (new)
    g.write(new)
    count +=1
    if count > max:
        count = 0
        g.write("\\end{tabular}\n\n")
        g.write("\\begin{tabular}{l l l}\n\n")

g.write("\\end{tabular}\n\n")
g.write("\\end{document}\n\n")
print ("run pdflatex on list_of_macros.tex")
g.close()
