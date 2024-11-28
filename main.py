import asyncio
import sys

from bot.utils import logger
from bot.utils.launcher import process


async def main():
    await process()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("<cyan>Bot stopped by user!</cyan>")
        sys.exit(2)