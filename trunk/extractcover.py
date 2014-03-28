import sys, os
import mobiunpack32
import shutil

def extractThumbnail(infile, outdir):
    files = mobiunpack32.fileNames(infile, outdir)
    
    # Instantiate the mobiUnpack class    
    mu = mobiunpack32.mobiUnpack(files)
    metadata = mu.getMetaData()
    proc = mobiunpack32.processHTML(files, metadata)
    imgnames = proc.processImages(mu.firstimg, mu.sect)
    destdir = "images.$$$"
    os.mkdir(destdir)
    if 'ThumbOffset' in metadata:
        imageNumber = int(metadata['ThumbOffset'][0])
        imageName = imgnames[imageNumber]
        if imageName is None:
            print "Error: Cover Thumbnail image %s was not recognized as a valid image" % imageNumber
        else:
            print 'Cover ThumbNail Image "%s"' % imageName
            infileName = os.path.splitext(infile)[0]
            imageExt = os.path.splitext(imageName)[1]
            shutil.copy(os.path.join("tmpdir.$$$", "images", imageName), os.path.join(destdir, infileName + ".thumbnail"+imageExt))
    if 'CoverOffset' in metadata:
        imageNumber = int(metadata['CoverOffset'][0])
        imageName = imgnames[imageNumber]
        if imageName is None:
            print "Error: Cover image %s was not recognized as a valid image" % imageNumber
        else:
            print 'Cover Image "%s"' % imageName
            infileName = os.path.splitext(infile)[0]
            imageExt = os.path.splitext(imageName)[1]
            shutil.copy(os.path.join("tmpdir.$$$", "images", imageName), os.path.join(destdir, infileName + ".cover"+imageExt))

def processFile(infile):
    infileext = os.path.splitext(infile)[1].upper()
    if infileext not in ['.MOBI', '.PRC', '.AZW', '.AZW4', '.AZW3']:
        print "Error: first parameter must be a Kindle/Mobipocket ebook or a Kindle/Print Replica ebook."
        return 1

    try:
        print 'Extracting...'
        extractThumbnail(infile, "tmpdir.$$$");
        shutil.rmtree("tmpdir.$$$")
        print 'Completed'
        
    except ValueError, e:
        print "Error: %s" % e
        return 1
    return 0

def main(argv=sys.argv):
    if len(argv) != 2:
        print "Usage:"
        print "  extractcover.py infile"
        return 1
    else:  
        return processFile(argv[1])

if __name__ == "__main__":
    sys.exit(main())
