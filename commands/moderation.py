import discord
from discord import app_commands
from discord.ext import commands
from utils.permissions import has_admin_role
from utils.logging_utils import log_action

warns = {}

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Kick a user from the server")
    async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
        if not has_admin_role(interaction.user):
            return await interaction.response.send_message("❌ No permission", ephemeral=True)
        await user.kick(reason=reason)
        await interaction.response.send_message(f"Kicked {user.mention} for: {reason}")
        log_action("kick", interaction.user, user, reason)

    @app_commands.command(name="warn", description="Warn a user")
    async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
        if not has_admin_role(interaction.user):
            return await interaction.response.send_message("❌ No permission", ephemeral=True)
        warns.setdefault(user.id, []).append((interaction.user.id, reason))
        await interaction.response.send_message(f"{user.mention} has been warned. Reason: {reason}")
        log_action("warn", interaction.user, user, reason)

    @app_commands.command(name="warnlist", description="List warnings for a user")
    async def warnlist(self, interaction: discord.Interaction, user: discord.Member):
        user_warns = warns.get(user.id, [])
        if not user_warns:
            return await interaction.response.send_message(f"{user.mention} has no warnings.")
        warning_list = "\n".join([f"Warned by <@{w[0]}>: {w[1]}" for w in user_warns])
        await interaction.response.send_message(f"Warnings for {user.mention}:\n{warning_list}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))