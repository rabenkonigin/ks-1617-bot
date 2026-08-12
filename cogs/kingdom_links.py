import discord
from discord import app_commands
from discord.ext import commands
from .pimp_my_bot import theme

BEAR_URL = "https://vgs-1617.vercel.app/#bear"
SWORDLAND_URL = "https://vgs-1617.vercel.app/#sword"


class KingdomLinks(commands.Cog):
    bear_group = app_commands.Group(name="bear", description="Bear Hunt commands.")

    def __init__(self, bot):
        self.bot = bot

    @bear_group.command(name="tutorial", description="Get a link to the Bear Hunt tutorial.")
    async def bear_tutorial(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"{theme.documentIcon} Bear Hunt",
            description="Open the Bear Hunt tutorial.",
            color=theme.emColor1
        )
        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="Open Bear Hunt",
            emoji=f"{theme.linkIcon}",
            url=BEAR_URL,
            style=discord.ButtonStyle.link
        ))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @app_commands.command(name="swordland", description="Get a link to the Swordland tutorial.")
    async def swordland(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"{theme.documentIcon} Swordland",
            description="Open the Swordland tutorial.",
            color=theme.emColor1
        )
        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="Open Swordland",
            emoji=f"{theme.linkIcon}",
            url=SWORDLAND_URL,
            style=discord.ButtonStyle.link
        ))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(KingdomLinks(bot))
