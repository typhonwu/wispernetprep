import sys, os, inspect
import shutil
import extractcover
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
        resize(imgname)    

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

    draw(infilename, imgtext)

    return 0

def draw(infilename, imgtext):
    #add/not add book number in sequence
    if imgtext == None: return
    print "Drawing:", imgtext
    if imgtext=='auto':
        seqnum = infilename[0] + (infilename[1] if infilename[1].isdigit() else "")
        if seqnum.isdigit():
            thumb_name = "thumbnail_" + infilename + "_EBOK_portrait.jpg"
            txt2img(seqnum,img_in = thumb_name,img_out = thumb_name)
        else:
            print "Warning: name does not start with digits", seqnum  
    else:
        #actions for drawing number
        #draw user defined book sequence number
        if not imgtext.isdigit():
            print "Error: image text should be digits only"
            return 1
        #seqnum = imgtext[0:2].zfill(2)
        seqnum = imgtext[0:2]
        thumb_name = "thumbnail_" + infilename + "_EBOK_portrait.jpg"
        print "Sequence number:", seqnum
        txt2img(seqnum,img_in = thumb_name,img_out = thumb_name)

def resize(img_in):
    try:
        from PIL import Image
        img = Image.open(img_in)
        img = img.resize((250,400), Image.ANTIALIAS)
        img.save(img_in, "JPEG", quality=100)
    except ImportError as e:
        print "Error:", e
        print "Warning: Pillow is not installed - image not resized"

def txt2img(text, img_in = 'thumb.jpg', img_out = 'thumb2.jpg'):
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.open(img_in)
        font = 'PTC55F.ttf'
        font_size = 35
        font_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        fnt = ImageFont.truetype(os.path.join(font_dir, font), font_size)
        mask = Image.new('L', img.size, 'black')       # make a mask that masks out all
        draw = ImageDraw.Draw(img)                     # setup to draw on the main image
        drawmask = ImageDraw.Draw(mask)                # setup to draw on the mask
        width,height = img.size
        # mask position
        xmask = 1.10*font_size
        ymask = height - 1.10*font_size
        haxis = font_size
        drawmask.ellipse((xmask - haxis, ymask - haxis, xmask + haxis, ymask + haxis),fill=255)
        img.paste(0, mask=mask)                    # put the (somewhat) transparent bg on the main
        textwidth, textheight = fnt.getsize(text)
        draw.text((xmask-0.5*textwidth, ymask - 0.5*textheight), text, font=fnt, fill=(255,255,255,255))
        del draw
        img.save(img_out, "JPEG", quality=100)
    except ImportError as e:
        print "Error:", e
        print "Warning: Pillow is not installed - image text not drawn"


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
