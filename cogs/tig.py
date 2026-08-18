import discord
from discord import app_commands
from discord.ext import commands
from .pimp_my_bot import theme

TIG_NICKNAMES = [
    "tug", "tuggles", "tiggles", "tiggly", "tiggy", "tuggy", "koktator", "light switch",
    "tigtator", "The DON", "Tuggernuts", "tiggibug", "Mr. Tigglesworth", "tuggernutter",
    "tuggleupagus", "tiggums", "Tugs'em", "tigglebutt", "TugLovin", "Tiggymiggy",
    "tuggy wuggy", "Tig the rig", "flick flick", "flick & lick", "rub a tug tug",
    "rub a rug n tug", "tiglet", "tugglepus", "Sir Tugsalot", "tiggly wiggly",
    "TUG-o-RAMA", "OpTigmus Prime! Autokoks roll out!", "King Kok", "Mc Tugglebutt",
    "Tugglesaur", "Tuggy wuggy woo", "Doc Mc Tiggins", "Tigald Mc Tugalds",
    "Doc Tugaday", "Tiggy Tig", "Tug of Doom", "Tuglin the Dethroned", "Tuggsy",
    "Tuggly Bear", "Tiggy Bear", "Tiggy Boo", "TugTug", "tugglebuns", "Tiggy Tuggy",
    "Big Rig Tig", "tiggle Bittys", "Tig ol' Bitty", "Tiggus", "Tiggy wiggy",
    "Maximus Tiggus", "Maximus Decimus Tiggius", "Rub-a-tug Tig", "tiggly winks",
    "gig", "tiggity giggity", "Tig tug", "Tiggamus Maximus", "Tugalug", "Tigatron",
    "Tiggs McGiggs", "The Tigginator", "Sir McTigguns", "Señor McTigum", "Tigathy",
    "Tuggy Nuggy", "tigapotamus", "Tigasaurus", "Tigmeister", "Tiggly Tuggly",
    "Tiggles McGiggles", "Tiggermeister", "MeisterTigger", "Tugglius Maximus",
    "Tignaught", "Tugganaught", "Tuggernaught", "Tuggle Wuggle", "TuggenaNut",
    "Tiggidy Wiggley", "Sir Tigsalot", "Kokney", "tug a tug a tug a choooo chooo",
    "Tugglebum", "Tip tugging tipsy tig", "Tiggy McTugface",
]


class Tig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="tig", description="Show the list of Tig's nickname.")
    async def tig(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"{theme.documentIcon} Tig's Nicknames",
            color=theme.emColor1
        )
        column_count = 3
        column_size = -(-len(TIG_NICKNAMES) // column_count)  # ceil division
        for i in range(column_count):
            column = TIG_NICKNAMES[i * column_size:(i + 1) * column_size]
            if not column:
                continue
            embed.add_field(
                name="​",
                value="\n".join(f"• {nickname}" for nickname in column),
                inline=True
            )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Tig(bot))
