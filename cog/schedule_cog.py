import discord
from discord.ext import tasks
from discord.ext.commands import Cog, Bot, command, Context
from discord.ext.commands.errors import BadArgument, CommandError, CommandNotFound
import datetime
import openpyxl



wb = openpyxl.load_workbook('classes.xlsx')


ws1 = wb['schedule']
ws2 = wb['vacation']

dateDict = {0: 'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'Sat', 6:'Sun'}
weekDict = {1: '월요일', 2:'화요일', 3:'수요일', 4:'목요일', 5:'금요일', 6:'토요일', 7:'일요일'}
dayDict = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
class_list = {'한국어', '수학', '국어', '물리', '화학', '영어', '작문', '체육', '생물'}


class 시간표(Cog):
    
    @command(pass_context = True)
    async def 저장(self, ctx: Context, cur_date: int, section_num: int, lesson):
        if ctx.author.guild_permissions.administrator:
            if cur_date < 6 and cur_date > 0:
                if section_num < 8 and section_num > 0:
                    cell_name = str(dateDict[cur_date] + str(section_num))
                    ws1[cell_name] = lesson
                    wb.save('classes.xlsx')
                    await ctx.send(f"{weekDict[cur_date]}의 {section_num}교시는 {lesson}으로 설정되었습니다")
                else:
                    await ctx.send("몇교시를 입력하셨는지 다시 확인해주세요")
            else:
                await ctx.send("요일을 다시 확인해주세요")
        else:
            await ctx.send("관리자 권한이 없습니다!")
        
    
    @command(pass_context = True)
    async def 방학(self, ctx: Context, from_year: int, from_mon: int, from_day: int, end_year: int, end_mon: int, end_day: int):
        if ctx.author.guild_permissions.administrator:
        
            date_diff = cal_date(end_year, end_mon, end_day, from_year, from_mon, from_day)
            if date_diff >= 0:
                await ctx.send("날짜를 다시 확인해주세요")
            else:
                ws2['A1'] = from_year
                ws2['A2'] = from_mon
                ws2['A3'] = from_day
                ws2['B1'] = end_year
                ws2['B2'] = end_mon
                ws2['B3'] = end_day
                await ctx.send(f"방학은 {from_year}년 {from_mon}월 {from_day}일 부터 {end_year}년 {end_mon}월 {end_day}일 까지로 설정되었습니다")
                wb.save('classes.xlsx')
                
        else:
            await ctx.send("관리자 권한이 없습니다")
    
            
        
    @command(pass_context = True)
    async def 지금(self, ctx: Context):
        time = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
        week_num = time.weekday()
        week = dateDict[time.weekday()]
        
        hour = time.hour
        min = time.minute
        
        
        index_num = 8
        index_num = time_to_section(hour, min)
        
        vaca_date_diff = cal_date(ws2['A1'].value, ws2['A2'].value, ws2['A3'].value, ws2['B1'].value, ws2['B2'].value, ws2['B3'].value)
        now = time
        to_vaca_date_diff = cal_date(ws2['A1'].value, ws2['A2'].value, ws2['A3'].value, now.year, now.month, now.day)
        
        
        if to_vaca_date_diff < 0 or to_vaca_date_diff > vaca_date_diff:
            if week == 'Sat' or week == 'Sun':
                await ctx.send(f"휴일에는 수업이없습니다")
            else :
                if index_num < 8 :
                    cell_name = str(dateDict[week_num] + str(index_num))
                    await ctx.send(f"{ws1[cell_name].value}")
                    await ctx.send(f"{class_num(ws1[cell_name].value)}")
                else:
                    await ctx.send(f"수업이 없습니다")
        else:
            await ctx.send("방학에는 수업이없습니다")
            
            
        
        
    @command(pass_context = True)
    async def 다음(self, ctx: Context):
        time = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
        second_time = datetime.datetime.utcnow() + datetime.timedelta(hours=9,minutes=11)
        week_num = time.weekday()
        week = dateDict[time.weekday()]
        
        hour = time.hour 
        min = time.minute
        
        index_num = 8
        index_num = time_to_section(hour, min)
        second_index_num = time_to_section(second_time.hour, second_time.min)
        
        
            
        
        if hour == 8 and min <= 59 and min > 40:
            index_num = 1
        else:
            if not index_num == second_index_num:
                index_num = second_index_num
            else:
                if index_num < 8:
                    index_num += 1
        
        vaca_date_diff = cal_date(ws2['A1'].value, ws2['A2'].value, ws2['A3'].value, ws2['B1'].value, ws2['B2'].value, ws2['B3'].value)
        now = time
        to_vaca_date_diff = cal_date(ws2['A1'].value, ws2['A2'].value, ws2['A3'].value, now.year, now.month, now.day)
        
        
        if to_vaca_date_diff < 0 or to_vaca_date_diff > vaca_date_diff:
            if week == 'Sat' or week == 'Sun':
                await ctx.send(f"휴일에는 수업이없습니다")
            else :
                if index_num < 8 :
                    cell_name = str(dateDict[week_num] + str(index_num))
                    await ctx.send(f"{ws1[cell_name].value}")
                    await ctx.send(f"{class_num(ws1[cell_name].value)}")

                else:
                    await ctx.send(f"수업이 없습니다")
        else:
            await ctx.send("방학에는 수업이없습니다")

    @command(pass_context = True)
    async def 아까(self, ctx: Context):
        time = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
        second_time = datetime.datetime.utcnow() + datetime.timedelta(hours=9,minutes=-11)
        week_num = time.weekday()
        week = dateDict[time.weekday()]
        
        hour = time.hour 
        min = time.minute
        
        index_num = 8
        index_num = time_to_section(hour, min)
        second_index_num = time_to_section(second_time.hour, second_time.min)
        
        
            
        
        
        if not index_num == second_index_num:
            index_num = second_index_num
        else:
            if index_num < 8:
                index_num -= 1
                
        vaca_date_diff = cal_date(ws2['A1'].value, ws2['A2'].value, ws2['A3'].value, ws2['B1'].value, ws2['B2'].value, ws2['B3'].value)
        now = time
        to_vaca_date_diff = cal_date(ws2['A1'].value, ws2['A2'].value, ws2['A3'].value, now.year, now.month, now.day)
        
        if to_vaca_date_diff < 0 or to_vaca_date_diff > vaca_date_diff:
            if week == 'Sat' or week == 'Sun':
                await ctx.send(f"휴일에는 수업이없습니다")
            else :
                if index_num < 8 :
                    cell_name = str(dateDict[week_num] + str(index_num))
                    await ctx.send(f"{ws1[cell_name].value}")
                    await ctx.send(f"{class_num(ws1[cell_name].value)}")
                    

                else:
                    await ctx.send(f"수업이 없습니다")
        else:
            await ctx.send("방학에는 수업이없습니다")
            
    @command(pass_context = True)
    async def 특정(self, ctx: Context, delta: int):
        time = datetime.datetime.utcnow() + datetime.timedelta(hours=9,minutes=delta)
        week_num = time.weekday()
        week = dateDict[time.weekday()]
        
        hour = time.hour
        min = time.minute
        
        index_num = 8
        
        index_num = time_to_section(hour, min)
        

        vaca_date_diff = cal_date(ws2['A1'].value, ws2['A2'].value, ws2['A3'].value, ws2['B1'].value, ws2['B2'].value, ws2['B3'].value)
        now = time
        to_vaca_date_diff = cal_date(ws2['A1'].value, ws2['A2'].value, ws2['A3'].value, now.year, now.month, now.day)
        
        if to_vaca_date_diff < 0 or to_vaca_date_diff > vaca_date_diff:
            if week == 'Sat' or week == 'Sun':
                await ctx.send(f"휴일에는 수업이없습니다")
            else :
                if index_num < 8 :
                    cell_name = str(dateDict[week_num] + str(index_num))
                    if delta > 0 or delta < 0:
                        if delta > 0:
                            await ctx.send(f"{delta}분후의 수업 : {ws1[cell_name].value}")
                        elif delta < 0:
                            await ctx.send(f"{delta}분전의 수업 : {ws1[cell_name].value}")
                        await ctx.send(f"{class_num(ws1[cell_name].value)}")
                    elif delta == 0:
                        await ctx.send("그럴꺼면 !!지금 명령어를 치세요")

                else:
                    await ctx.send(f"수업이 없습니다")
        else:
            await ctx.send("방학에는 수업이없습니다")
    
    @command(pass_context = True)
    async def 그때(self, ctx: Context, week: str, section: int):
        
        if week == '월' or week == '월요일' or week == '1':
            cur_week = 'A'
        elif week == '화' or week == '화요일' or week == '2':
            cur_week = 'B'
        elif week == '수' or week == '수요일' or week == '3':
            cur_week = 'C'
        elif week == '목' or week == '목요일' or week == '4':
            cur_week = 'D'
        elif week == '금' or week == '금요일' or week == '5':
            cur_week = 'E'
        else:
            cur_week = 'dump'
        
        if not cur_week == 'dump':
            if section < 8 and section > 0:
                vaca_date_diff = cal_date(ws2['A1'].value, ws2['A2'].value, ws2['A3'].value, ws2['B1'].value, ws2['B2'].value, ws2['B3'].value)
                now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
                to_vaca_date_diff = cal_date(ws2['A1'].value, ws2['A2'].value, ws2['A3'].value, now.year, now.month, now.day)
                
                if to_vaca_date_diff < 0 or to_vaca_date_diff > vaca_date_diff:
                    cell_name = str(cur_week + str(section))
                    await ctx.send(f"{ws1[cell_name].value}")
                    await ctx.send(f"{class_num(ws1[cell_name].value)}")
                else:
                    await ctx.send("방학에는 수업이없습니다")    
            else:
                await ctx.send("몇교시를 입력하셨는지 다시 확인해주세요")
        else:
            await ctx.send("그날에는 수업이없습니다")     
                        
    @command(pass_context = True)
    async def 전부(self, ctx:Context):
        
        embed = discord.Embed(title="✨✨시간표✨✨", description="모든 시간표 나열", color=0x00ffff)
            
#        embed.add_field(name=" 요일", value="     월       화       수       목       금", inline=False)
#        embed.add_field(name="1교시", value="   생물     국어     생물     생물     화학", inline=False)
#        embed.add_field(name="2교시", value="   물리     생물     물리   한국어     수학", inline=False)
#        embed.add_field(name="3교시", value=" 한국어     수학     국어     화학     국어", inline=False)
#        embed.add_field(name="4교시", value="   국어     체육     수학     영어     영어", inline=False)
#        embed.add_field(name="5교시", value="   영어     영어     화학     수학     물리", inline=False)
#        embed.add_field(name="6교시", value="   수학   컴퓨터     영어     물리   컴퓨터", inline=False)
#        embed.add_field(name="7교시", value="   작문     화학   한국어     국어   한국어", inline=False)
        
        embed.add_field(name="월요일", value="생물    물리  한국어  국어  영어    수학    작문", inline=False)
        embed.add_field(name="화요일", value="국어    생물    수학  체육  영어  컴퓨터    화학", inline=False)
        embed.add_field(name="수요일", value="생물    물리    국어  수학  화학    영어  한국어", inline=False)
        embed.add_field(name="목요일", value="생물  한국어    화학  영어  수학    물리    국어", inline=False)
        embed.add_field(name="금요일", value="화학    수학    국어  영어  물리  컴퓨터  한국어", inline=False)

        embed.set_footer(text="고2-3")

        await ctx.send(embed=embed)
        
    @command(pass_context = True)
    async def 코드(self, ctx: Context, class_name: str):
        if class_name in class_list:
            await ctx.send(f"{class_num(class_name)}")
        else:
            await ctx.send("저희반은 그런수업이 없습니다")
            
    @command(pass_context = True)
    async def 과목(self, ctx: Context):
        text = '저희반은 '
        for classes in class_list:
            text = text + classes + ', ' 
        
        text = text[:-2] + "들이 있습니다"
        await ctx.send(text)
        
        
            
        
        
        


def setup(bot: Bot):
    bot.add_cog(시간표())
    
    

def class_num(class_name: str):
    text = " "
    if class_name == '한국어':
        text = "834 139 1392"
    elif class_name == '국어' or class_name == '작문':
        text = "442 784 6158"
    elif class_name == '컴퓨터':
        text = "998 667 8365"
    elif class_name == '물리':
        text = "365 177 6358"
    elif class_name == '영어':
        text = "324 652 7160"
    elif class_name == '수학':
        text = "482 902 3938"
    elif class_name == '화학':
        text = "235 936 9431"
    elif class_name == '생물':
        text = "773 563 6517"
    elif class_name == '체육':
        text = "952 019 8686"
    
    return text


def time_to_section(hour: int, min: int):
    num = 8
    if hour == 9 and min <= 45 :
        num = 1
    elif (hour == 9 and min > 55 ) or (hour == 10 and min <= 40):
        num = 2
    elif (hour == 10 and min > 50 ) or (hour == 11 and min <= 35):
        num = 3
    elif (hour == 11 and min > 45 ) or (hour == 12 and min <= 30):
        num = 4
    elif (hour == 13 and min > 30 ) or (hour == 14 and min <= 15):
        num = 5
    elif (hour == 14 and min > 25 ) or (hour == 15 and min <= 10):
        num = 6
    elif (hour == 15 and min > 20 ) or (hour == 16 and min <= 5):
        num = 7
    else:
        num = 8
    
    return num
    

def cal_date(from_year: int, from_mon: int, from_day: int, to_year: int, to_mon: int, to_day: int):
    date_to = datetime.datetime(to_year, to_mon, to_day, 0, 0, 0)
    date_from = datetime.datetime(from_year, from_mon, from_day, 0, 0, 0)
    date_diff = date_to - date_from
    
    return date_diff.days
    
    