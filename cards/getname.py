import os
import io
from base64 import b64decode
from html.parser import HTMLParser
from PIL import Image, ImageDraw, ImageFont

fnt = ImageFont.truetype("consola.ttf", 30)

class parser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super(parser, self).__init__(*args, **kwargs)
        self.count = 0
        self.getname = False

    def handle_data(self, data):
        if self.getname:
            self.getname = False
            self.name = data[8:-1]

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            self.count+=1
            if os.path.isfile("bppall/" + str(self.count) + ".png"):
                im = Image.new("RGB", (600, 480), "white")
                im.paste(Image.open("bppall/" + str(self.count) + ".png"), (0, 0))
                d = ImageDraw.Draw(im)
                print(self.name)
                d.text((0, 450), "By: " + self.name, fill=(0,0,0), font=fnt)
                im.save("bppcredit/"+str(self.count)+".png", "png")
        if tag == "h3":
            self.getname = True

p = parser()
for filename in os.listdir('bpphtml'):
    f = open("bpphtml/"+filename)
    p.feed(f.read())

