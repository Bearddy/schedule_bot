import discord
from discord.ext.commands import Cog, Bot, command, Context
from discord.ext.commands.core import group
from discord.ext.commands.errors import BadArgument, CommandError, CommandNotFound
from random import *
import datetime

weekDict = {1: '월요일', 2:'화요일', 3:'수요일', 4:'목요일', 5:'금요일', 6:'토요일', 7:'일요일'}

class 유용한기능(Cog):

    @command(pass_context = True)
    async def 청소(self, ctx: Context, count: int):

        """
        채팅청소를 해준다
        """

        if ctx.author.guild_permissions.administrator:
            if count < 21 and count > 0 :
                await ctx.channel.purge(limit=count + 1)
                await ctx.send(str(count) + "개의 메시지를 청소했습니다")
            elif count < 0 or count > 20:
                if count > 20:
                    await ctx.send("그렇게나 많은 메시지를 지울필요는 없어보이는데요?")
                elif count < 0:
                    count *= -1
                    await ctx.channel.purge(limit=count+1)
                    await ctx.send(str(count) + "개의 메시지를 청소했습니다")
        else:
            await ctx.send("관리자 권한이 없습니다")


    @command(pass_context = True)
    async def 투표(self, ctx: Context, *, list: str):
        emoji = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣']
        vote_list = list.split("/")
        if(len(vote_list) > 6):
            await ctx.send("투표 항목이 너무 많으면 도배가 될수있으므로 5개 이하로 해주세요")
        else:
            embed = discord.Embed(title="🎉투표🎉", description="**" + vote_list[0] + "**", color=0x00ff00)
            
            for i in range(1, len(vote_list)):
                embed.add_field(name="ㅤ", value=str(i) + "." + vote_list[i], inline=False)
            msg = await ctx.send(embed=embed)
            
            for i in range(0, len(vote_list)-1):
                await msg.add_reaction(emoji[i])

    
    @command(pass_context = True)
    async def 시간(self, ctx: Context):
        time = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
        week = weekDict[time.weekday() + 1]
        hour = time.hour
        min = time.minute
        await ctx.send(f"{hour}시 {min}분 {week}")
        
    @command(pass_context = True)
    async def 숫자(self, ctx: Context, num1: int, num2: int):
        if num1 < num2:

            if num2 < 2147483647 and num2 > 0 :
                rand = int(random() * (num2 - num1 + 1)) + num1
                await ctx.send(f"{num1}부터 {num2}중에서 랜덤으로 {rand} 이/가 나왔습니다")
            elif num2 < 0 or num2 > 2147483647:
                if num2 < 0:
                    await ctx.send("음수는 계산 못함")    
                elif num2 > 2147483647:
                    await ctx.send("정수값이 너무 크면 계산 못함")
        else :
            await ctx.send("두번째 숫자가 더작습니다")

    @command(pass_context = True)
    async def 단어(self, ctx: Context, words: str):
        list = words.split("/")
        rand = int(random() * len(list))

        await ctx.send(f"단어 리스트중에서 \"{list[rand]}\"이/가 나왔습니다")
        
    @command()
    async def 헬프(self, ctx: Context):
        embed = discord.Embed(title="💡명령어 리스트💡", description=" ", color=0x00ffff)
            
        embed.add_field(name="!!지금", value="지금이 무슨 수업인지 알려준다", inline=False)
        embed.add_field(name="!!아까", value="아까가 무슨 수업인지 알려준다", inline=False)
        embed.add_field(name="!!다음", value="다음이 무슨 수업인지 알려준다", inline=False)
        embed.add_field(name="!!과목", value="고2-3반은 무슨 과목들이 있는지 알려준다", inline=False)
        embed.add_field(name="!!전부", value="모든 시간표를 보여준다", inline=False)
        embed.add_field(name="!!코드 [과목]", value="[과목]의 줌코드를 알려준다", inline=False)
        embed.add_field(name="!!그때 [요일] [교시]", value="[요일]의 [교시]때가 무슨 수업인지 알려준다", inline=False)
        embed.add_field(name="!!시간", value="몇시 인지 알려준다", inline=False)
        embed.add_field(name="!!투표 [질문/항목1/항목2/항목3....]", value="[항목1 ~... 마지막 항목]까지 투표를 진행합니다", inline=False)
        embed.add_field(name="!!청소 [숫자]", value="[숫자] 만큼의 채팅을 지웁니다", inline=False)
        embed.add_field(name="!!숫자 [숫자1] [숫자2]", value="[숫자1]부터 [숫자2]에서 랜덤으로 하나를 배출합니다", inline=False)
        embed.add_field(name="!!단어 [단어1/단어2/단어3...]", value="[단어1, 단어2, 단어3 ....] 중에서 랜덤으로 하나를 배출합니다", inline=False)
        
        embed.set_footer(text="Made by 곰띠/Bearddy#4453", icon_url="https://ifh.cc/g/nxRpdO.png")
        
        await ctx.send(embed=embed)
    
    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        if isinstance(error, CommandNotFound):
            await ctx.send('해당 명령어가가 존재하는지 확인해주세요')
        elif isinstance(error, BadArgument):
            await ctx.send('값을 제대로 대입하셨나요?')
        else:
            await ctx.send('명령어 실행중 알수없는 오류가 발생했습니다')
    
   
        
        

def setup(bot: Bot):
    bot.add_cog(유용한기능())