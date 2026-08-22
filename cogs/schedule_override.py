from datetime import datetime
import discord
from discord import app_commands
from discord.ext import commands
from .notification_event_types import (
    get_event_types, get_event_config, get_event_icon,
    get_reference_override, set_reference_override, calculate_next_occurrence,
)
from .permission_handler import PermissionManager
from .pimp_my_bot import theme

OVERRIDABLE_EVENTS = [
    name for name in get_event_types()
    if (get_event_config(name) or {}).get("reference_date")
]


class ScheduleOverride(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="overrideschedule",
        description="Fix an event's schedule if it's running on the wrong date for this server.",
    )
    @app_commands.describe(
        event="The event whose schedule is off",
        date="A date this event actually ran on your server, YYYY-MM-DD (leave blank to reset to default)",
    )
    @app_commands.choices(event=[
        app_commands.Choice(name=name, value=name) for name in OVERRIDABLE_EVENTS
    ])
    async def overrideschedule(
        self,
        interaction: discord.Interaction,
        event: app_commands.Choice[str],
        date: str = None,
    ):
        is_admin, _ = PermissionManager.is_admin(interaction.user.id)
        if not is_admin:
            await interaction.response.send_message(
                f"{theme.deniedIcon} You don't have permission to use this command!",
                ephemeral=True,
            )
            return

        event_name = event.value
        config = get_event_config(event_name)
        guild_id = interaction.guild_id

        if date is None or not date.strip():
            set_reference_override(guild_id, event_name, None)
            nxt = calculate_next_occurrence(event_name, guild_id=guild_id)
            nxt_text = nxt.strftime("%Y-%m-%d") if nxt else "-"
            await interaction.response.send_message(
                f"{theme.verifiedIcon} {get_event_icon(event_name)} **{event_name}** reset to "
                f"the default rotation. Next occurrence: `{nxt_text}`.",
                ephemeral=True,
            )
            return

        date = date.strip()
        try:
            parsed = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            await interaction.response.send_message(
                f"{theme.deniedIcon} Invalid date. Use YYYY-MM-DD (e.g. 2026-07-19).",
                ephemeral=True,
            )
            return

        default_ref = datetime.strptime(config["reference_date"], "%Y-%m-%d")
        if parsed.weekday() != default_ref.weekday():
            weekday = default_ref.strftime("%A")
            await interaction.response.send_message(
                f"{theme.deniedIcon} {event_name} runs on a {weekday}. Enter a {weekday} date.",
                ephemeral=True,
            )
            return

        set_reference_override(guild_id, event_name, date)
        nxt = calculate_next_occurrence(event_name, guild_id=guild_id)
        nxt_text = nxt.strftime("%Y-%m-%d") if nxt else "-"
        await interaction.response.send_message(
            f"{theme.verifiedIcon} {get_event_icon(event_name)} **{event_name}** reference date "
            f"set to `{date}`. Next occurrence: `{nxt_text}`.",
            ephemeral=True,
        )


async def setup(bot):
    await bot.add_cog(ScheduleOverride(bot))
