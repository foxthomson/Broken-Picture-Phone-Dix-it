from player import Player
from deck import Deck
from random import shuffle
import random
import discord

welcome_messages = [
    "Can you hear me?",
    "Oh, hello!",
    "New phone, who this?",
    "Dix-it begins",
    "I awaken",
    "Who summoned me?",
    "Beep boop?",
    "Noot noot!",
    ";)",
    "A wild Dix-It appears",
    "I have been summoned",
]
deal_messages = [
    "I deal the cards",
    "You get a card, you get a card, you all get cards!!!",
    "Sending virtual cards...",
    "Please accept this gift",
    "Merry christmas",
    "Happy birthday",
    "Cards a coming",
]
storyteller_messages = [
    "{} is our leader",
    "Try to get inside {}'s mind this round",
    "You're gonna have to think like {} this round",
    "Would {} please pick an easy one this round",
    "Time to put {} on the spot!",
]
wait_messages = [
    "The following people are slow: {}",
    "Shame these people: {}",
    "Indecisive people: {}",
    "I'm waiting for: {}",
    "Why can't {} make up their minds",
    "I'm gonna start without {}",
    "Complain at {} for your bordem",
    "{} just slow us down",
    "{}. You've been shamed!!",
]
choices_messages = [
    "This is the choices",
    "Here are some pictures",
    "I drew these myself",
    "Art?",
    "Delivery for you!",
    "Enjoy",
    "You all finally picked!"
]
choose_messages = [
    "You won't regret choosing {}",
    "Great decision picking {}!",
    "I would have chosen {} too",
    "{} is a winner",
    "I love {} too",
    "{} is a great choice",
    "I'm so pleased you choose {}"
]
answer_messages = ["{} was the correct answer"]
correct_messages = ["{} got the correct answer"]
voted_messages = ["{} voted for {}'s card"]
everyone_correct_messages = ["Everyone picked the right card"]
noone_correct_messages = ["Noone picked the right card"]
start_vote_messages = [
    "Cast your votes now!",
    "Guess... if you dare",
    "Let's do this thing!",
]
vote_messages = [
    "You won't regret choosing {}",
    "Great decision picking {}!",
    "I would have chosen {} too",
    "{} is a winner",
    "I love {} too",
    "{} is a great choice",
    "I'm so pleased you choose {}"
]

class Game(object):
    def __init__(self, game_channel, img_dir):
        self.players = {}
        self.game_channel = game_channel
        self.deck = Deck(img_dir)
        self.pile = []
        self.storyteller = None
        self.turn_order = None

    async def add_player(self, user):
        newplayer = Player(user)
        self.players[user] = (newplayer)
        await newplayer.message(random.choice(welcome_messages))

    def start(self):
        self.turn_order = list(self.players.values())
        shuffle(self.turn_order)
        self.storyteller = 0

    async def new_round(self):
        self.storyteller = (self.storyteller + 1) % len(self.players)
        self.pile = []
        await self.game_channel.send(random.choice(storyteller_messages).format(self.turn_order[self.storyteller].user.name))
        self.waiting = list(self.players.values())
        self.wait_message_text = random.choice(wait_messages)
        self.wait_message = await self.game_channel.send(self.wait_message_text.format(", ".join(map(lambda p: p.user.name, self.waiting))))

    async def deal_cards(self, hand_size):
        print(self.players)
        for player in self.players.values():
            print(player.user.name)
            for _ in range(hand_size):
                player.draw(self.deck.deal())
        await self.game_channel.send(random.choice(deal_messages))

    async def choose(self, player, choice):
        if self.players[player] in self.waiting:
            self.waiting.remove(self.players[player])
            await self.wait_message.edit(content=self.wait_message_text.format(", ".join(map(lambda p: p.user.name, self.waiting))))
            self.pile.append((self.players[player].choose(choice), self.players[player]))
            await self.players[player].message(random.choice(choose_messages).format(choice))
            if self.waiting == []:
                await self.vote_phase()
                
    async def vote_phase(self):
        try:
            await self.wait_message.delete()
        except Exception as e:
            pass
        shuffle(self.pile)
        await self.game_channel.send(random.choice(choices_messages), files=list(map(lambda f: discord.File(f[0]), self.pile)))
        await self.game_channel.send(random.choice(start_vote_messages))
        self.waiting = list(self.players.values())
        self.wait_message_text = random.choice(wait_messages)
        self.waiting.remove(self.turn_order[self.storyteller])
        self.wait_message = await self.game_channel.send(self.wait_message_text.format(", ".join(map(lambda p: p.user.name, self.waiting))))

    async def vote(self, player, vote):
        if self.players[player] in self.waiting:
            await player.send(random.choice(vote_messages).format(vote))
            self.waiting.remove(self.players[player])
            await self.wait_message.edit(content=self.wait_message_text.format(", ".join(map(lambda p: p.user.name, self.waiting))))
            self.players[player].vote = vote
            if self.waiting == []:
                await self.round_end()
    
    async def round_end(self):
        try:
            await self.wait_message.delete()
        except Exception as e:
            pass
        answer = list(map(lambda x: x[1], self.pile)).index(
            self.turn_order[self.storyteller]) + 1
        await self.game_channel.send(random.choice(answer_messages).format(answer))
        correct = []
        votes = [[] for _ in self.pile]
        for player in self.players.values():
            if player == self.turn_order[self.storyteller]:
                continue
            if player.vote == answer:
                correct.append(player)
            else:
                votes[player.vote - 1].append(player)
        if len(correct) == len(self.players) - 1:
            await self.game_channel.send(random.choice(everyone_correct_messages))
            for player in self.players.values():
                if player != self.turn_order[self.storyteller]:
                    player.score += 2
        elif correct == []:
            await self.game_channel.send(random.choice(noone_correct_messages))
            for player in self.players.values():
                if player != self.turn_order[self.storyteller]:
                    player.score += 2
        else:
            await self.game_channel.send(random.choice(correct_messages).format(", ".join(map(lambda p: p.user.name, correct))))
            for player in correct:
                player.score += 3
            self.turn_order[self.storyteller].score += 3
            for ((_, player), votes) in zip(self.pile, votes):
                if votes != []:
                    await self.game_channel.send(random.choice(voted_messages).format(", ".join(map(lambda p: p.user.name, votes)), player.user.name))
                    player.score += len(votes)
        await self.display_score()
        await self.new_round()

    async def display_score(self):
        await self.game_channel.send("\n".join(map(lambda p: "{} has {} points".format(p.user.name, p.score), list(self.players.values()))))
