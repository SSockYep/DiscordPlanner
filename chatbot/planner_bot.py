import discord
from discord.ext import commands, tasks
import pymongo
from pymongo import MongoClient
from constants import *
import time
import datetime
import requests
import json


cluster = MongoClient(MONGO_URL)
db = cluster["DiscordPlannerDB"]
collection = db["Plans"]

intents = discord.Intents(messages=True, guilds=True, members=True)
bot = commands.Bot(command_prefix='!', intents=intents)


@tasks.loop(minutes=30)
async def send_alarm_loop():
    now = datetime.datetime.now()
    query = {'time': {'$gte': now, '$lt': now+datetime.timedelta(minutes=30)}}
    plans = collection.find(query)
    for plan in plans:
        time = plan['time']
        guild = bot.get_guild(plan['guild'])
        name = plan['name']
        attendee_ids = plan['attendee']

        message = f"{time}에 {guild.name}서버에서 {name}에 참여할 예정입니다."
        for attendee in attendee_ids:
            dm_to = guild.get_member(attendee)
            await dm_to.send(message)


@bot.command(name='도움말')
async def _help(ctx, *args):
    embed = discord.Embed(title="명령어모음")
    embed.add_field(name='!도움말', value='명령어 모음', inline=False)
    embed.add_field(name='!목록', value='현재 계획 목록 확인', inline=False)
    embed.add_field(
        name='!생성', value='!생성 <계획명> <YYYY-mm-dd HH:MM> <최대 참가 인원(옵션)>\nYYYY년 mm월 dd일 HH시 MM분에 <계획명> 계획 생성', inline=False)
    embed.add_field(
        name='!참가', value='!참가 <계획명>으로 <계획명>에 참가 신청', inline=False)
    embed.add_field(
        name='!참가자', value='!참가자 <계획명>으로 <계획명>에 참가하는 사람 목록 확인', inline=False)
    await ctx.send(embed=embed)


# @bot.command()
# async def help(ctx):
#     await _help()


@bot.command(name='목록')
async def check_plans(ctx):
    now = datetime.datetime.now()
    guild_info = {'guild': ctx.guild.id, 'time': {"$gte": now}}
    plans = collection.find(guild_info).sort('time', pymongo.ASCENDING)
    print(type(plans))
    await ctx.send('{guild_name}의 계획 로딩중'.format(guild_name=ctx.guild.name))
    embed = discord.Embed(title='계획 목록')
    for plan in plans:
        text = f'시각: {plan["time"]}\n인원: {len(plan["attendee"])}'
        if plan.get('max_attendee'):
            text += '/' + str(plan['max_attendee'])
        text += '\n'
        embed.add_field(name=plan['name'], value=text, inline=False)
    if len(embed.fields) == 0:
        embed.add_field(name='추가된 계획이 없습니다.', value='"!생성"으로 계획을 추가하세요!')
    await ctx.send(embed=embed)


@ bot.command(name='참가자')
async def check_attendee(ctx, name: str):
    now = datetime.datetime.now()
    query = {'guild': ctx.guild.id, 'name': name, 'time': {"$gte": now}}
    plan = collection.find_one(query)
    if not plan:
        ctx.send(f'{name} 계획이 없습니다.')
        return
    attendee_id = plan['attendee']
    embed = discord.Embed(title=f'{name}의 참가자 목록')

    attendee = [ctx.guild.get_member(
        x).display_name for x in attendee_id if x != ctx.guild.owner.id]
    for i in attendee_id:
        if i == ctx.guild.owner.id:
            attendee.append(ctx.guild.owner.display_name)
    for a in attendee:
        embed.add_field(name=a, value=a)
    await ctx.send(embed)


@ bot.command(name='생성')
async def make_plans(ctx, name: str, date: str, time: str, max_attendee=0):
    print('계획생성')
    try:
        time_info = datetime.datetime.strptime(date + time, '%Y-%m-%d%H:%M')
    except:
        await ctx.send('입력을 확인해주세요.')
        return
    now = datetime.datetime.now()
    if time_info < now:
        await ctx.send('현재 시각 이후의 계획만 만들 수 있습니다.')
        return
    if len(list(collection.find({'guild': ctx.guild.id, 'time': {"$gte": now}, 'name': name}))) != 0:
        await ctx.send(f'"{name}"이(가) 이미 있습니다.')
        return
    plan_info = {
        'name': name, 'time': time_info, 'guild': ctx.guild.id, 'attendee': [ctx.author.id]}
    if max_attendee:
        plan_info['max_attendee'] = int(max_attendee)
    collection.insert_one(plan_info)
    await ctx.send(f'{name}이(가) 생성되었습니다.')


@bot.command(name="참가")
async def attend_plan(ctx, name):
    now = datetime.datetime.now()
    query = {'guild': ctx.guild.id, 'name': name, 'time': {"$gte": now}}
    plan = collection.find_one(query)
    if plan.get('max_attendee') and len(plan['attendee']) >= plan['max_attendee']:
        await ctx.send(f'{name}의 참가자가 꽉 찼습니다.')
        return
    collection.find_one_and_update(
        query, {'$addToSet': {'attendee': ctx.author.id}})
    print(type(plan))
    await ctx.send(f'{ctx.author.display_name}님 {name} 참가 신청 완료')


@bot.command()
async def member(ctx):
    display_names = [x.display_name for x in ctx.guild.members]
    print(ctx.guild.members)
    text = ''
    for name in display_names:
        text = text + name + ' '
    await ctx.send(text)


@bot.event
async def on_member_remove(member):
    query = {'guild': member.guild.id, 'attendee': member.id}
    plans = collection.find(query)
    for plan in plans:
        attendee = plan['attendee']
        collection.find_one_and_update(
            plan, {'$pull': {'attendee': member.id}})


@bot.event
async def on_guild_join(guild):
    api_url = BASE_URL + '/api/guild/create'
    member_ids = []
    for memeber in guild.members:
        member_ids.append({'uid': member.id, 'name': member.name})
    data = {
        'gid': guild.id,
        'name': guild.name,
        'members': members,
    }
    print(data)
    response = requests.post(api_url, data=data)  # await?
    response.raise_for_status()
    print(response.json())


@bot.event
async def on_member_join(member):
    print('%s join' % member.name)
    user_data = {'uid': member.id, 'name': member.name}
    join_data = {
        'gid': member.guild.id,
        'uid': member.id,
    }
    response = requests.post(BASE_URL + '/api/user/create', data=user_data)
    response.raise_for_status()
    print(response.json())
    response = requests.post(BASE_URL + '/api/user/join_guild', data=join_data)
    response.raise_for_status()
    print(response.json())


@bot.event
async def on_ready():
    print('Logging on...')
    for guild in bot.guilds:
        member_response_list = []
        response = requests.post(
            BASE_URL + '/api/guild/create',
            data={
                'gid': guild.id,
                'name': guild.name,
            }
        )
        response.raise_for_status()
        print(response.json())
        for m in guild.members:
            response = requests.post(
                BASE_URL + '/api/user/create_and_join_guild',
                data={
                    'uid': m.id,
                    'name': m.name,
                    'gid': guild.id,
                }
            )
            response.raise_for_status()

            member_response_list.append(response.json())
        print(member_response_list)

    print('Logged on as', bot.user)
    send_alarm_loop.start()


bot.run(DISCORD_TOKEN)
