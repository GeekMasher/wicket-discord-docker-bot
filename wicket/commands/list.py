import docker
import discord


LIST_CONTAINERS = """\
Currently Services:
{servers}
"""


async def botListServices(client, message: discord.Message, **kargvs):

    client = docker.from_env()

    labels = kargvs.get("config", {}).get("docker-labels", [])

    containers = client.containers.list(all=True, filters={"label": labels})

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

        port = container.labels.get("wicket.services.port", None)

        if not port:
            container_ports = container.attrs.get("NetworkSettings", {}).get(
                "Ports", {}
            )
            for _, port_data in container_ports.items():
                # Pick first port that is forwarded
                port = int(port_data[0].get("HostPort"))
                break

        if port:
            server_string = (
                f"[steam://connect/{domain}:{port}](stream://connect/{domain}:{port})"
            )
        else:
            server_string = f"[steam://connect/{domain}](stream://connect/{domain})"

        embed.add_field(
            name=server,
            value=server_string,
            inline=False,
        )

    # await message.channel.send(LIST_CONTAINERS.format(servers="\n".join(servers)))
    await message.channel.send(embed=embed)
