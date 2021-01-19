import glob, os, random

class Deck(object):
    def __init__(self, img_dir = None):
        self.img_dir = img_dir

        self.cards = []
        if img_dir:
            os.chdir(img_dir)
            for card in glob.glob("*.png"):
                self.cards.append(card)    
    
    def deal(self):
        return self.cards.pop(random.randrange(len(self.cards)))
    
    def add(self, card):
        self.cards.append(card)