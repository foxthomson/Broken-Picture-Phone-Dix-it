import os
import io
from base64 import b64decode
from html.parser import HTMLParser
from PIL import Image

class parser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super(parser, self).__init__(*args, **kwargs)
        self.count = 0

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            dat = b64decode(attrs[0][1][22:])
            stream = io.BytesIO(dat)
            im = Image.open(stream)
            # im.show()
            self.count+=1
            im.save("bppall/"+str(self.count)+".png", "png")

p = parser()
for filename in os.listdir('bpphtml'):
    f = open("bpphtml/"+filename)
    p.feed(f.read())