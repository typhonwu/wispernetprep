import sys, os, inspect
import unicodefix
from unidecode import unidecode

def ProcessString(instr):
        outstr = unidecode(instr).replace("'","z")
        sys.stdout.write(outstr)
        return 0
def main(argv=sys.argv): 
    input = unicode(argv[1], sys.stdin.encoding)
    return ProcessString(input)

if __name__ == "__main__":
    sys.exit(main())