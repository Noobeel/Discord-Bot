import os
import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents().all()
description = "A discord bot for Majboori's community server!"
bot = commands.Bot(command_prefix='~',
                   description=description, intents=intents, help_command=None)
guild = bot.get_guild(679859298980986927)
load_dotenv()
token = os.getenv('DiscordBotToken')


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Majboori's feelings"))
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    print('Guilds Joined:')
    print(bot.guilds)
    print('------')


@bot.command()
async def hello(ctx, member=discord.Member):
    await ctx.send(f'Hi {ctx.author.mention}')


@bot.command()
async def help(ctx, command=None, extra=None):
    commandEmbed = allhelpEmbed = None
    if not command:
        allhelpEmbed = discord.Embed(
            title="Help", description="**A list of all commands along with their functions and usage examples:**", color=0x00ff00)
        allhelpEmbed.add_field(
            name="`~help`", value="A list of all commands (or a specific command) and their functions.\nUsage: ~help <command (optional)>", inline=False)
        allhelpEmbed.add_field(
            name="`~hello`", value="Say Hello to the bot.\nUsage: ~hello", inline=False)
        allhelpEmbed.add_field(
            name="`~rps`", value="Play Rock, Paper, Scissors with the bot!\nUsage: ~rps <choice> where choice can be either rock, paper, or scissor", inline=False)
        allhelpEmbed.add_field(
            name="`~ttt`", value="Play Tic Tac Toe with the bot!\nUsage: ~ttt start to start a game", inline=False)
        allhelpEmbed.add_field(
            name="`~roles`", value="A list of all assignable roles in the server.\nUsage: ~roles", inline=False)
        allhelpEmbed.add_field(
            name="`~calc`", value="A list of all commands and their functions.\nUsage: ~calc <expr> where expr is a mathematical expression\nExample: 1+(2x3)", inline=False)
        allhelpEmbed.add_field(
            name="`~exchange`", value="A tool to get exchange rates between two currencies.\nUsage: ~exchange <from currency> <to currency>\nExample: ~exchange USD CAD", inline=False)
    elif command == "help" and extra == "help":
        commandEmbed = discord.Embed(
            title="**Do it again~~", description="***Dumbass***", color=0x00ff00)
    elif command == "help":
        commandEmbed = discord.Embed(
            title="***~help***", description="A list of all commands (or a specific command) and their functions.\nUsage: ~help <command (optional)>\nMight as well do `~help help help` at this point", color=0x00ff00)
    elif command == "hello":
        commandEmbed = discord.Embed(
            title="***~hello***", description="Say Hello to the bot.\nUsage: ~hello", color=0x00ff00)
    elif command == "rps":
        commandEmbed = discord.Embed(
            title="***~rps***", description="Play Rock, Paper, Scissors with the bot!\nUsage: ~rps <choice> where choice can be either rock, paper, or scissor", color=0x00ff00)
    elif command == "ttt":
        commandEmbed = discord.Embed(
            title="***~ttt***", description="Play Tic Tac Toe with the bot!\nUsage: ~ttt start to start a game", color=0x00ff00)
    elif command == "roles":
        commandEmbed = discord.Embed(
            title="***~roles***", description="A list of all assignable roles in the server.\nUsage: ~roles", color=0x00ff00)
    elif command == "calc":
        commandEmbed = discord.Embed(
            title="***~calc***", description="A list of all commands and their functions.\nUsage: ~calc <expr> where expr is a mathematical expression\nExample: ~calc 1+(2x3)", color=0x00ff00)
    elif command == "exchange":
        commandEmbed = discord.Embed(
            title="***~exchange***", description="A tool to get exchange rates between two currencies.\nUsage: ~exchange <from currency> <to currency>\nExample: ~exchange USD CAD", color=0x00ff00)
    await ctx.send(embed=commandEmbed) if commandEmbed else await ctx.send(embed=allhelpEmbed)


@bot.command()
async def roles(ctx):
    embedVar = discord.Embed(
        title="Server Roles", description="All assignable roles in this server", color=0x00ff00)
    for role in ctx.guild.roles:
        if role.id not in [700465520809476146, 790808747081072661, 679859298980986927, 702042797586251857]:
            embedVar.add_field(name="___________",
                               value=role.name, inline=False)
    await ctx.send(embed=embedVar)


@bot.command()
async def exchange(ctx, from_currency, to_currency):
    url = os.getenv('ExchangeAPI_URL') + from_currency
    response = requests.get(url)
    data = response.json()
    if data["result"] == "error":
        error = data["error-type"]
        if error == "unsupported-code":
            await ctx.send("**Currency not supported :(**")
        elif error in ["malformed-request", "invalid-key", "quota-reached"]:
            await ctx.send(f"Request failed due to error: {error}, Contact Majboori for assistance.")
    elif data["result"] == "success":
        to_currency_rate = data["conversion_rates"][to_currency]
        time = data["time_last_update_utc"]
        currencyEmbed = discord.Embed(
            title="Currency Exchange", description=f"Exchange rate from {from_currency} to {to_currency}:", color=0x00ff00)
        currencyEmbed.add_field(
            name=f"1 {from_currency} = {to_currency_rate} {to_currency}", value=f"*Last Updated = {time} UTC*", inline=False)
        await ctx.send(embed=currencyEmbed)


@bot.command()
async def calc(ctx, expression):
    # use stack, + - * / ( ) ^ % ! [ ] < >
    pass


@bot.event
async def on_raw_reaction_add(payload):
    pass


@bot.event
async def on_raw_reaction_remove(payload):
    pass


@bot.event
async def on_member_join(member):
    joinEmbed = discord.Embed(title="Welcome to Majboori's Server!",
                              description=f"{member.mention} Remember to read and agree to server rules and enjoy your stay!", color=0x00ff00)
    joinEmbed.set_thumbnail(url=member.avatar_url_as(size=2048))
    await bot.get_channel(799175678443782164).send(embed=joinEmbed)


@bot.event
async def on_member_remove(member):
    message = await bot.get_channel(799175678443782164).send(str(member.display_name) + " has left the server")
    await message.add_reaction('<:PepeHands:702257643950964877>')


if __name__ == "__main__":
    all_cogs = ['cogs.rps', 'cogs.ttt']
    for cog in all_cogs:
        bot.load_extension(cog)


bot.run(token)
