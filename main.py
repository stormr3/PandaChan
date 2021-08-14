import os
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Bot is Online')
    await bot.change_presence(activity=discord.Game(name='!help'))

@bot.command()
async def load(ctx, extension):
  bot.load_extension(f'cogs.{extension}')
  await ctx.send(f'Loaded {extension}')

@bot.command()
async def unload(ctx, extension):
  bot.unload_extension(f'cogs.{extension}')
  await ctx.send(f'Unloaded {extension}')

@bot.command()
async def reload(ctx, extension):
  bot.unload_extension(f'cogs.{extension}')
  bot.load_extension(f'cogs.{extension}')
  await ctx.send(f'Reloaded {extension}')

@bot.event
async def on_command_error(ctx,error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send('You Cant Do That ;-;')
  
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('Complete the command ;-;')

  elif isinstance(error, commands.MemberNotFound):
    await ctx.send('Member Not Found')

  else:
    raise error

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

bot.run("ODY4NzM5MzYyNDM3ODU3Mjkw.YP0ClA.huPDGN-ZS8YURozyzyJ9Ns5qpXI")
