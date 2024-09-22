# Math.py

import discord
from discord.ext import commands


class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    math = discord.SlashCommandGroup(name="math", description="Solves math problems.")

    @math.command(name="add", description="Solves addition problems.")
    async def add(self, ctx, num1: int, num2: int):
        """Solves addition problems."""
        num3 = num1 + num2
        await ctx.respond(str(num1)+"+"+str(num2)+"="+str(num3))

    @math.command(name="subtract", description="Solves subtraction problems.")
    async def subtract(self, ctx, num1: int, num2: int):
        """Solves subtraction problems."""
        num3 = num1 - num2
        await ctx.respond(str(num1)+"-"+str(num2)+"="+str(num3))

    @math.command(name="multiply", description="Solves multiplication problems.")
    async def multiply(self, ctx, num1: int, num2: int):
        """Solves multiplication problems."""
        num3 = num1 * num2
        await ctx.respond(str(num1)+"×"+str(num2)+"="+str(num3))

    @math.command(name="divide", description="Solves division problems.")
    async def divide(self, ctx, num1: int, num2: int):
        """Solves division problems."""
        num3 = num1 / num2
        await ctx.respond(str(num1)+"÷"+str(num2)+"="+str(num3))


def setup(bot):
    bot.add_cog(Math(bot))
