import sys, os, inspect

def draw(imgname, imgtext):
    #add/not add book number in sequence
    if imgtext == None: return
    print "Drawing:", imgtext
    if imgtext=='auto':
        seqnum = imgname[0] + (imgname[1] if imgname[1].isdigit() else "")
        if seqnum.isdigit():
            txt2img(seqnum,img_in = imgname,img_out = imgname)
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
        print "Sequence number:", seqnum
        txt2img(seqnum,img_in = imgname,img_out = imgname)

def resize(img_in):
    try:
        from PIL import Image
        img = Image.open(img_in)
        img = img.resize((250,400), Image.ANTIALIAS)
        img.save(img_in, "JPEG", quality=100)
    except ImportError as e:
        print "Error:", e
        print "Warning: Pillow is not installed - image not resized"

def txt2img(text, img_in, img_out):
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
    if len(argv) < 2:
        print "Usage:"
        print "  preparecover.py infile [seqnum]"
        return 1
    else:  
        infile = argv[1]
        resize(infile)
        if (len(argv)==3):
            print "Drawing", argv[2], "on", infile
            draw(infile, argv[2])


if __name__ == "__main__":
    sys.exit(main())
