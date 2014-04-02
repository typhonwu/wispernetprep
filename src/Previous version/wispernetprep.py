#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys, os, inspect
import shutil
import extractcover
import glob
from subprocess import Popen, PIPE, STDOUT
import mobiunpack32

def processFile(infile, imgtext, asin):
    #asin is a third CIL parameter.
    #If imgtext=='asin' then asin is amazon's ASIN
    #If imgtext=='title' then asin contains sequence number
    infilename = os.path.splitext(infile)[0]
    infileext = os.path.splitext(infile)[1]
    files = mobiunpack32.fileNames(infile, "tmpdir2.$$$")
    mu = mobiunpack32.mobiUnpack(files)
    metadata = mu.getMetaData()
    bktitle = unicode(mu.title, mu.codec).encode("utf-8")
    inputdir = "input.$$$"
    outputdir = "output.$$$"
    os.mkdir(inputdir)
    os.mkdir(outputdir)
    shutil.copy(infile, os.path.join(inputdir, infilename + ".mobi"))
    if (imgtext != 'asin'):
        for file in glob.glob(os.path.join("images.$$$", infilename + '.cover*')):
            imgname = "thumbnail_" + infilename + "_EBOK_portrait.jpg"
            shutil.copy(file, imgname)
            resize(imgname)
    scriptdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    cmd = 'java -cp "' + os.path.join(scriptdir, "MobiMetaEditorV0.16.jar") + '" cli.WhisperPrep "%s" "%s"' % (
        inputdir, outputdir)
    print "Running", cmd
    process = Popen(cmd, stdin=PIPE, stdout=sys.stdout, stderr=STDOUT)
    if imgtext == 'asin':
        process.stdin.write(asin)
    else:
        process.stdin.write(infilename)
    process.stdin.write("\n")
    process.stdin.close()
    process.wait()
    shutil.copy(os.path.join(outputdir, infilename + ".mobi"), infilename + ".processed" + infileext)
    shutil.rmtree("images.$$$")
    shutil.rmtree(inputdir)
    shutil.rmtree(outputdir)
    shutil.rmtree("tmpdir2.$$$")

    if (imgtext != 'asin'):
        draw(infilename, imgtext, bktitle, asin)

    return 0


def draw(infilename, imgtext, bktitle, asin):
    #add/not add book number in sequence
    drawtitle = 0
    if imgtext == None: return
    print "Drawing:", imgtext
    if imgtext in ('auto','autotitle','title'):
        seqnum = infilename[0] + (infilename[1] if infilename[1].isdigit() else "")
        thumb_name = "thumbnail_" + infilename + "_EBOK_portrait.jpg"
        if imgtext in ('auto','autotitle'):
            if imgtext=='auto':
                drawtitle = 0 # do not draw title
            else:
                drawtitle = 1 # draw auto number and title
            if seqnum.isdigit():
                txt2img(seqnum, bktitle, drawtitle, img_in=thumb_name, img_out=thumb_name)
            else:
                print "Warning: name does not start with digits", seqnum
        else: #title; number+title if asin is not empty
            if asin==None: # draw title only, no number
                drawtitle = 2
                asin = '0'
            else:
                drawtitle = 1 #draw number and title
            txt2img(asin, bktitle, drawtitle, img_in=thumb_name, img_out=thumb_name)
    else:
        #draw user defined book sequence number
        if not imgtext.isdigit():
            print "Error: image text should be digits only"
            return 1
        #seqnum = imgtext[0:2].zfill(2)
        seqnum = imgtext[0:2]
        thumb_name = "thumbnail_" + infilename + "_EBOK_portrait.jpg"
        print "Sequence number:", seqnum
        txt2img(seqnum, bktitle, drawtitle, img_in=thumb_name, img_out=thumb_name)


def resize(img_in):
    try:
        from PIL import Image

        img = Image.open(img_in)
        img = img.resize((250, 400), Image.ANTIALIAS)
        img.save(img_in, "JPEG", quality=100)
    except ImportError as e:
        print "Error:", e
        print "Warning: Pillow is not installed - image not resized"


