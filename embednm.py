import sys
import shutil
import zlib
import binascii
import xml.etree.ElementTree as etree
import zipfile
from zipfile import ZipFile, ZipInfo, ZIP_STORED, ZIP_DEFLATED
from contextlib import closing
import os, re
import os.path
import argparse

def run(path_to_ebook,marg, calibre):
        inf = zipfile.ZipFile(path_to_ebook, "r")
        namelist = set(inf.namelist())
        if 'content.opf' not in namelist:
            print "Error: content.opf missing."
            sys.exit(0)
        content = etree.fromstring(inf.read('content.opf'))
        manifest = content.find("{http://www.idpf.org/2007/opf}manifest")
        if manifest == None:
            print "Error: manifest in content.xml missing"
            sys.exit(0)

        #modify stylesheet.css file
        #    text-decoration: underline
        #    text-style: italic

        # embed negative margins into calibre class for basic test
        stylesheetcontent = inf.read('stylesheet.css')
        #sample = '.calibre'+ calibre +' {'
        sample = '.' + calibre +' {'

#        shifts = "margin-left: -" + left + "pt;margin-right: -" + right + "pt; "
        shifts = "margin:  0pt  -" + marg + "pt  0pt;"
        insertplace = stylesheetcontent.find(sample) + len(sample)
        newstylesheetcontent = stylesheetcontent[:insertplace] + shifts + stylesheetcontent[insertplace:]
        insertplace = insertplace + len(shifts)
        curl_pos = newstylesheetcontent.find('}',insertplace)
        marg_pos = newstylesheetcontent.find('margin',insertplace,curl_pos)
        if marg_pos != -1:
            newline_pos = newstylesheetcontent.find('\n',marg_pos)
            newstylesheetcontent = newstylesheetcontent[:marg_pos] + '/*' + newstylesheetcontent[marg_pos:]
            newstylesheetcontent = newstylesheetcontent[:newline_pos+2] + '*/' + newstylesheetcontent[newline_pos+2:]
        # embed spaces around each entry of 'font-style: italic'
        #insertplace = newstylesheetcontent.find('font-style: italic')
        #if insertplace != -1:
        #    newstylesheetcontent = newstylesheetcontent[:insertplace] + \
        #    "*{text-indent: " + left + "px;margin-right: " +\
        #    right + "px;} " + \
        #    newstylesheetcontent[insertplace:]

        #insertplace = 0
        #shift_string = "text-indent: " + ileft + "px;margin-right: " + iright + "px; font-style: italic;"
        #shift = len(shift_string)
        #while insertplace < len(newstylesheetcontent):
        #    insertplace = newstylesheetcontent.find('font-style: italic',insertplace)
        #    if insertplace == -1:
        #        break
        #    newstylesheetcontent = newstylesheetcontent[:insertplace] + \
        #        "text-indent: " + ileft + "px;margin-right: " +\
        #        iright + "px; " + \
        #        newstylesheetcontent[insertplace:]
        #    insertplace += shift
        ## embed spaces arounf underlined text
        #insertplace = 0
        #shift_string = "margin-left: " + ileft + "px;margin-right: " + iright + "px; text-decoration: underline;"
        #shift = len(shift_string)
        #while insertplace < len(newstylesheetcontent):
        #    insertplace = newstylesheetcontent.find('text-decoration: underline',insertplace)
        #    if insertplace == -1:
        #        break
        #    newstylesheetcontent = newstylesheetcontent[:insertplace] + \
        #        "margin-left: " + ileft + "px;margin-right: " +\
        #        iright + "px; " + \
        #        newstylesheetcontent[insertplace:]
        #    insertplace += shift

        namelist.remove('content.opf')
        namelist.remove('stylesheet.css')
        namelist.remove('mimetype')
        kwds = dict(compression=ZIP_DEFLATED, allowZip64=False)
        # create the modified archive
        temp = "temp.epub"
        outf = zipfile.ZipFile(temp, "w", **kwds)
        # output mimetype uncompressed and first
        zi = inf.getinfo('mimetype')
        zi.compress_type = ZIP_STORED
        outf.writestr(zi, inf.read('mimetype'))
        # then write other files
        outf.writestr('content.opf', etree.tostring(content))
        outf.writestr('stylesheet.css', newstylesheetcontent)
        for path in namelist:
            data = inf.read(path)
            outf.writestr(path, data)
        outf.close()
        shutil. copy (temp , path_to_ebook)
        os.remove(temp)
        return path_to_ebook

#main
# Accepts four parameters: file name, left margin, right margin, and Calibre class name  for a class that renders basic text
# Inserts negative margins into respective class definition AND comments out FIRST margin line in that class
parser = argparse.ArgumentParser(description='T')
parser.add_argument('-m', action="store", dest="marg", default='9', help='Basic text (class selection needed)left=right negative margin, pt')
parser.add_argument('-e', action="store", dest="file", help='Input epub file name with extension')
parser.add_argument('-c', action="store", dest="calibre", default='Calibre3', help='Calibre class for basic text')
results = parser.parse_args()
marg = results.marg
if int(marg)<0:
    marg = str(-int(marg))
calibre = results.calibre
path_to_ebook = results.file
m = run(path_to_ebook,marg,calibre)


