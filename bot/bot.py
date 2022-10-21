import getpass
import json
import time
import os
import sys
import discord
from discord import CategoryChannel, option
from discord.ext import commands, tasks
import datetime
import time

from edookit.scraper import Scraper
import outlook.calendar as cal
import edookit.gradeaverage as ga


bot = commands.Bot(command_prefix = ':', activity=discord.Activity(type=discord.ActivityType.watching, name="/help"))
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Bot online.')

@bot.slash_command(
    name="help",
    description="Shows the list of availible commands",
)
async def help(ctx: discord.ApplicationContext):
    embed = discord.Embed(title=f"List of commands")
    embed.set_author(name=f"made by azurim#8202", url=f"https://www.instagram.com/mr_rohland/")
    embed.add_field(name="```/avrg```", value="Průměr známek", inline=False)
    await ctx.respond(embed=embed)

@bot.slash_command(
    name="avrg",
    description="Průměr známek",
)
@option(
    name="access1",description="Access Code 1",required=True, option_type=3
)
@option(
    name="access2",description="Access Code 2",required=True, option_type=3
)
async def help(ctx: discord.ApplicationContext, access1: str, access2: str):
    embed = discord.Embed(title=f"Průměr známek",timestamp=datetime.datetime.utcnow(), description="Scraping and calculating all the data...")
    embed.set_author(name=f"made by azurim#8202", url=f"https://www.instagram.com/mr_rohland/")
    await ctx.respond(embed=embed)

    embed = discord.Embed(title=f"Průměr známek",timestamp=datetime.datetime.utcnow(), description=f"Data for: {ctx.author}")

    st = time.time()
    try:
        r = ga.gradeAverage(access1, access2)
        for i in r:
            for subj, avrg in i.items():
                if avrg < 3:
                    embed.add_field(name=subj.removesuffix('- 5A8'), value=f"```py\n{avrg}```")
                else:
                    embed.add_field(name=subj.removesuffix('- 5A8'), value=f"```fix\n{avrg}```")

    except Exception as e:
        print(e)
        embed.add_field(name="Exception occured.", value="Could be caused by using invalid access codes.")

    et = time.time()

    elapsed_time = et - st

    embed.add_field(name="Time taken", value=f"```{elapsed_time}```", inline="False")
    await ctx.edit(embed=embed)

def runbot(token: str):
    bot.run(token)