def txt2img(text, bktitle, drawtitle, img_in='thumb.jpg', img_out='thumb2.jpg'):
    #bktitle: contains book title extracted from file
    #drawtitle: control drawing flag; ==0 number only, no title; ==1 number + title; ==2: no number, title only
    try:
        from PIL import Image, ImageDraw, ImageFont
        import textwrap
        img = Image.open(img_in)
        #prepare font
        font = 'PTC55F.ttf'
        #font = 'ARIALBD.TTF'
        font_size = 35
        font_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        fnt = ImageFont.truetype(os.path.join(font_dir, font), font_size)
        #prepare black/white text background
        width, height = img.size
        # mask position
        xmask = 1.10 * font_size
        ymask = height - 1.10 * font_size
        haxis = font_size
        #
        #Select colors
        #
        #bgcolor = 'white'
        #txtcolor = 'black'
        bgcolor = 'black'
        txtcolor = 'white'
        draw = ImageDraw.Draw(img)  # setup to draw on the main image
        textwidth, textheight = fnt.getsize(text)
        if drawtitle<2:
            #
            #draw sequence number
            #
            #draw number background
            draw.ellipse((xmask - haxis, ymask - haxis, xmask + haxis, ymask + haxis), fill=bgcolor)
            #draw number
            #if len(text) < 2:
            #    text = '0' + text
            draw.text((xmask - 0.5 * textwidth, ymask - 0.5 * textheight), text, font=fnt, fill=txtcolor)
        if drawtitle>0:
            #
            #draw title background
            #
            #line must draw along the text center line
            if drawtitle<2:
                draw.line((xmask + 0.5*haxis, ymask, xmask + haxis + 0.7 * width, ymask),fill=bgcolor,width=int(1.4*haxis))
            else:
                draw.line(( 0, ymask, width, ymask),fill=bgcolor,width=int(1.4*haxis))
            #draw.polygon((xmask + 0.5*haxis, ymask +  0.7*haxis
            #                  , xmask + haxis + 0.7 * width, ymask + 0.7*haxis
            #                  , xmask + haxis + 0.7 * width, ymask - 0.7*haxis
            #                  , xmask + 0.5*haxis, ymask - 0.7*haxis), fill=bgcolor)
            #draw title
            text2 = bktitle.decode('utf-8')
            text2= text2.upper()
            font_size2 = 15
            fnt2 = ImageFont.truetype(os.path.join(font_dir, font), font_size2)
            textwidth2, textheight2 = fnt.getsize(text2)
            if drawtitle<2:
                margin = xmask + haxis
            else:
                margin = 0.5*fnt2.getsize(text2)[1]
            offset = ymask - 0.6*textheight
            if len(text2)<=20:
                offset = ymask - 0.25*textheight2
            if drawtitle<2:
                titlelength = 18
            else:
                titlelength = 27
            #
            #No wrap drawing
            #
            splits=[text2[x:x+titlelength] for x in range(0,len(text2),titlelength)]
            ystep = fnt2.getsize(text2)[1]
            for i in range (len(splits) if len(splits)<3 else 3):
                line = splits[i]
                draw.text((margin, offset), line, font=fnt2, fill=txtcolor)
                offset += ystep
            #
            # This is wrapping alternative
            #
            #for line in textwrap.wrap(text2, width=titlelength):
            #    draw.text((margin, offset), line, font=fnt2, fill=txtcolor)
            #    offset += fnt2.getsize(line)[1]
        img.save(img_out, "JPEG", quality=100)
        del draw
    except ImportError as e:
        print "Error:", e
        print "Warning: Pillow is not installed - image text not drawn"


def main(argv=sys.argv):
    numofparams = len(argv) - 1
    if numofparams < 1 or numofparams > 3:
        print "Usage:"
        print "  wispernetprep.py infile [<sequence number>|auto|autotitle|[title[<sequence number>]][asin]<user's ASIN>]"
        return 1
    else:
        extractcover.main(argv[0:2])
        return processFile(argv[1], argv[2] if numofparams in (2,3) else None, argv[3] if numofparams == 3 else None)

if __name__ == "__main__":
    sys.exit(main())
