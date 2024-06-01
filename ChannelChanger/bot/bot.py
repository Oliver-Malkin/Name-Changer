import logging, hikari, lightbulb

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc
from ChannelChanger import __version__

class Bot(lightbulb.BotApp):
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()
        self.scheduler.configure(timezone=utc)

        with open("./secrets/discord", mode="r", encoding="utf-8") as f:
            token = f.read().strip()

        super().__init__(
            token = token,
            default_enabled_guilds=(427217346835382273),
            help_slash_command=False,
            intents = hikari.Intents.GUILDS # For debugging just use all cos why not
            #intents = hikari.Intents.GUILD_MEMBERS # For sending messages
        )

    def run(self) -> None:
        self.event_manager.subscribe(hikari.StartingEvent, self.on_starting)            # When the bot it starting
        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)              # When the bot started
        self.event_manager.subscribe(hikari.StoppingEvent, self.on_stopping)            # When the bot is stopping
        self.event_manager.subscribe(hikari.StoppedEvent, self.on_stopped)              # When the bot stopped

        super().run(
            activity=hikari.Activity(
                name=f"Version {__version__}", # displays on the side, discord presence
                type=hikari.ActivityType.PLAYING
            )
        )

    async def on_starting(self, event: hikari.StartingEvent) -> None:
        self.load_extensions_from("./ChannelChanger/bot/extensions") # Load all extensions
        logging.info("All extensions loaded")

    async def on_started(self, event: hikari.StartedEvent) -> None:
        self.scheduler.start()
        await self.update_presence(status=hikari.Status.ONLINE)
        logging.info("BOT READY")

    async def on_stopping(self, event: hikari.StoppingEvent) -> None:
        self.scheduler.shutdown()
        await self.update_presence(status=hikari.Status.DO_NOT_DISTURB)
        logging.info("BOT STOPPING")

    async def on_stopped(self, event:hikari.StoppedEvent) -> None:
        logging.info("BOT STOPPED")
