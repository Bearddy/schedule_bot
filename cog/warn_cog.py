import discord
from discord.ext.commands import Cog, Bot, command, Context
from discord.ext.commands.core import group
import openpyxl

wb = openpyxl.load_workbook('warn.xlsx')


ws1 = wb['Sheet1']
ws2 = wb['Sheet2']
alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

class 경고명령어(Cog):

    @group()
    async def 경고(self, ctx: Context):
        '''경고해줌'''

    @경고.command(pass_context = True)
    async def 주기(self, ctx, user: discord.User, amount: int, *, reason):
        if ctx.author.guild_permissions.administrator:
            if not user.guild_permissions.administrator:
                if reason is None:
                    await ctx.send("사유를 적으세요")
                    return

                
                for i in range(0, len(alpha)):
                    
                    if(ws1[str(alpha[i] + str('1'))].value is None):
                        ws1[alpha[i] + str('1')] = str(user.id)[0:10]
                        ws1[alpha[i] + str('4')] = str(user.id)[10:len(str(user.id))]
                        
                        if(ws1[alpha[i] + str('2')].value is None):
                            ws1[alpha[i] + str('2')] = amount;
                        else:
                            ws1[alpha[i] + str('2')] = ws1[alpha[i] + str('2')].value + amount
                        
                        check = True
                        j = 0
                        while (check):
                            j += 1
                            if(ws2[alpha[i] + str(j)].value is None):
                                ws2[alpha[i] + str(j)] = reason
                                check = False
                            
                        if ((ws1[alpha[i] + str('3')].value is None or ws1[alpha[i] + str('3')].value == False) and ws1[alpha[i] + str('2')].value >= 4):
                        
                            await user.send(f"경고 횟수가 4번이 됬으므로 \"{ctx.message.guild.name}\" 에서 추방 당하셨습니다")
                            await user.kick(reason=f"경고 횟수가 4번")
                            ws1[alpha[i] + str('3')] = True
                        if (ws1[alpha[i] + str('3')].value == True and ws1[alpha[i] + str('2')].value >= 7):

                            await user.send(f"경고 횟수가 7번이 됬으므로 \"{ctx.message.guild.name}\" 에서 밴 당하셨습니다")
                            await user.ban(reason=f"경고 횟수가 7번")
                            ws1[alpha[i] + str('3')] = False
                            
                        wb.save('warn.xlsx') 
                        await ctx.send(f"성공적으로 {user.name}에게 {amount}개의 경고를 부여했습니다")
                        await ctx.send(f"{user.name}님의 경고 횟수 : {ws1[alpha[i] + str('2')].value}번")
                        
                        break
                    elif(str(ws1[str(alpha[i] + str('1'))].value) + str(ws1[str(alpha[i] + str('4'))].value) == str(user.id)):
                        if(ws1[alpha[i] + str('2')].value is None):
                                ws1[alpha[i] + str('2')] = amount;
                        else:
                            ws1[alpha[i] + str('2')] = ws1[alpha[i] + str('2')].value + amount
                        
                        check = True
                        j = 0
                        while (check):
                            j += 1
                            if(ws2[alpha[i] + str(j)].value is None):
                                ws2[alpha[i] + str(j)] = reason
                                check = False
                            
                        if ((ws1[alpha[i] + str('3')].value is None or ws1[alpha[i] + str('3')].value == False) and ws1[alpha[i] + str('2')].value >= 4):
                        
                            await user.send(f"경고 횟수가 4번이 됬으므로 \"{ctx.message.guild.name}\" 에서 추방 당하셨습니다")
                            await user.kick(reason=f"경고 횟수가 4번")
                            ws1[alpha[i] + str('3')] = True
                        if (ws1[alpha[i] + str('3')].value == True and ws1[alpha[i] + str('2')].value >= 7):
                            
                            
                            await user.send(f"경고 횟수가 7번이 됬으므로 \"{ctx.message.guild.name}\" 에서 밴 당하셨습니다")
                            await user.ban(reason=f"경고 횟수가 7번")
                            ws1[alpha[i] + str('3')] = False
                            
                        wb.save('warn.xlsx') 
                        await ctx.send(f"성공적으로 {user.name}에게 {amount}개의 경고를 부여했습니다")
                        await ctx.send(f"{user.name}님의 경고 횟수 : {ws1[alpha[i] + str('2')].value}번")
                        break
                        
            else:
                await ctx.send("관리자권한이 있는사람한테는 경고를 못줍니다!")
        else:
            await ctx.send("관리자 권한이 없습니다!")

    @경고.command(pass_context = True)
    async def 확인(self, ctx, user:discord.User):
        warn_check = False
        for i in range(0, len(alpha)):
            if (str(user.id) == str(ws1[alpha[i] + str('1')].value) + str(ws1[str(alpha[i] + str('4'))].value)):
                if not int(ws1[alpha[i] + str('2')].value) == 0:
                    
                    j = 0
                    check = True
                    reason = ''
                    while (check):
                        j += 1
                        if(ws2[alpha[i] + str(j)].value is not None):
                            reason = reason + ws2[alpha[i] + str(j)].value + ","
                        else:
                            reason = reason[0:len(reason) - 1]
                            check = False
                    
                    embed = discord.Embed(title=f"{user.name}님의 경고판", description="　", color=0xff0000)
                    
                    embed.add_field(name="경고 횟수 : ", value=f"{ws1[alpha[i] + str('2')].value}번", inline=False)
                    embed.add_field(name="경고 사유:", value=f"{reason}", inline=False)
                    
                    embed.set_footer(text="버그제보는 곰띠/Bearddy#4453 로 해주세요", icon_url="https://ifh.cc/g/nxRpdO.png")
                    embed.set_thumbnail(url="https://ifh.cc/g/5LIwNe.jpg")

                    await ctx.send(embed=embed)
                    
                    warn_check = True
                    break   
        
        if(warn_check == False):
            await ctx.send(f"{user.name}님은 경고가 없는 클린한 사람입니다") 
            
    @경고.command(pass_context = True)
    async def 제거(self, ctx, user: discord.User, amount: int):
        if ctx.author.guild_permissions.administrator:
            warn_check = False
            for i in range(0, len(alpha)):
                if (str(user.id) == str(ws1[alpha[i] + str('1')].value) + str(ws1[str(alpha[i] + str('4'))].value)):
                    if not ws1[alpha[i] + str('2')].value == 0:
                        if ws1[alpha[i] + str('2')].value >= amount:
                            ws1[alpha[i] + str('2')] = ws1[alpha[i] + str('2')].value - amount
                            
                            await ctx.send(f"성공적으로 {user.name}의 경고횟수에서 {amount}을/를 뺐습니다")
                              
                        else:
                            ws1[alpha[i] + str('2')] = 0
                            await ctx.send(f"성공적으로 {user.name}의 경고횟수에서 {amount}을/를 뺐습니다")
                        
                        await ctx.send(f"{user.name}님의 경고 횟수 : {ws1[alpha[i] + str('2')].value}번")
                        wb.save('warn.xlsx') 
                        warn_check = True
                        break
                    
            if(warn_check == False):
                await ctx.send(f"{user.name}님은 아직 경고당한적이 없습니다")
        else:
            await ctx.send("관리자 권한이 없습니다!")


    


def setup(bot: Bot):
    bot.add_cog(경고명령어())
