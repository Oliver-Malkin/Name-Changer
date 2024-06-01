import lightbulb

from ChannelChanger.bot import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import timezone

plugin = lightbulb.Plugin("changer")

names = ("🕴️-jacobs-fun-house", "🕴️-okeh-boom-ray")
flag = 0

CHANNEL_ID = 430424765337960449

@plugin.command
@lightbulb.command("switch", "Manually advance the name of the memes channel")
@lightbulb.implements(lightbulb.SlashCommand)
async def switch(ctx: lightbulb.SlashContext) -> None:
    await change()
    await ctx.respond("Done")

async def change() -> None:
    global flag
    flag += 1
    if flag >= len(names):
        flag = 0

    await plugin.bot.rest.edit_channel(CHANNEL_ID, name=names[flag])

scheduler = AsyncIOScheduler()
scheduler.configure(timezone = timezone.utc)
scheduler.start()
scheduler.add_job(change, trigger="cron", hour="00", minute="00")

def load(bot: Bot) -> None:
    bot.add_plugin(plugin)

def unload(bot: Bot) -> None:
    scheduler.shutdown()
    bot.remove_plugin("changer")