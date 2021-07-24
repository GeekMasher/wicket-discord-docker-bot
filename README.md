# wicket-discord-docker-bot

Wicket - The Discord Docker Bot to link your Docker deployments to Discord

This bot was created to make it easier for a Discord user to list, start, and stop Docker containers primarily for gaming servers.


## Setup

There are three core parts to setting up the bot; configuration file, Discord token, and Docker socket.


### Configuration file

```yml
domain: domain.example.com

# Discord servers
servers:
  example:
    name: Example Server Name
    admins:
      - MyUser#1234

docker-labels:
  - com.example.services.type=gaming

```

### Discord Token

To communicate to and from Discord you'll need an Application Discord Token to pass into the Bot.
This can be set as the environment variable `DISCORD_TOKEN`:

```
DISCORD_TOKEN=ABCDEFG
```

This can also be passed in manually using the `--token` argument.

```bash
pipenv run python -m wicket --token $MY_DISCORD_TOKEN
```

### Docker Socket

To connect to the Doker daemon you'll need access to the Docker socket on the local or remote machine.

This is done by connecting to the local system Docker enviroment using a number of methods including the `DOCKER_HOST` environment variable.

```env
# Local Unix Socket
DOCKER_HOST=/var/run/docker.sock

# Remote Socket
DOCKER_HOST=ssh://user@1.1.1.1

```

