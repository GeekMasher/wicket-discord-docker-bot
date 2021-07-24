import docker
import discord


LIST_CONTAINERS = """\
Currently Services:
{servers}
"""


async def botListServices(client, message: discord.Message, **kargvs):

    client = docker.from_env()

    labels = client.__CONFIG__.get("docker-labels", [])

    containers = client.containers.list(all=True, filters={"label": labels.index(0)})

    if len(containers) == 0:
        await message.channel.send("❌ No Services online at this moment")
        return

    domain = kargvs.get("config", {}).get("domain", "N/A")

    embed = discord.Embed(
        title="Current Available Services",
        url=f"https://{domain}",
        description="All the currently available services",
        color=0xFF5733,
    )

    for container in containers:
        print("Container :: " + str(container.name))

        server = f"{container.name:<24}"

        if container.status == "running":
            server = "✅ " + server
        else:
            server = "⚠️ " + server

        port = container.labels.get("wicket.services.port", 0)

        embed.add_field(
            name=server,
            value=f"[steam://connect/{domain}:{port}](stream://connect/{domain}:{port})",
            inline=False,
        )

    # await message.channel.send(LIST_CONTAINERS.format(servers="\n".join(servers)))
    await message.channel.send(embed=embed)
