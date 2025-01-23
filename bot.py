import discord, os
from discord.ext import commands, tasks
from bus import bus_alert#, bus_info
from datetime import time
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    await bot.change_presence(status=discord.Status.online)


@bot.hybrid_command(hidden=True)
async def sync(ctx):
    try:
        synced = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f'{len(synced)} Commands Synced')
    except:
        await ctx.send('Unable to sync commands!')


@tasks.loop(time=time(hour=8, minute=00))
async def busTimer(ctx):
    await ctx.send(embed=bus_alert())


@bot.command(help="Displays any current bus alerts")
async def bus(ctx):
    await ctx.send(embed=bus_alert())

"""
READ INSTRUCTIONS ON WEBSCRAPING
@bot.command(help="Provides links to bus schedules, specify number for stop info", aliases=['sched'])
async def schedule(ctx, num:int =commands.Parameter(name = 'num', kind=commands.Parameter.KEYWORD_ONLY, description='Schedule number', default = 0)):
    await ctx.send(embed=bus_info(num))
"""

if __name__ == '__main__':
    load_dotenv()
    bot.run(os.getenv('API_KEY'))
