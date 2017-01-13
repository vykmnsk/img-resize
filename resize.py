import os
import glob
from PIL import Image, ExifTags

OUTDIR = 'resized'
SIZE = 1200, 1200

if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)

for filename in glob.glob('*.JPG'):
    img = Image.open(filename)

    if hasattr(img, '_getexif'):  # only present in JPEGs
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        e = img._getexif()       # returns None if no EXIF data
        if e is not None:
            exif = dict(e.items())
            orientation = exif[orientation]

            if orientation == 3:   img = img.transpose(Image.ROTATE_180)
            elif orientation == 6: img = img.transpose(Image.ROTATE_270)
            elif orientation == 8: img = img.transpose(Image.ROTATE_90)

    img.thumbnail(SIZE, Image.ANTIALIAS)
    img.save(os.path.join(OUTDIR, filename))
    img.close()


