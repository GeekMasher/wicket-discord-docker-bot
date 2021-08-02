from typing import Container
import docker
import discord

from wicket.docker_utils import findContainers


async def botStartServices(client, message: discord.Message, **kargvs):

    client = docker.from_env()

    if len(kargvs.get("messages")) == 0:
        await message.channel.send(
            f"No service names were request, use the `list` command."
        )
        return

    for msg in kargvs.get("messages"):
        containers = findContainers(
            client, kargvs.get("config", {}), name=msg, guild=message.guild
        )

        container = containers[0]

        if container:
            print(container.status)

            if container.status == "paused":
                container.unpause()
                await message.channel.send(
                    f"Unpausing service `{msg}`. This might take a few minutes."
                )

            elif container.status == "running":
                await message.channel.send(
                    f"Service `{msg}` is already running, try using the `restart` command"
                )

            else:
                container.start()

                await message.channel.send(
                    f"Starting up service `{msg}`. This might take a few minutes."
                )

        else:
            await message.channel.send(f"Unable to find service name :: `{msg}`")


async def botStopServices(client, message: discord.Message, **kargvs):

    client = docker.from_env()

    if len(kargvs.get("messages")) == 0:
        await message.channel.send(
            f"No service names were request, use the `list` command."
        )
        return

    for msg in kargvs.get("messages"):
        containers = findContainers(
            client, kargvs.get("config", {}), name=msg, guild=message.guild
        )

        container = containers[0]

        if container:
            if container.status == "paused" or container.status == "stopped":
                await message.channel.send(
                    f"Service `{msg}` is already stopped/paused."
                )
            else:
                await message.channel.send(
                    f"Stopping service `{msg}`... This might take a few minutes."
                )

                container.stop(timeout=10)

                await message.channel.send(f"Service `{msg}` has been stopped.")

        else:
            await message.channel.send(f"Unable to find service name :: `{msg}`")


async def botRestartServices(client, message: discord.Message, **kargvs):

    client = docker.from_env()

    if len(kargvs.get("messages")) == 0:
        await message.channel.send(
            f"No service names were request, use the `list` command."
        )
        return

    for msg in kargvs.get("messages"):
        containers = findContainers(
            client, kargvs.get("config", {}), name=msg, guild=message.guild
        )

        container = containers[0]

        if container:
            await message.channel.send(
                f"Restarting `{msg}` service... This might take a few minutes."
            )

            if container.status == "running" or container.status == "paused":
                print("Container is being stopped...")
                container.stop(timeout=10)

            else:
                print("Container is already offline...")

            container.start()

            await message.channel.send(f"Service `{msg}` has been restarted.")

        else:
            await message.channel.send(f"Unable to find service name :: `{msg}`")


async def botUpdateServices(client, message: discord.Message, **kargvs):

    client = docker.from_env()

    if len(kargvs.get("messages")) == 0:
        await message.channel.send(
            f"No service names were request, use the `list` command."
        )
        return

    for msg in kargvs.get("messages"):
        containers = findContainers(
            client, kargvs.get("config", {}), name=msg, guild=message.guild
        )

        container = containers[0]

        if container:
            await message.channel.send(
                f"Updating `{msg}` service... This might take a few minutes."
            )

            # Pull
            image = container.image
            tag = image.tags[0]
            print(f"Image tag :: {tag}")

            try:
                new_image = client.images.pull(tag)

                print(f"Updating image: {new_image} ({new_image.short_id})")

            except Exception as err:
                print(f"Unable to pull image: {tag}")
                return

            if container.status == "running" or container.status == "paused":
                print("Container is being stopped...")
                container.stop(timeout=10)

            else:
                print("Container is already offline...")

            container.start()

            await message.channel.send(f"Service `{msg}` has been restarted.")

        else:
            await message.channel.send(f"Unable to find service name :: `{msg}`")
