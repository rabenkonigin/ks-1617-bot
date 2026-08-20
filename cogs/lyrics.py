import random
import asyncio
import sqlite3
import discord
import requests
from bs4 import BeautifulSoup
from discord import app_commands
from discord.ext import commands
from .pimp_my_bot import theme

LYRICS_EDITOR_ROLE_ID = 1522812704794873856
RANT_CHANNEL_ID = 1530447808912560158

DB_PATH = "db/lyrics.sqlite"
MAX_LINES_PER_ADD = 1000
RANT_INTERVAL_SECONDS = 7


def _init_db():
    with sqlite3.connect(DB_PATH, timeout=30.0) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS lyrics_lines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                line TEXT NOT NULL,
                added_by INTEGER,
                added_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


def _add_lines(lines: list[str], added_by: int):
    with sqlite3.connect(DB_PATH, timeout=30.0) as db:
        db.executemany(
            "INSERT INTO lyrics_lines (line, added_by) VALUES (?, ?)",
            [(line, added_by) for line in lines],
        )
        db.commit()


def _load_all_lines() -> list[str]:
    with sqlite3.connect(DB_PATH, timeout=30.0) as db:
        rows = db.execute("SELECT line FROM lyrics_lines").fetchall()
    return [row[0] for row in rows]


def _extract_lines(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    for br in soup.find_all("br"):
        br.replace_with("\n")
    text = soup.get_text()
    lines = [line.strip() for line in text.split("\n")]
    return [line for line in lines if line]


class Lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._active_channels = set()
        _init_db()

    @app_commands.command(
        name="addlyrics",
        description="Add song lyrics from a link, saved as individual lines.",
    )
    @app_commands.describe(link="URL to the lyrics page")
    async def addlyrics(self, interaction: discord.Interaction, link: str):
        member_roles = getattr(interaction.user, "roles", [])
        if not any(role.id == LYRICS_EDITOR_ROLE_ID for role in member_roles):
            await interaction.response.send_message(
                f"{theme.deniedIcon} You are not allowed to use this command.",
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)

        try:
            resp = requests.get(
                link, timeout=10,
                headers={"User-Agent": "Mozilla/5.0 (compatible; KingshotBot/1.0)"},
            )
            resp.raise_for_status()
        except Exception as e:
            await interaction.followup.send(
                f"{theme.deniedIcon} Couldn't fetch that link: {e}", ephemeral=True
            )
            return

        lines = _extract_lines(resp.text)[:MAX_LINES_PER_ADD]
        if not lines:
            await interaction.followup.send(
                f"{theme.deniedIcon} No text could be extracted from that link.",
                ephemeral=True,
            )
            return

        _add_lines(lines, interaction.user.id)
        await interaction.followup.send(
            f"{theme.verifiedIcon} Saved {len(lines)} lyric lines from that link.",
            ephemeral=True,
        )

    @app_commands.command(
        name="rants",
        description="Post a random saved lyric line every 7 seconds for a set duration.",
    )
    @app_commands.describe(duration="How many minutes to run for (max 30)")
    async def rants(
        self, interaction: discord.Interaction, duration: app_commands.Range[int, 1, 30]
    ):
        channel_id = interaction.channel_id
        if channel_id != RANT_CHANNEL_ID:
            await interaction.response.send_message(
                f"{theme.deniedIcon} This command can only be used in <#{RANT_CHANNEL_ID}>.",
                ephemeral=True,
            )
            return

        if channel_id in self._active_channels:
            await interaction.response.send_message(
                f"{theme.deniedIcon} A rant session is already running in this channel.",
                ephemeral=True,
            )
            return

        lines = _load_all_lines()
        if not lines:
            await interaction.response.send_message(
                f"{theme.deniedIcon} No lyrics have been added yet.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            f"🎤 Starting a {duration}-minute rant session — a new line every "
            f"{RANT_INTERVAL_SECONDS} seconds!"
        )
        self._active_channels.add(channel_id)
        self.bot.loop.create_task(
            self._run_rant(interaction.channel, channel_id, lines, duration)
        )

    async def _run_rant(self, channel, channel_id: int, lines: list[str], duration_minutes: int):
        try:
            loop = asyncio.get_event_loop()
            end_time = loop.time() + duration_minutes * 60
            last_line = None
            while loop.time() < end_time:
                await asyncio.sleep(RANT_INTERVAL_SECONDS)
                choices = [l for l in lines if l != last_line] or lines
                line = random.choice(choices)
                last_line = line
                try:
                    await channel.send(line)
                except discord.HTTPException:
                    pass
        finally:
            self._active_channels.discard(channel_id)


async def setup(bot):
    await bot.add_cog(Lyrics(bot))
