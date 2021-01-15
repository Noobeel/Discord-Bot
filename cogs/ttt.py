import random
import asyncio
import discord
from discord.ext import commands


class TicTacToeCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ttt(self, ctx, option=None):

        def get_easy_computer_move(computeroption, playeroption, board):
            pass

        def get_hard_computer_move(computeroption, playeroption, board):
            possibleMoves = []
            for x in range(1, 10):
                if board.get(x) == "  ":
                    possibleMoves.append(x)

            for i in possibleMoves:
                copy = board.copy()
                copy[i] = computeroption.upper()
                if check_win(computeroption, copy):
                    chosen = i
                    return chosen

            for i in possibleMoves:
                copy = board.copy()
                copy[i] = playeroption.upper()
                if check_win(playeroption, copy):
                    chosen = i
                    return chosen

            if 5 in possibleMoves:
                chosen = 5
                return chosen

            corners = []
            for i in possibleMoves:
                if i in [1, 3, 7, 9]:
                    corners.append(i)
            if len(corners) > 0:
                r = random.randrange(0, len(corners))
                chosen = corners[r]
                return chosen

            edges = []
            for i in possibleMoves:
                if i in [2, 4, 6, 8]:
                    edges.append(i)
            if len(edges) > 0:
                r = random.randrange(0, len(edges))
                chosen = edges[r]
                return chosen

        def add_move(move, option, board):
            board[move] = option.upper()

        def check_empty(move, board):
            if board[move] == 'X' or board[move] == 'O':
                return False
            return True

        def check_win(option, board):
            if option == 'x':
                if (board.get(7) == 'X' and board.get(8) == 'X' and board.get(9) == 'X') or (board.get(4) == 'X' and board.get(5) == 'X' and board.get(6) == 'X') or (board.get(1) == 'X' and board.get(2) == 'X' and board.get(3) == 'X') or (board.get(7) == 'X' and board.get(4) == 'X' and board.get(1) == 'X') or (board.get(8) == 'X' and board.get(5) == 'X' and board.get(2) == 'X') or (board.get(9) == 'X' and board.get(6) == 'X' and board.get(3) == 'X') or (board.get(7) == 'X' and board.get(5) == 'X' and board.get(3) == 'X') or (board.get(1) == 'X' and board.get(5) == 'X' and board.get(9) == 'X'):
                    return True
            else:
                if (board.get(7) == 'O' and board.get(8) == 'O' and board.get(9) == 'O') or (board.get(4) == 'O' and board.get(5) == 'O' and board.get(6) == 'O') or (board.get(1) == 'O' and board.get(2) == 'O' and board.get(3) == 'O') or (board.get(7) == 'O' and board.get(4) == 'O' and board.get(1) == 'O') or (board.get(8) == 'O' and board.get(5) == 'O' and board.get(2) == 'O') or (board.get(9) == 'O' and board.get(6) == 'O' and board.get(3) == 'O') or (board.get(7) == 'O' and board.get(5) == 'O' and board.get(3) == 'O') or (board.get(1) == 'O' and board.get(5) == 'O' and board.get(9) == 'O'):
                    return True
            return False

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        if option:
            if option.lower() == "start":
                embedWelcome = discord.Embed(
                    title="Tic Tac Toe", description="**Welcome to Tic Tac Toe!**", color=0x00ff00)
                embedWelcome.add_field(name="Follow bot instructions to start playing",
                                       value='Enter choices by typing in the current channel.\nNo commands are needed to submit choices.\nYou have __90 seconds__ to reply when it is your turn, if timelimit is exceeded the game will end.\nType **end** to end the game', inline=False)
                await ctx.send(embed=embedWelcome)

                board = {1: "  ", 2: "  ", 3: "  ",
                         4: "  ", 5: "  ", 6: "  ",
                         7: "  ", 8: "  ", 9: "  "}

                await ctx.send("**Choose your character by typing `X` or `O`**")
                try:
                    while True:
                        player_option = await self.bot.wait_for('message', timeout=90.0, check=check)
                        player_option = player_option.content.lower()
                        if player_option == "end":
                            await ctx.send("**Game ended**")
                            return
                        if player_option in ['x', 'o']:
                            break
                        else:
                            await ctx.send("**Incorrect character entered. Retry by typing `X` or `O`**")
                    comp_option = 'x' if player_option == 'o' else 'o'
                except asyncio.TimeoutError:
                    await ctx.send("**Player didn't respond within 90 seconds, ending game**")
                    return

                await ctx.send("**Choose level of AI difficulty by typing `Easy` or `Hard`**")
                while True:
                    try:
                        difficulty = await self.bot.wait_for('message', timeout=90.0, check=check)
                        difficulty = difficulty.content.lower()
                        if difficulty == "end":
                            await ctx.send("**Game ended**")
                            return
                        if difficulty in ['easy', 'hard']:
                            break
                        else:
                            await ctx.send("**Incorrect level entered. Retry by typing `Easy` or `Hard`**")
                    except asyncio.TimeoutError:
                        await ctx.send("**Player didn't respond within 90 seconds, ending game**")
                        return

                player_win = comp_win = False
                count = 0
                await ctx.send("**Enter the number (in current channel) corresponding to the position to place your character once it is your turn\n1|2|3\n-------\n4|5|6\n-------\n7|8|9**")
                while True:
                    count += 1
                    await ctx.send("**Players Turn; Enter a valid position**")
                    player_move = None
                    while True:
                        try:
                            player_move = await self.bot.wait_for('message', timeout=90.0, check=check)
                            if player_move.content.lower() == "end":
                                await ctx.send("**Game ended**")
                                return
                            elif player_move.content.isdigit() and int(player_move.content) > 0 and int(player_move.content) <= 9 and check_empty(int(player_move.content), board):
                                add_move(int(player_move.content),
                                         player_option, board)
                                break
                            else:
                                await ctx.send("**Invalid move, try again**")
                        except asyncio.TimeoutError:
                            await ctx.send("**Player didn't respond within 90 seconds, ending game**")
                            return
                    await ctx.send("**Players Move:**")
                    await ctx.send(f"**{board.get(1)} | {board.get(2)} | {board.get(3)} \n-----------\n{board.get(4)} | {board.get(5)} | {board.get(6)} \n-----------\n{board.get(7)} | {board.get(8)} | {board.get(9)} **")
                    player_win = check_win(player_option, board)
                    if player_win:
                        await ctx.send("**Player has won against Computer!\nGame has Ended!**")
                        break
                    await ctx.send("**\nComputers Move:\n**")
                    if count != 4:
                        comp_move = None
                        if difficulty == "easy":
                            comp_move = get_hard_computer_move(
                                comp_option, player_option, board)
                        elif difficulty == "hard":
                            comp_move = get_hard_computer_move(
                                comp_option, player_option, board)
                        add_move(comp_move, comp_option, board)
                    await ctx.send(f"**{board.get(1)} | {board.get(2)} | {board.get(3)} \n-----------\n{board.get(4)} | {board.get(5)} | {board.get(6)} \n-----------\n{board.get(7)} | {board.get(8)} | {board.get(9)} **")
                    if count == 4 and (not player_win and not comp_win):
                        await ctx.send("**It's a draw!\nGame has Ended!**")
                        break
                    comp_win = check_win(comp_option, board)
                    if comp_win:
                        await ctx.send("**Computer has won against Player!\nGame has Ended!**")
                        break
        else:
            await ctx.send("__***Error:***__\n**Usage: `~ttt start` to start the game**")


def setup(bot):
    bot.add_cog(TicTacToeCog(bot))
