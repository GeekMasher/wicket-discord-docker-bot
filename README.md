# wicket-discord-docker-bot


## Setup

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

```bash
pipenv run python -m wicket --token $MY_DISCORD_TOKEN
```

Or this can be set as the environment variable `DISCORD_TOKEN`:

```
DISCORD_TOKEN=ABCDEFG
```

### Docker Socket

```env

DOCKER_HOST=/var/run/docker.sock

# Remote Socket
DOCKER_HOST=ssh://user@1.1.1.1

```

