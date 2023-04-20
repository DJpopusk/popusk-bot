import discord
from TOKEN import TOKEN
import logging
import sqlite3
import dbapi
from discord import app_commands
from discord.ext import commands
from connect4 import Game

EMOTES = {':one:': 0, ':two:': 1, ':three:': 2, ':four:': 3, ':5:': 4, ':6:': 5, ':7:': 6,
          ':flag_white:': -1}
client = commands.Bot(command_prefix='!!', case_insensitive=True)
client.remove_command('help')


@client.event
async def on_ready():
    print("started")
    await client.change_presence(activity=discord.Game(' connect 4'))


@client.command()
async def play(ctx):
    if len(ctx.message.mentions) == 0 or ctx.message.mentions[0] == client.user:
        player2 = client.user
    elif ctx.message.mentions[0].bot or ctx.message.mentions[0] == ctx.author:
        await ctx.send("Нельзя начать игру, попробуйте еще раз")

        return None
    else:
        player2 = ctx.message.mentions[0]
    player1 = ctx.author
    gm = Game(p1=player1, p2=player2)
