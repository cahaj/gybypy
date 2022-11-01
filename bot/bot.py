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
import requests

from edookit.scraper import Scraper
import outlook.calendar as cal
import edookit.gradeaverage as ga

def inbotdir():
    dir = f"{os.getcwd()}\\bot"
    indir = os.listdir(dir)
    indir.remove("__pycache__")
    return indir

def writeable():
    list = inbotdir()
    for c, i in enumerate(list):
        if ".py" in i:
            del list[c]
    return list

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
async def avrg(ctx: discord.ApplicationContext, access1: str, access2: str):
    embed = discord.Embed(title=f"Průměr známek",timestamp=datetime.datetime.utcnow(), description="Scraping and calculating all the data...")
    await ctx.respond(embed=embed)

    embed = discord.Embed(title=f"Průměr známek",timestamp=datetime.datetime.utcnow(), description=f"Data for: {ctx.author}")

    st = time.time()
    try:
        r = ga.gradeAverage(access1, access2)
        for i in r:
            for subj, avrg in i.items():
                split = subj.split()
                possible = [*split[-1]]
                try:
                  int(possible[0])
                  subj = ' - '.join(subj.split(' - ')[:-1])
                except:
                  pass
                if avrg < 3:
                    embed.add_field(name=subj, value=f"```py\n{avrg}```")
                else:
                    embed.add_field(name=subj, value=f"```fix\n{avrg}```")

    except Exception as e:
        print(e)
        embed.add_field(name="Exception occured.", value="Could be caused by using invalid access codes.")

    et = time.time()

    elapsed_time = et - st

    embed.add_field(name="Time taken", value=f"```{elapsed_time}```", inline="False")
    await ctx.edit(embed=embed)


@bot.slash_command(
    name="download",
    description="Download",
)
@option(
    name="data",description="Data to download",required=True, option_type=3, choices = inbotdir()
)
@option(
    name="hidden",description="Hidden?",required=True, option_type=3, choices=["True", "False"]
)
async def download(ctx: discord.ApplicationContext, data: str, hidden: str):
    if hidden == "True":
        hide = True
    else:
        hide = False
    if ctx.author.id == 673799940560125952:
        try:
            file = data
            await ctx.respond(file=discord.File(f"bot/{file}"), ephemeral=hide)
        except Exception as e:
            print(e)
            await ctx.respond("Invalid file", ephemeral=hide)
    else:
        await ctx.respond("No permissions", ephemeral=True)

@bot.slash_command(name="write")
@option(
    "file",
    discord.Attachment,
    description="File",
)
@option(
    name="to",description="File",required=True, choices = writeable()
)
async def say(
    ctx: discord.ApplicationContext, file: discord.Attachment, to: str):
    if ctx.author.id == 673799940560125952:
        try:
            writeto=to
            r = requests.get(file.url)
            data = r.json()
            print(data)
            with open(writeto, "w") as obj:
                json.dump(data, obj)
            await ctx.respond(f"Written {file.url} to {writeto}")
        except Exception as e:
            print(e)
            await ctx.respond("Exception occured")
    else:
        ctx.respond("No permissions", ephemeral=True)

def runbot(token: str):
    bot.run(token)