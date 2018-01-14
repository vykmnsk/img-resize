import os
import re
import glob
from PIL import Image, ExifTags

OUTDIR = 'resized'
SIZE = 1200, 1200

if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)

# for filename in glob.glob('*.JPG'):
for filename in [f for f in glob.glob('*') if re.match('^.*\.JPG$', f, flags=re.IGNORECASE)]:
    print 'processing {}/{}'.format(OUTDIR, filename)
    img = Image.open(filename)

    if hasattr(img, '_getexif'):  # only present in JPEGs
        exif = img._getexif()       # returns None if no EXIF data
        key = next((k for k,v in ExifTags.TAGS.items() if v == 'Orientation'), None)
        if key and (key in exif):
            orientation = exif[key]
            if orientation == 3:   img = img.transpose(Image.ROTATE_180)
            elif orientation == 6: img = img.transpose(Image.ROTATE_270)
            elif orientation == 8: img = img.transpose(Image.ROTATE_90)

    img.thumbnail(SIZE, Image.ANTIALIAS)
    img.save(os.path.join(OUTDIR, filename))
    img.close()

