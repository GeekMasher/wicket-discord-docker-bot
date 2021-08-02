import os
import argparse

import yaml
import docker
import discord

from wicket.commands import COMMANDS, botHelp


parser = argparse.ArgumentParser(__name__)

parser.add_argument(
    "-t", "--token", default=os.environ.get("DISCORD_TOKEN"), help="Discord Token"
)
parser.add_argument(
    "-a",
    "--admins",
    default=os.environ.get("DISCORD_ADMINS"),
    help="Discord List of Admins. Seperated by comma (,)",
)
parser.add_argument("--config", default="./data/config.yml")


from wicket.commands import COMMANDS


class WicketClient(discord.Client):

    __CONFIG__ = {}
    __PREFIX__ = "/wicket"

    def isAuthorized(self, message: discord.Message):
        #  Global admins
        admins = WicketClient.__CONFIG__.get("admins", [])
        if message.author in admins:
            return True

        # Per Server/Guide Configuration
        server_config = None
        for _, data in WicketClient.__CONFIG__.get("servers", {}).items():
            if data.get("name", "") == str(message.guild):
                server_config = data
                break

        if server_config:
            if server_config.get("channels"):
                if str(message.channel) not in server_config.get("channels"):
                    return False

            if str(message.author) in server_config.get("admins"):
                return True

        return False

    async def on_ready(self):
        print("Logged on as", self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if not message.content.startswith(WicketClient.__PREFIX__):
            print("Message is not for me...")
            return

        msg = message.content.replace(WicketClient.__PREFIX__ + " ", "", 1)

        commands = msg.split(" ")

        if len(commands) == 0:
            await botHelp(self, message)
            return

        base_command = commands.pop(0)

        ran_command = False

        for command_name, command in COMMANDS.items():
            if command.get("auth") and not self.isAuthorized(message):
                await message.channel.send(
                    f"Hmmm... What are you doing `{message.author}`!?"
                )
                return

            if command_name == base_command:
                command_function = command.get("func")
                await command_function(
                    self, message, config=WicketClient.__CONFIG__, messages=commands
                )
                ran_command = True
                break

        if not ran_command:
            await botHelp(self, message)
            return


if __name__ == "__main__":
    args = parser.parse_args()

    config = {}
    if os.path.exists(args.config):
        print(f"Loading config from :: {args.config}")

        with open(args.config, "r") as handle:
            config = yaml.safe_load(handle)

    admins = []
    if args.admins:
        admins.extend(args.admins.split(","))

    if not config.get("admins"):
        config["admins"] = []
    config["admins"].extend(admins)

    print(f"Admins :: {config['admins']}")

    for server, server_data in config.get("servers", {}).items():
        print(
            f"[+] Server({server}, admins=\"{server_data.get('admins')}\", labels=\"{server_data.get('labels', [])}\")"
        )

    #  Set the Wicket client's config
    WicketClient.__CONFIG__ = config

    client = docker.from_env()

    client = WicketClient(use_slash_commands=True)

    try:
        client.run(args.token)
    except Exception as err:
        print("Exiting...")
