import discord
from TOKEN import TOKEN
import logging
import sqlite3
import dbapi
from discord import app_commands
from discord.ext import commands
from connect4 import Game

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

con = sqlite3.connect("allDATA.db")
cur = con.cursor()
con.commit()

# client = discord.Client()

EMOTES = {'1️⃣': 0, '2️⃣': 1, '3️⃣': 2, '4️⃣': 3, '5️⃣': 4, '6️⃣': 5, '7️⃣': 6,
          '🏳': 'F'}


def game_start_message(message):
    if message.mentions:
        pass


class YLBotClient(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)
        self.game = Game()
        self.playing = False
        self.game_message = None

    async def on_ready(self):
        logger.info(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            logger.info(
                f'{self.user} подключились к чату:\n'
                f'{guild.name}(id: {guild.id})')

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Привет, {member.name}!'
        )

    async def on_message(self, message):
        if message.content and message.content[:6] == "!!play":
            if message.mentions and message.mentions[0]:
                self.game.edit_players(message.author, message.mentions[0])
                self.playing = True
                self.game_message = await message.channel.send(self.game.draw())

                for i in EMOTES:
                    await self.game_message.add_reaction(i)
        if message.author == self.user:
            return
        logger.info(
            f"{message.channel} :: {message.author} :: {message.content}"
            f" :: {message.type} :: {message.components} :: {message.attachments[0] if message.attachments else None}"
            f" :: {message.embeds[0] if message.embeds else None}  :: {message.created_at}")
        if message.content or message.attachments and message.author != 'P0pusk-bot#2673':
            dbapi.add_message(message)

    async def on_reaction_add(self, reaction, user):
        if self.game_message and reaction.message.jump_url == self.game_message.jump_url:
            if user in self.game.players.values():
                if self.game.players[self.game.turn] == user:
                    if EMOTES[reaction.emoji] == "F":
                        self.game.switch_turn()
                        self.game.force_win(self.game.turn)

                        await self.game_message.edit(content=self.game.on_win(self.game.turn))
                        self.game = Game()
                    else:
                        self.game.move(EMOTES[reaction.emoji], self.game.turn)
                        await self.game_message.edit(content=self.game.draw())


intents = discord.Intents.all()
intents.members = True
client = YLBotClient(intents)
tree = app_commands.CommandTree(client)
client.run(TOKEN)
