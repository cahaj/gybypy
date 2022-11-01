import bot.bot as bot
from bot.keep_alive import keep_alive
import discord
import os

while __name__ == '__main__':
  try:
    keep_alive()
    bot.runbot(os.environ['token'])
  except discord.errors.HTTPException as e:
    print(e)
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    os.system('kill 1')