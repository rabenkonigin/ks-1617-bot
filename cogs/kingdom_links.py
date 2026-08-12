import discord
from discord import app_commands
from discord.ext import commands
from .pimp_my_bot import theme

BEAR_URL = "https://vgs-1617.vercel.app/#bear"
SWORDLAND_URL = "https://vgs-1617.vercel.app/#sword"


class KingdomLinks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bear", description="Get a link to the Bear Hunt tracker.")
    async def bear(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"{theme.documentIcon} Bear Hunt",
            description="Open the Bear Hunt tracker.",
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

    @app_commands.command(name="swordland", description="Get a link to the Swordland tracker.")
    async def swordland(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"{theme.documentIcon} Swordland",
            description="Open the Swordland tracker.",
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
