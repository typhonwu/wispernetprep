import sys, os, inspect
import shutil
import extractcover, preparecover
import glob
from subprocess import Popen, PIPE, STDOUT

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
    numofparams = len(argv)-1
    if numofparams < 1 or numofparams > 2:
        print "Usage:"
        print "  wispernetprep.py infile [<sequence number>|auto]"
        return 1
    else:
        extractcover.main(argv[0:2])
        return processFile(argv[1], argv[2] if numofparams == 2 else None)

if __name__ == "__main__":
    sys.exit(main())
