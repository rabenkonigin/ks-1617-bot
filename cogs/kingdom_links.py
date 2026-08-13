import discord
from discord import app_commands
from discord.ext import commands
from .pimp_my_bot import theme

BEAR_URL = "https://vgs-1617.vercel.app/#bear"
SWORDLAND_URL = "https://vgs-1617.vercel.app/#sword"
VIKING_URL = "https://vgs-1617.vercel.app/#viking"
TRI_URL = "https://vgs-1617.vercel.app/#tri"
HEROES4_URL = "https://vgs-1617.vercel.app/#s4heroes"


class KingdomLinks(commands.Cog):
    bear_group = app_commands.Group(name="bear", description="Bear Hunt commands.")
    tri_group = app_commands.Group(name="tri", description="Tri-Alliance commands.")

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

    @app_commands.command(name="viking", description="Get a link to the Viking Guide.")
    async def viking(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"{theme.documentIcon} Viking Guide",
            description="Open the Viking Guide.",
            color=theme.emColor1
        )
        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="Open Viking Guide",
            emoji=f"{theme.linkIcon}",
            url=VIKING_URL,
            style=discord.ButtonStyle.link
        ))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @tri_group.command(name="alliance", description="Get a link to the Tri-Alliance guide.")
    async def tri_alliance(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"{theme.documentIcon} Tri-Alliance",
            description="Open the Tri-Alliance guide.",
            color=theme.emColor1
        )
        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="Open Tri-Alliance",
            emoji=f"{theme.linkIcon}",
            url=TRI_URL,
            style=discord.ButtonStyle.link
        ))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @app_commands.command(name="heroes4", description="Get a link to the Kingshot Season 4 Heroes Development Guide.")
    async def heroes4(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"{theme.documentIcon} Season 4 Heroes Development Guide",
            description="Open the Kingshot Season 4 Heroes Development Guide.",
            color=theme.emColor1
        )
        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="Open Season 4 Heroes Guide",
            emoji=f"{theme.linkIcon}",
            url=HEROES4_URL,
            style=discord.ButtonStyle.link
        ))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(KingdomLinks(bot))
