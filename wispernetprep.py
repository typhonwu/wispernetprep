import sys, os, inspect
import shutil
import extractcover, preparecover
import glob
from subprocess import Popen, PIPE, STDOUT
import argparse

def processFile(infile, imgtext):
    infilename = os.path.splitext(infile)[0]
    infileext = os.path.splitext(infile)[1]
    inputdir = "input.$$$"
    outputdir = "output.$$$"
    os.mkdir(inputdir)
    os.mkdir(outputdir)
    shutil.copy(infile, os.path.join(inputdir, infilename+".mobi"))
    for file in glob.glob(os.path.join("images.$$$", infilename+'.cover*')):
        imgname = "thumbnail_" + infilename + "_EBOK_portrait.jpg"
        shutil.copy(file, imgname)
        preparecover.resize(imgname)    

    scriptdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    cmd = 'java -cp "' + os.path.join(scriptdir, "MobiMetaEditorV0.16.jar") +'" cli.WhisperPrep "%s" "%s"' % (inputdir, outputdir)
    print "Running", cmd
    process = Popen(cmd, stdin=PIPE, stdout=sys.stdout, stderr=STDOUT)
    process.stdin.write(infilename)
    process.stdin.write("\n")
    process.stdin.close()
    process.wait()
    shutil.copy(os.path.join(outputdir, infilename+".mobi"), infilename+".processed"+infileext)
    shutil.rmtree("images.$$$")
    shutil.rmtree(inputdir)
    shutil.rmtree(outputdir)

    preparecover.draw("thumbnail_" + infilename + "_EBOK_portrait.jpg", imgtext)

    return 0

def main(argv=sys.argv):
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', metavar='<input file>', help='Input file')
    parser.add_argument('-seq', '--sequence-number',  nargs='?', help='A number to stamp on the cover ("auto" for first one-two characters of the name)')
    
    args = parser.parse_args()
    print args

    extractcover.processFile(args.input_file)
    return processFile(args.input_file, args.sequence_number)

if __name__ == "__main__":
    sys.exit(main())
