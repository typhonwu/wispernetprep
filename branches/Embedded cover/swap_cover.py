import os 
import sys
import unicodefix
from lib.mobi_split2 import mobi_split

def modify_mobi(infile, outfile):
    splitter = mobi_split(infile)
    open(os.path.splitext(outfile)[0] + '.azw3', 'wb').write(splitter.getResult8())

def main(argv=sys.argv):
    # infile, outfile, ASIN
    input_file = unicode(argv[1], sys.stdin.encoding)
    output_file = unicode(argv[2], sys.stdin.encoding)
    return modify_mobi(input_file, output_file)

if __name__ == "__main__":
    sys.exit(main())
