import logging, os

from ChannelChanger import __version__
from ChannelChanger.bot import Bot
from datetime import datetime

if os.name != 'nt': # A better, faster version of asyncio for Linux
    import uvloop
    uvloop.install()

def rename_log():
    os.rename("logs/latest.txt", f"logs/{datetime.now().strftime('%d-%m-%Y %I-%M-%S-%p')}.txt")

if __name__ == '__main__':
    # Does some logging stuff
    """
    if os.path.exists("logs/latest.txt"):
        rename_log() # prevents overiding a log in the event of catastrophic failure before
    elif not os.path.exists("logs/"):
        os.mkdir("logs/")
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%d-%m-%Y %H:%M:%S', filename="logs/latest.txt", encoding="utf-8", level=logging.INFO) # Open a logging file
    """
    bot = Bot()
    bot.run()

    logging.shutdown() # Stops the logging and allows for the file to be renamed
    #rename_log()
