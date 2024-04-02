
from dotenv import load_dotenv
import os
import logging
import discord
from discord.ext import commands
from discord.ui import Button, View

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print(f"Bot is up and running {bot.user}")
    guild_count = 0
    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count = guild_count + 1
    print("Silas Manager is in " + str(guild_count) + " guilds.")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=f"{guild_count} Servers"))


@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return
    if ctx.author.bot:
        return
    if ctx.content == '':
        return
    with open('text.txt', 'a') as file_log:
        file_log.write(f"{ctx.author} | {ctx.content}\n")
@bot.slash_command(name="ban", description='Ban users')
@commands.has_role('Ban_Hammer')
async def first_slash(ctx, user: discord.Member, reason: str = None):
    confirm_button_for_ban = Button(label='Confirm', style=discord.ButtonStyle.green, emoji='✅')
    deny_button_for_ban = Button(label='Deny', style=discord.ButtonStyle.danger)

    async def confirm_button(interaction):
        await interaction.response.edit_message(content='', view=None)
        await interaction.followup.send(content=f"<@{ctx.author.id}> has confirmed ban for {user}")
        await user.ban(reason=reason)

    async def deny_button(interaction):
        await interaction.response.edit_message(content='', view=None)
        await interaction.followup.send(content=f"<@{ctx.author.id}> has denied ban for {user}")
        pass

    confirm_button_for_ban.callback = confirm_button
    deny_button_for_ban.callback = deny_button
    view = View()
    view.add_item(confirm_button_for_ban)
    view.add_item(deny_button_for_ban)
    embed = discord.Embed(title="Ban Hammer", description=f"<@{ctx.author.id}> is trying to ban",
                          color=discord.Colour.blurple(), )
    embed.add_field(name="Ban Info", value=f"> Person Getting Banned | {user}. \n > Reason For Ban | {reason}")
    print(f"{ctx.author} is trying to ban person Getting Banned | {user}. \n Reason For Ban | {reason}")
    await ctx.response.send_message(embed=embed, view=view)

@bot.slash_command(name="kick", description='Kick users')
@commands.has_role('Ban_Hammer')
async def second_slash(ctx, user: discord.Member, reason: str = None):
    confirm_button_for_ban = Button(label='Confirm', style=discord.ButtonStyle.green, emoji='✅')
    deny_button_for_ban = Button(label='Deny', style=discord.ButtonStyle.danger)

    async def confirm_button(interaction):
        await interaction.response.edit_message(content='', view=None)
        await interaction.followup.send(content=f"Has been kicked for {user}")
        await user.ban(reason=reason)

    async def deny_button(interaction):
        await interaction.response.edit_message(content='', view=None)
        await interaction.followup.send(content=f"Kick has beed denied for the {user}")
        pass

    confirm_button_for_ban.callback = confirm_button
    deny_button_for_ban.callback = deny_button
    view = View()
    view.add_item(confirm_button_for_ban)
    view.add_item(deny_button_for_ban)
    embed = discord.Embed(title="Kick Hammer", description=f"<@{ctx.author.id}> is trying to kick",
                          color=discord.Colour.blurple(), )
    embed.add_field(name="Kick Info", value=f"> Person Getting Kicked | {user}. \n > Reason For Kick | {reason}")
    print(f"{ctx.author} is trying to ban person Getting Kicked | {user}. \n Reason For Kick | {reason}")
    await ctx.response.send_message(embed=embed, view=view)

@bot.slash_command(name="help", description="List of all commands")
async def thierd_slash(ctx):
    embed1 = discord.Embed(title="Commands", description=f"Commands", color=discord.Colour.blurple(), )
    embed1.add_field(name="/kick", value=f"| Kick a player from the server |")
    embed1.add_field(name="/ban", value=f"| Ban a player from the server |")

    await ctx.response.send_message(embed=embed1)

@first_slash.error
async def slash1_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.response.send_message('You cant use this command')

@second_slash.error
async def slash2_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.response.send_message('You cant use this command')
@thierd_slash.error
async def slash3_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.response.send_message('You cant use this command')

load_dotenv('token.env')
bot.run(os.getenv('TOKEN'))
