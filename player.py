from deck import Deck

import discord

class Player(object):
    def __init__(self, user):
        self.user = user
        self.deck = Deck()
        self.vote = None
        self.score = 0

    async def message(self, message):
        print(self.user.name)
        await self.user.send(message)

    def get_hand(self):
        return list(map(discord.File, self.deck.cards))

    async def display_hand(self):
        print(self.user)
        await self.user.send("This is your hand", files=list(map(discord.File, self.deck.cards)))

    def draw(self, card):
        self.deck.add(card)

    def choose(self, card):
        return self.deck.cards.pop(card-1)
