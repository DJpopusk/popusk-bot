import discord
from TOKEN import TOKEN
import logging
import sqlite3
import dbapi
import connect4

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
    def __init__(self, intents):
        super().__init__(intends)
        is_game = False
        game = None
        p1id = None
        p2id = None
        ordr = None

    async def on_ready(self):
        logger.info(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            logger.info(
                f'{self.user} подключились к чату:\n'
                f'{guild.name}: (id: {guild.id})')

        async def on_member_join(self, member):
            await member.create_dm()
            await member.dm_channel.send(
                f'Здравствуйте, {member.name}, хотите поиграть в Соедини 4?'
            )

    async def on_message(self, message):
        if message.author == self.user:
            return

        logger.info(
            f"{message.channel} :: {message.author} :: {message.content}"
            f" :: {message.type} :: {message.components} :: {' ;; '.join(message.attachments) if message.attachments else None}"
            f" :: {' ;; '.join(message.embeds) if message.embeds else None}  :: {message.created_at}")
        if 'да' in message.content.lower() and not is_game:
            self.is_game = True
            await message.author.dm_channel.send(
                f'Хорошо, начнём'
            )
            self.game = connect4.Game()
            await message.author.dm_channel.send(
                f'выбираем колонну для заполнения'
            )
            self.game.p1 = self.p1id = message.author
        elif game:
            if self.ordr == 1:
                if message.author == self.p1id:
                    try:
                        c = int(message.content.split(','))
                        self.game.move(c, 't1')
                        self.game.draw()
                        if self.game.win():
                            self.p1id = None
                            self.p2id = None
                            self.game = None
                            self.is_game = None
                    except ValueError:
                        await message.author.dm_channel.send(f'Только целые числа')
                        return
                else:
                    await message.author.dm_channel.send(f'ходить за других нельзя')
                    return
                self.ordr == 2
            elif self.ordr == 2:
                if self.p2id and message.author != self.p1id:
                    self.game.p2 = self.p2id = message.author
                elif message.author == self.p1id:
                    await message.author.dm_channel.send(f'ходить за других нельзя')
                if message.author == self.p2id:
                    try:
                        c = int(message.content.split(','))
                        self.game.move(c, 't2')
                        if self.game.win():
                            self.p1id = None
                            self.p2id = None
                            self.game = None
                            self.is_game = None
                    except ValueError:
                        await message.author.dm_channel.send(f'Только целые числа')
                        return
                elif message.author == self.p2id:
                    await message.author.dm_channel.send(f'ходить за других нельзя')
                    return
                    

intents = discord.Intents.all()
intents.members = True
client = YLBotClient(intents=intents)
client.run(TOKEN)
