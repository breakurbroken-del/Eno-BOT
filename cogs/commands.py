import discord
from discord.ext import commands

from utils.database import (
    add_tracked,
    remove_tracked,
    get_warning,
    reset_warning,
    add_role,
    remove_role
)


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="track")
    @commands.has_permissions(administrator=True)
    async def track(self, ctx, member: discord.Member):
        await add_tracked(member.id)
        await ctx.send(f"✅ {member.mention} is now being tracked.")

    @commands.command(name="untrack")
    @commands.has_permissions(administrator=True)
    async def untrack(self, ctx, member: discord.Member):
        await remove_tracked(member.id)
        await ctx.send(f"✅ {member.mention} has been removed from tracking.")

    @commands.command(name="protect")
    @commands.has_permissions(administrator=True)
    async def protect(self, ctx, role: discord.Role):
        await add_role(role.id)
        await ctx.send(f"🛡️ Protected Role Added: {role.mention}")

    @commands.command(name="unprotect")
    @commands.has_permissions(administrator=True)
    async def unprotect(self, ctx, role: discord.Role):
        await remove_role(role.id)
        await ctx.send(f"❌ Protected Role Removed: {role.mention}")

    @commands.command(name="warnings")
    async def warnings(self, ctx, member: discord.Member):
        warns = await get_warning(member.id)
        await ctx.send(f"{member.mention} has **{warns}/20** warnings.")

    @commands.command(name="resetwarn")
    @commands.has_permissions(administrator=True)
    async def resetwarn(self, ctx, member: discord.Member):
        await reset_warning(member.id)
        await ctx.send(f"🔄 Warnings reset for {member.mention}")


async def setup(bot):
    await bot.add_cog(Commands(bot))
