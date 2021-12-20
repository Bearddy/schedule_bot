import discord
import asyncio
import os


from os import listdir
from random import *
from discord.ext.commands import Bot, Context

bot = Bot(command_prefix='!!')


for filename in listdir('cog'):
    if filename.endswith('.py'):
        bot.load_extension(f'cog.{filename[:-3]}')
        print(f'Cog {filename}을/를 가져왔습니다')

@bot.event
async def on_ready():
    
    print(bot.user.name)
    print('봇이 시작됨')
    game = discord.Game('!!헬프 로 도움말을 확인해보세요')
    await bot.change_presence(status=discord.Status.online, activity=game)


bot.run(os.environ['bot_token'])


