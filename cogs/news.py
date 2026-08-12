import discord
from discord import app_commands
from discord.ext import commands
from .pimp_my_bot import theme

NEWS_URL = "https://kingdom-1617-news.vercel.app/"


class News(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="news", description="Get a link to the Kingdom 1617 news site.")
    async def news(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"{theme.documentIcon} Kingdom 1617 News",
            description="Stay up to date with the latest kingdom news.",
            color=theme.emColor1
        )
        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label="Open News",
            emoji=f"{theme.linkIcon}",
            url=NEWS_URL,
            style=discord.ButtonStyle.link
        ))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(News(bot))
