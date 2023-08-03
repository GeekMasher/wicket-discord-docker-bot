import discord

from wicket.commands.list import botListServices
from wicket.commands.docker_commands import *


async def botHelp(cxt, message: discord.Message, **kargvs):
    TEXT = "Help Options:\n"

    for name, command in COMMANDS.items():
        TEXT += f" - `{cxt.__PREFIX__} {name}` - {command.get('description')}"
        if command.get("auth"):
            TEXT += " (auth required)"
        TEXT += "\n"

    await message.channel.send(TEXT)


COMMANDS = {
    "help": {"func": botHelp, "auth": False, "description": "Get help with the bot"},
    "list": {
        "func": botListServices,
        "auth": False,
        "description": "Get a list of services",
    },
    "start": {
        "func": botStartServices,
        "auth": True,
        "description": "Start a service",
    },
    "restart": {
        "func": botRestartServices,
        "auth": True,
        "description": "Restart a service",
    },
    "stop": {
        "func": botStopServices,
        "auth": True,
        "description": "Stop a service",
    },
    "update": {
        "func": botUpdateServices,
        "auth": True,
        "description": "Update the service",
    },
}
