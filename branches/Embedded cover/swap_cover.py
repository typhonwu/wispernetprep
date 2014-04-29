import os 
import sys
from lib.mobi_split2 import mobi_split
def modify_mobi(infile,outfile):
    splitter = mobi_split(infile)
    open(os.path.splitext(outfile)[0] + '.azw3', 'wb').write(splitter.getResult8())

def main(argv=sys.argv):
    # infile, outfile, ASIN
    return modify_mobi(argv[1], argv[2])

if __name__ == "__main__":
    sys.exit(main())
