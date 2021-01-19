import discord
from discord.ext import commands
from game import Game
import logging

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='+',
                   description="Broken Picture Phone Dix it", intents=intents)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    bot.img_dir = "\\bppdi\\bpp"

@bot.command()
async def new(ctx):
    bot.game = Game(ctx.message.channel, bot.img_dir)
    await ctx.send("Type +join to join")

@bot.command()
async def join(ctx):
    await bot.game.add_player(ctx.message.author)
    await ctx.send("Joined!")

@bot.command()
async def hand(ctx):
    await ctx.send("This is your hand", files=bot.game.players[ctx.message.author].get_hand())

@bot.command()
async def start(ctx):
    bot.game.start()
    await bot.game.deal_cards(6)
    await bot.game.new_round()

@bot.command()
async def choose(ctx, choice: int):
    await bot.game.choose(ctx.message.author, choice)

@bot.command()
async def deal(ctx):
    await bot.game.deal_cards(1)
    await bot.game.new_round()

@bot.command()
async def vote(ctx, choice: int):
    await bot.game.vote(ctx.message.author, choice)

@bot.command()
async def score(ctx):
    await bot.game.display_score()

def login(token):
    bot.run(token)

if __name__ == "__main__":
    bot.run(input("Input bot id: "))
