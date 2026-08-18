import sqlite3
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

# Raven, Sigrid
TIG_NICKNAME_EDITOR_IDS = {1218426159059173478, 1471197123054665992}

DB_PATH = "db/settings.sqlite"


def _init_db():
    with sqlite3.connect(DB_PATH, timeout=30.0) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS tig_nicknames (
                nickname TEXT PRIMARY KEY
            )
        """)


def _load_custom_nicknames() -> list[str]:
    with sqlite3.connect(DB_PATH, timeout=30.0) as db:
        rows = db.execute("SELECT nickname FROM tig_nicknames ORDER BY rowid").fetchall()
    return [row[0] for row in rows]


def _add_custom_nickname(nickname: str):
    with sqlite3.connect(DB_PATH, timeout=30.0) as db:
        db.execute("INSERT INTO tig_nicknames (nickname) VALUES (?)", (nickname,))
        db.commit()


class Tig(commands.Cog):
    add_group = app_commands.Group(name="add", description="Add commands.")

    def __init__(self, bot):
        self.bot = bot
        _init_db()

    @app_commands.command(name="tig", description="Show the list of Tig's nickname.")
    async def tig(self, interaction: discord.Interaction):
        nicknames = TIG_NICKNAMES + _load_custom_nicknames()
        embed = discord.Embed(
            title=f"{theme.documentIcon} Tig's Nicknames",
            color=theme.emColor1
        )
        column_count = 3
        column_size = -(-len(nicknames) // column_count)  # ceil division
        for i in range(column_count):
            column = nicknames[i * column_size:(i + 1) * column_size]
            if not column:
                continue
            embed.add_field(
                name="​",
                value="\n".join(f"• {nickname}" for nickname in column),
                inline=True
            )
        await interaction.response.send_message(embed=embed)

    @add_group.command(name="tig", description="[Raven/Sigrid] Add new Tig's nickname.")
    @app_commands.describe(nickname="The new nickname to add")
    async def add_tig(self, interaction: discord.Interaction, nickname: str):
        if interaction.user.id not in TIG_NICKNAME_EDITOR_IDS:
            await interaction.response.send_message(
                f"{theme.deniedIcon} You are not allowed to use this command.",
                ephemeral=True,
            )
            return

        nickname = nickname.strip()
        if not nickname:
            await interaction.response.send_message(
                f"{theme.deniedIcon} Nickname can't be empty.",
                ephemeral=True,
            )
            return

        existing = {n.lower() for n in TIG_NICKNAMES} | {n.lower() for n in _load_custom_nicknames()}
        if nickname.lower() in existing:
            await interaction.response.send_message(
                f"{theme.deniedIcon} \"{nickname}\" is already in the list.",
                ephemeral=True,
            )
            return

        _add_custom_nickname(nickname)
        await interaction.response.send_message(
            f"{theme.verifiedIcon} Added \"{nickname}\" to Tig's nicknames!",
            ephemeral=True,
        )


async def setup(bot):
    await bot.add_cog(Tig(bot))
