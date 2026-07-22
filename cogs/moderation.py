import discord
from discord.ext import commands
from datetime import timedelta

import config
from utils.database import (
    is_tracked,
    get_roles,
    add_warning
)


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if message.author.bot:
            return

        if not message.guild:
            return

        # User tracked hai ya nahi
        if not await is_tracked(message.author.id):
            return

        protected_roles = await get_roles()

        triggered = False

        for role in message.role_mentions:
            if role.id in protected_roles:
                triggered = True
                break

        if not triggered:
            return

        # Warning add
        warning = await add_warning(message.author.id)

        # Kick at 20
        if warning >= config.KICK_AT:

            try:
                await message.author.send(
                    "You have reached 20 warnings and will now be removed from the server."
                )
            except:
                pass

            try:
                await message.guild.kick(
                    message.author,
                    reason="Reached 20 warnings."
                )
            except:
                pass

            return

        # Timeout duration
        if warning in config.TIMEOUTS:
            seconds = config.TIMEOUTS[warning]
        else:
            seconds = config.DEFAULT_TIMEOUT

        # Timeout
        if seconds > 0:
            try:
                await message.author.timeout(
                    timedelta(seconds=seconds),
                    reason=f"Warning #{warning}"
                )
            except:
                pass

        # Next punishment
        next_warning = warning + 1

        if next_warning >= config.KICK_AT:
            next_text = "Kick from Server"
        elif next_warning in config.TIMEOUTS:
            next_text = f"{config.TIMEOUTS[next_warning]//60} Minutes/Hours Timeout"
        else:
            next_text = "12 Hours Timeout"

        # DM
        try:
            await message.author.send(
                f"""⚠ Warning #{warning}

Reason:
You mentioned a protected role.

Next Punishment:
{next_text}

Warnings:
{warning}/20
"""
            )
        except:
            pass


async def setup(bot):
    await bot.add_cog(Moderation(bot))
