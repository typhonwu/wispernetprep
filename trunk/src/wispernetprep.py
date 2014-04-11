#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys, os, inspect
import shutil
import extractcover, preparecover
import mobiunpack32
import glob
from subprocess import Popen, PIPE, STDOUT
import argparse
import unicodefix

def processFile(infile, seqnumber, title, asin):
    infilename = os.path.splitext(infile)[0]
    infileext = os.path.splitext(infile)[1]
    inputdir = u"input.$$$"
    outputdir = u"output.$$$"
    os.mkdir(inputdir)
    os.mkdir(outputdir)
    shutil.copy(infile, os.path.join(inputdir, infilename+u".mobi"))
    for file in glob.glob(os.path.join(u"images.$$$", infilename+u'.cover*')):
        imgname = u"thumbnail_" + infilename + u"_EBOK_portrait.jpg"
        shutil.copy(file, imgname)
        preparecover.resize(imgname)    

    scriptdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    cmd = u'java -cp "' + os.path.join(scriptdir, u"MobiMetaEditorV0.16.jar") +u'" cli.WhisperPrep "%s" "%s"' % (inputdir, outputdir)
    print u"Running", cmd
    process = Popen(cmd, stdin=PIPE, stdout=sys.stdout, stderr=STDOUT)
    process.stdin.write(infilename.encode("utf-8") if asin is None else asin)
    process.stdin.write("\n")
    process.stdin.close()
    process.wait()
    shutil.copy(os.path.join(outputdir, infilename+u".mobi"), infilename+u".processed"+infileext)
    shutil.rmtree(u"images.$$$")
    shutil.rmtree(inputdir)
    shutil.rmtree(outputdir)

    title = get_booktitle(infile, title)
    if title==None:
        print "No title"
    else:
        try:
            print u'Title: "%s"' % title
        except:
            tit = translit(title)
            print u'Title: "%s"' % tit
    seqnumber = get_seqnumber(infilename, seqnumber)
    print u'Seq number: "%s"' % seqnumber
    if title is not None or seqnumber is not None:
        preparecover.draw(u"thumbnail_" + infilename + u"_EBOK_portrait.jpg", title, seqnumber)
    
    return 0

def get_booktitle(infile, title):
    if title is None: return None
    title = unicode(title, sys.stdin.encoding)
    if title == 'auto':
        files = mobiunpack32.fileNames(infile, "tmpdir2.$$$")
        mu = mobiunpack32.mobiUnpack(files)
        metadata = mu.getMetaData()
        title = unicode(mu.title, mu.codec)
        shutil.rmtree("tmpdir2.$$$")
    return title

def get_seqnumber(infilename, seqnumber):
    if seqnumber is None: return None
    result = seqnumber if seqnumber != 'auto' else infilename[0] + (infilename[1] if infilename[1].isdigit() else "")
    if not result.isdigit():
        print "Error: image text should be digits only"
        return None
    #result = result[0:2].zfill(2)
    result = result[0:2]
    return result

def translit(locallangstring):
    conversion = {
        u'\u0410' : 'A',    u'\u0430' : 'a',
        u'\u0411' : 'B',    u'\u0431' : 'b',
        u'\u0412' : 'V',    u'\u0432' : 'v',
        u'\u0413' : 'G',    u'\u0433' : 'g',
        u'\u0414' : 'D',    u'\u0434' : 'd',
        u'\u0415' : 'E',    u'\u0435' : 'e',
        u'\u0401' : 'Yo',   u'\u0451' : 'yo',
        u'\u0416' : 'Zh',   u'\u0436' : 'zh',
        u'\u0417' : 'Z',    u'\u0437' : 'z',
        u'\u0418' : 'I',    u'\u0438' : 'i',
        u'\u0419' : 'Y',    u'\u0439' : 'y',
        u'\u041a' : 'K',    u'\u043a' : 'k',
        u'\u041b' : 'L',    u'\u043b' : 'l',
        u'\u041c' : 'M',    u'\u043c' : 'm',
        u'\u041d' : 'N',    u'\u043d' : 'n',
        u'\u041e' : 'O',    u'\u043e' : 'o',
        u'\u041f' : 'P',    u'\u043f' : 'p',
        u'\u0420' : 'R',    u'\u0440' : 'r',
        u'\u0421' : 'S',    u'\u0441' : 's',
        u'\u0422' : 'T',    u'\u0442' : 't',
        u'\u0423' : 'U',    u'\u0443' : 'u',
        u'\u0424' : 'F',    u'\u0444' : 'f',
        u'\u0425' : 'H',    u'\u0445' : 'h',
        u'\u0426' : 'Ts',   u'\u0446' : 'ts',
        u'\u0427' : 'Ch',   u'\u0447' : 'ch',
        u'\u0428' : 'Sh',   u'\u0448' : 'sh',
        u'\u0429' : 'Sch',  u'\u0449' : 'sch',
        u'\u042a' : '"',    u'\u044a' : '"',
        u'\u042b' : 'Y',    u'\u044b' : 'y',
        u'\u042c' : '\'',   u'\u044c' : '\'',
        u'\u042d' : 'E',    u'\u044d' : 'e',
        u'\u042e' : 'Yu',   u'\u044e' : 'yu',
        u'\u042f' : 'Ya',   u'\u044f' : 'ya',
    }
    translitstring = []
    for c in locallangstring:
        translitstring.append(conversion.setdefault(c, c))
    return ''.join(translitstring)


def main(argv=sys.argv):
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', metavar='<input file>', help='Input file')
    parser.add_argument('-s', '--sequence-number',  nargs='?', help='A number to stamp on the cover ("auto" for first one-two characters of the name of the file)')
    parser.add_argument('-t', '--title',  nargs='?', help='A text to stamp on the cover ("auto" for the title from the metainfo of the book)')
    parser.add_argument('-a', '--asin',  nargs='?', help='A text to put into ASIN metainfo field')
    
    args = parser.parse_args()
    print args
    #tprint(args)
    input_file = unicode(args.input_file, sys.stdin.encoding)

    extractcover.processFile(input_file)
    return processFile(input_file, args.sequence_number, args.title, args.asin)

if __name__ == "__main__":
    sys.exit(main())
