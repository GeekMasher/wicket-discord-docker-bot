import docker


def findContainers(client, config, name=None, guild=None):
    labels = []

    if guild:
        found = False
        for _, guild_data in config.get("servers", {}).items():
            if guild_data.get("name") == str(guild):
                labels = guild_data.get("labels", [])
                found = True

        if not found:
            return []

    containers = client.containers.list(all=True, filters={"label": labels})

    filter = {}
    if name:
        filter["name"] = name
    if len(labels) <= 1:
        filter["label"] = labels

    containers = client.containers.list(
        all=True,
        filters=filter,
    )

    return containers
