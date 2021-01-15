import random
import discord
from discord.ext import commands


class RockPaperScissorCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rps(self, ctx, player_choice=None):
        choices = ["rock", "paper", "scissor"]
        random.shuffle(choices)
        comp_choice = choices[0]
        if (player_choice not in choices) or (player_choice is None):
            await ctx.send("__***Error:***__\n**Usage: ~rps <choice> where <choice> is either rock, paper, or scissor.\nExample: ~rps scissor**")
        else:
            embedAns = discord.Embed(
                title="Rock, Paper, Scissor", color=0x00ff00)
            if comp_choice == player_choice.lower():
                embedAns.add_field(
                    name="Choices Selected:", value=f"Computer: {comp_choice.capitalize()} \n Player: {player_choice.capitalize()} \n\n `It's a draw!`", inline=False)
                await ctx.send(embed=embedAns)
                embedAns.clear_fields()
            if (comp_choice == "rock" and player_choice.lower() == "scissor") or (comp_choice == "paper" and player_choice.lower() == "rock") or (comp_choice == "scissor" and player_choice.lower() == "paper"):
                embedAns.add_field(
                    name="Choices Selected:", value=f"Computer: {comp_choice.capitalize()} \n Player: {player_choice.capitalize()} \n\n `Computer wins the game!`", inline=False)
                await ctx.send(embed=embedAns)
                embedAns.clear_fields()
            if (comp_choice == "scissor" and player_choice.lower() == "rock") or (comp_choice == "rock" and player_choice.lower() == "paper") or (comp_choice == "paper" and player_choice.lower() == "scissor"):
                embedAns.add_field(
                    name="Choices Selected:", value=f"Computer: {comp_choice.capitalize()} \n Player: {player_choice.capitalize()} \n\n `Player wins the game!`", inline=False)
                await ctx.send(embed=embedAns)
                embedAns.clear_fields()


def setup(bot):
    bot.add_cog(RockPaperScissorCog(bot))
