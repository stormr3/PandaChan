import discord
from discord.ext import commands
import json

with open('reports.json', encoding='utf-8') as f:
  try:
    report = json.load(f)
  except ValueError:
    report = {}
    report['users'] = []

class Moderation(commands.Cog):
  def __init__(self,bot):
    self.bot = bot

  #Events


  #Commands
  @commands.command()
  @commands.has_permissions(manage_roles=True, ban_members=True)
  async def warn(self, ctx,user:discord.User,*reason:str):
    if not reason:
      await ctx.send("Please provide a reason")
      return
    reason = ' '.join(reason)
    for current_user in report['users']:
      if current_user['name'] == user.name:
        current_user['reasons'].append(reason)
        embed = discord.Embed(title=f"Warned {user.name} ",color=discord.Colour.green())
        await ctx.send(embed = embed)
        #current_user['reasons'].pop(0)
        break
    else:
      report['users'].append({
        'name':user.name,
        'reasons': [reason,]
      })
      embedd = discord.Embed(title=f"Warned {user.name} ",color=discord.Colour.green())
      await ctx.send(embed = embedd)
    with open('reports.json','w+') as f:
      json.dump(report,f)

  @commands.command(aliases=['cwarn'])
  @commands.has_permissions(manage_roles=True, ban_members=True)
  async def clearwarn(self, ctx,user:discord.User):
    for current_user in report['users']:
      if current_user['name'] == user.name:
        if len(current_user['reasons']) == 0:
          embed = discord.Embed(title="User have no Reports",color=discord.Colour.green())
          await ctx.send(embed =embed)
        else:
          i = 1
          while i <= len(current_user['reasons']):
            current_user['reasons'].pop(0)
          embedd = discord.Embed(title=f"Cleared {user.name} Warns",color=discord.Colour.green())
          await ctx.send(embed = embedd)

  @commands.command(aliases=['rwarn'])
  @commands.has_permissions(manage_roles=True, ban_members=True)
  async def removewarn(self, ctx,user:discord.User, warnId):
    for current_user in report['users']:
      if current_user['name'] == user.name:
        if len(current_user['reasons']) == 0:
          embed = discord.Embed(title="User have no Reports",color=discord.Colour.green())
          await ctx.send(embed =embed)
        else:
          current_user['reasons'].pop(int(warnId) -1)
          embedd = discord.Embed(title=f"Removed {user.name} Warn",color=discord.Colour.green())
          await ctx.send(embed = embedd)


    with open('reports.json','w+') as f:
      json.dump(report,f)

  @commands.command(pass_context = True)
  @commands.has_permissions(manage_roles=True, ban_members=True)
  async def warns(self, ctx,user:discord.User):
    for current_user in report['users']:
      if user.name == current_user['name']:
        embed = discord.Embed(title=f"{user.name} has been reported {len(current_user['reasons'])} times : {','.join(current_user['reasons'])}",color=discord.Colour.green())
        await ctx.send(embed =embed)
        break
    else:
      embedd = discord.Embed(title=f"{user.name} has never been reported", color=discord.Colour.green())
      await ctx.send(embed = embedd)  


  @commands.command(help='Kicks Member')  #kicks x user
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx, member: discord.Member, *, reason='No Reason provided'):
      embed = discord.Embed(title=f"{member} has been kicked",
                          color=discord.Colour.red())
      await member.send(f"You have been kicked from {ctx.guild.name}, Reason - " +
                      reason)
      await member.kick(reason=reason)
      await ctx.channel.send(embed=embed)


  @commands.command(help='dont u know the meaning of ban')  #bans x user
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx, member: commands.MemberConverter, *, reason='No Reason provided'):
      embed = discord.Embed(title=f"{member} has been banned",color=discord.Colour.red())
      await member.send(f"You have been banned from {ctx.guild.name}, Reason - " +reason)
      await member.ban(reason=reason)
      await ctx.channel.send(embed=embed)


  @commands.command(help='im bored thts why u will see unusual help messages')  #unbans x user
  @commands.has_permissions(ban_members=True)
  async def unban(self, ctx, id :int):
      user = self.bot.fetch_user(id)
      await ctx.guild.unban(user)
      embed=discord.Embed(title=f'{user.mention} has been unbanned', color=discord.Colour.green())
      await ctx.send(embed=embed)


  @commands.command(help='doobi doobi dooba doobi doobi dooba')
  @commands.has_permissions(manage_messages=True)
  async def mute(self,ctx, member: discord.Member, *, reason=None):
      guild = ctx.guild
      mutedRole = discord.utils.get(guild.roles, name="Muted")

      if not mutedRole:
          mutedRole = await guild.create_role(name="Muted")

          for channel in guild.channels:
              await channel.set_permissions(mutedRole,
                                          speak=False,
                                          send_messages=False,
                                          read_message_history=True,
                                          read_messages=False)
      embed = discord.Embed(title="Muted",
                          description=f"{member.mention} was muted ",
                          colour=discord.Colour.red())
      embed.add_field(name="reason:", value=reason, inline=False)
      await ctx.send(embed=embed)
      await member.add_roles(mutedRole, reason=reason)
      await member.send(
        f" you have been muted from: {guild.name} reason: {reason}")


  @commands.command(help='AGENT P!')
  @commands.has_permissions(manage_messages=True)
  async def unmute(self,ctx, member: discord.Member):
      mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

      await member.remove_roles(mutedRole)
      await member.send(f" you have Unmuted from: - {ctx.guild.name}")
      embed = discord.Embed(title="Unmute",
                          description=f" unmuted-{member.mention}",
                          colour=discord.Colour.green())
      await ctx.send(embed=embed)

  @commands.command()
  @commands.has_permissions(manage_messages=True)
  async def clear(self,ctx,amount = 2):
    await ctx.channel.purge(limit = amount + 1)

  @commands.command()
  @commands.has_permissions(manage_messages=True)
  async def embed(self,ctx):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    embedMessage1 = discord.Embed(description ='What is the title',colour = discord.Colour.green())

    embedMessage2 = discord.Embed(description ='What is the description',colour = discord.Colour.green())

    await ctx.send(embed = embedMessage1,delete_after=5)
    embedtitle = await self.bot.wait_for('message', check=check)
    await ctx.channel.purge(limit =1)


    await ctx.send(embed = embedMessage2,delete_after=5)
    embedDesc = await self.bot.wait_for('message', check=check)
    await ctx.channel.purge(limit =1)
    
    embedUser = discord.Embed(title = embedtitle.content,description = embedDesc.content,colour = discord.Colour.green())

    await ctx.message.delete()
  
    await ctx.send(embed = embedUser)


  #Error Handling
  


def setup(bot):
  bot.add_cog(Moderation(bot))