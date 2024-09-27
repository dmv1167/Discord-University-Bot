import discord, os
from discord.ext import commands, tasks
from news import set_timeout, get_news_embed, NewsView, get_timeout
from bus import bus_alert, bus_info
from datetime import time
from random import choice
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

DINING_LOCATIONS = {"breakfast": ["Beanz", "Ctrl Alt Deli", "College Grind"],
                    "lunch": ["Commons", "Crossroads", "Salsa's", "Gracie's"],
                    "dinner": ["Commons", "Crossroads", "Salsa's", "Gracie's"],
                    "academic": ["Crossroads", "Salsa's", "Ctrl Alt Deli"],
                    "dorms": ["Commons", "Beanz", "College Grind", "Gracie's"]}


bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    await bot.change_presence(status=discord.Status.online)


@bot.hybrid_command(help="Displays current headline news")
async def news(ctx):
    message = await ctx.send(embed=get_news_embed(), view=NewsView(timeout=get_timeout()))
    NewsView.message = message


@bot.command(hidden=True)
async def timeout(ctx, length: int):
    try:
        if isinstance(int(length), int):
            if int(length) == -1:
                set_timeout(None)
                await ctx.send('Timeout Disabled')
            else:
                set_timeout(int(length))
                await ctx.send(f'Timeout set to {length} seconds')
    except:
        await ctx.send('Invalid Time Period')


@bot.hybrid_command(hidden=True)
async def sync(ctx):
    try:
        synced = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f'{len(synced)} Commands Synced')
    except:
        await ctx.send('Unable to sync commands!')


@bot.command(help="Helps decide where to eat on campus\nUsage: eat {dorms/academic} {breakfast/lunch/dinner}", usage="eat {dorms/academic} {breakfast/lunch/dinner}")
async def eat(ctx,
              side:str =commands.Parameter(name='side', kind=commands.Parameter.KEYWORD_ONLY, description='Side of campus', default=None),
              type:str =commands.Parameter(name='type', kind=commands.Parameter.KEYWORD_ONLY, description='Type of food', default=None)):
    if side is None or type is None:
        await ctx.send(f'Usage: {eat.usage}')
    else:
        options = [location for location in DINING_LOCATIONS[side] if location in DINING_LOCATIONS[type]]
        await ctx.send("Eat at " + choice(options))


@tasks.loop(time=time(hour=8, minute=00))
async def busTimer(ctx):
    await ctx.send(embed=bus_alert())


@bot.command(help="Displays any current bus alerts")
async def bus(ctx):
    await ctx.send(embed=bus_alert())


@bot.command(help="Provides links to bus schedules, specify number for stop info", aliases=['sched'])
async def schedule(ctx, num:int =commands.Parameter(name = 'num', kind=commands.Parameter.KEYWORD_ONLY, description='Schedule number', default = 0)):
    await ctx.send(embed=bus_info(num))

if __name__ == '__main__':
    load_dotenv()
    bot.run(os.getenv('API_KEY'))
