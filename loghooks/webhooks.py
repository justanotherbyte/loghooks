import discord
import aiohttp


def create_adapter(session: aiohttp.ClientSession):
    if discord.__version__.startswith("1.7"):
        adapter = discord.AsyncWebhookAdapter(session)
        return adapter
    elif discord.__version__.startswith("2"):
        return session
    


def create_webhook(webhook_url: str, session: aiohttp.ClientSession) -> discord.Webhook:
    adapter_or_session = create_adapter(session)
    if discord.__version__.startswith("1.7"):
        webhook = discord.Webhook.from_url(webhook_url, adapter = adapter_or_session)
        return webhook
    elif discord.__version__.startswith("2"):
        webhook = discord.Webhook.from_url(webhook_url, session = adapter_or_session)
        return webhook