# Log Hooks

A discord webhook logging library

There are no docs as this isn't meant to be used in bots that are sharded or log a lot. Just ping moanie#6598 on discord.py for help (ID: 691406006277898302)

⚠️⚠️⚠️ DO NOT USE THIS IN HIGH LEVEL BOTS. THIS IS FINE IN PERSONAL BOTS OR LOW LEVEL BOTS THAT ARE NOT SHARDED AND THAT DO NOT LOG. THIS LIBRARY DOES NOT IMPLEMENT A QUEUE, BUT YOU CAN IMPLEMENT ONE ON YOUR OWN BY SUBCLASSING WEBHOOK HANDLER OR MAKING YOUR OWN SYSTEM. THIS IS A QUICKLY PUT TOGETHER LIBRARY AND SHOULD NOT BE HEAVILY DEPENDED UPON ⚠️⚠️⚠️

Example:
```py
import discord
import logging
import aiohttp

from loghooks import WebhookHandler

client = discord.Client() # use commands.Bot if you wish. It doesn't make a difference.
handler = WebhookHandler(
    webhook_url = "webhook-url",
    session = aiohttp.ClientSession()
)


@client.event
async def on_ready():
    print("ready")


# actual logging stuff
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
handler.setLevel(logging.INFO)

client.run("Bot Token")
```

## Using your own functions

```py
import discord
import logging
import aiohttp

from loghooks import WebhookHandler
from logging import LogRecord

client = discord.Client() # use commands.Bot if you wish. It doesn't make a difference.
handler = WebhookHandler(
    webhook_url = "webhook-url",
    session = aiohttp.ClientSession()
)


@client.event
async def on_ready():
    print("ready")


async def my_custom_webhook_function(log: LogRecord):
    ... # handle your log here

# actual logging stuff
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
handler.setLevel(logging.INFO)
handler.setCustomHandle(my_custom_webhook_function)

client.run("Bot Token")
```