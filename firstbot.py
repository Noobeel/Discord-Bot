import os
import requests
import json
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
    directory = os.path.abspath(__file__).split('\\')
    del directory[-1]
    dataFile = open('\\'.join(directory) + '\\help.json')
    data = json.load(dataFile)
    if not command:
        allhelpEmbed = discord.Embed(
            title="Help", description="**A list of all commands along with their functions and usage examples:**", color=0x00ff00)
        for commandInfo in data['help_command_descriptions']:
            allhelpEmbed.add_field(
                name=f"`~{commandInfo['name']}`", value=commandInfo['description'], inline=False)
    else:
        if command == "help" and extra == "help":
            commandEmbed = discord.Embed(
                title="~~Do it again~~", description="***Dumbass***", color=0x00ff00)
        else:
            for commandInfo in data['help_command_descriptions']:
                if command == commandInfo['name']:
                    commandEmbed = discord.Embed(
                        title=f"***~{commandInfo['name']}***", description=f"***{commandInfo['description']}***", color=0x00ff00)
                    break
    await ctx.send(embed=commandEmbed) if commandEmbed else await ctx.send(embed=allhelpEmbed)
    dataFile.close()


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
        elif error in ("malformed-request", "invalid-key", "quota-reached"):
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
    # + - * / ( ) ^ % ! [ ] < >
    # calculate, account for brackets, account for invalid expression
    stack = []
    result = 0
    prev = 'None'
    for index in range(len(expression)):
        if expression[index].isdigit():
            if prev.isdigit():
                if index+1 < len(expression):
                    if expression[index+1].isdigit():
                        prev += expression[index]
                    else:
                        stack.append(prev + expression[index])
                else:
                    stack.append(prev + expression[index])
            else:
                if index+1 < len(expression):
                    if not expression[index+1].isdigit():
                        stack.append(expression[index])
                else:
                    stack.append(expression[index])
                prev = expression[index]
        elif expression[index] in ['+', '-', '*', '/', '^', '%', '!', '<', '>']:
            prev = 'None'
            stack.append(expression[index])
    await ctx.send(f"Result for {expression} is {result}")


@bot.command()
async def suggest(ctx, *args):
    if not args:
        await ctx.send("__***Error:***__\n**Usage: `~suggest <suggestion>` to send your suggestion!**")
        return
    await ctx.message.delete()
    suggestEmbed = discord.Embed(title="A new suggestion has arrived!",
                                 description="React with <:upvote:800568171282038804> or <:downvote:800568135282589716> to upvote or downvote this suggestion.", color=0x00ff00)
    suggestEmbed.add_field(name="Suggestion:", value=' '.join(args), inline=False)
    message = await bot.get_channel(800566984273035264).send(embed=suggestEmbed)
    await message.add_reaction('<:upvote:800568171282038804>')
    await message.add_reaction('<:downvote:800568135282589716>')


@ bot.event
async def on_raw_reaction_add(payload):
    pass


@ bot.event
async def on_raw_reaction_remove(payload):
    pass


@ bot.event
async def on_member_join(member):
    joinEmbed = discord.Embed(title="Welcome to Majboori's Server!",
                              description=f"{member.mention} Remember to read and agree to server rules and enjoy your stay!", color=0x00ff00)
    joinEmbed.set_thumbnail(url=member.avatar_url_as(size=2048))
    await bot.get_channel(799175678443782164).send(embed=joinEmbed)


@ bot.event
async def on_member_remove(member):
    message = await bot.get_channel(799175678443782164).send(str(member.display_name) + " has left the server")
    await message.add_reaction('<:PepeHands:702257643950964877>')


if __name__ == "__main__":
    all_cogs = ['cogs.rps', 'cogs.ttt']
    for cog in all_cogs:
        bot.load_extension(cog)


bot.run(token)
