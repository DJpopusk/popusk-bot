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
        super().__init__(intents=intents)
        self.is_game = False
        self.game = None
        self.p1id = None
        self.p2id = None
        self.ordr = None

    async def on_ready(self):
        logger.info(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            logger.info(
                f'{self.user} подключились к чату:\n'
                f'{guild.name}: (id: {guild.id})')

        async def on_member_join(self, member):
            await member.create_dm()
            await member.channel.send(
                f'Здравствуйте, {member.name}, хотите поиграть в Соедини 4?'
            )

    async def on_message(self, message):
        if message.author == self.user:
            return

        logger.info(
            f"{message.channel} :: {message.author} :: {message.content}"
            f" :: {message.type} :: {message.components} :: {' ;; '.join(message.attachments) if message.attachments else None}"
            f" :: {' ;; '.join(message.embeds) if message.embeds else None}  :: {message.created_at} :: self.is_game :: {self.is_game}")
        if 'да' in message.content.lower() and not self.is_game:
            self.is_game = True
            await message.channel.send(
                f'Хорошо, начнём'
            )
            self.game = connect4.Game()
            await message.channel.send(
                f'выбираем колонну для заполнения'
            )
            self.game.p1 = self.p1id = message.author
            self.ordr = 1
        elif self.is_game:
            print(self.ordr)
            if self.ordr == 1:
                if message.author == self.p1id:
                    try:
                        c = int(message.content)
                        self.game.move(c - 1, 't1')
                        await message.channel.send(self.game.draw())
                        if self.game.win():
                            self.p1id = None
                            self.p2id = None
                            self.game = None
                            self.is_game = None
                    except TypeError:
                        await message.channel.send(f'Только целые числа')
                        return
                else:
                    await message.channel.send(f'ходить за других нельзя')
                    return
                self.ordr = 2
            elif self.ordr == 2:
                if self.p2id is None and message.author != self.p1id:
                    self.game.p2 = self.p2id = message.author
                elif message.author == self.p1id:
                    await message.channel.send(f'ходить за других нельзя')
                if message.author == self.p2id:
                    try:
                        c = int(message.content)
                        self.game.move(c - 1, 't2')
                        await message.channel.send(self.game.draw())
                        if self.game.win():
                            self.p1id = None
                            self.p2id = None
                            self.game = None
                            self.is_game = None
                    except ValueError:
                        await message.channel.send(f'Только целые числа')
                        return
                else:
                    await message.channel.send(f'ходить за других нельзя')
                    return
                self.ordr = 1
                    

intents = discord.Intents.all()
intents.members = True
client = YLBotClient(intents)
client.run(TOKEN)
