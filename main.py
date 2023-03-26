import discord
from TOKEN import TOKEN
import logging
import sqlite3
import dbapi

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

con = sqlite3.connect("allDATA.db")
cur = con.cursor()
con.commit()


# client = discord.Client()


class YLBotClient(discord.Client):

    async def on_ready(self):
        logger.info(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            logger.info(
                f'{self.user} подключились к чату:\n'
                f'{guild.name}: (id: {guild.id})')

        async def on_member_join(self, member):
            await member.create_dm()
            await member.dm_channel.send(
                f'Здравствуйте, {member.name}, как поживаете?'
            )

    async def on_message(self, message):
        if message.author == self.user:
            return

        logger.info(
            f"{message.channel} :: {message.author} :: {message.content}"
            f" :: {message.type} :: {message.components} :: {' ;; '.join(message.attachments) if message.attachments else None}"
            f" :: {' ;; '.join(message.embeds) message.embeds else None}  :: {message.created_at}")
        if message.content or message.attachments:
            print(message.jump_url)
            dbapi.add_message(message)


intents = discord.Intents.all()
intents.members = True
client = YLBotClient(intents=intents)
client.run(TOKEN)
