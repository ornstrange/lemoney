from util import readline_at_0
import logging
import tempfile
import asyncio
from modules import all

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    tfs = tempfile.TemporaryFile(mode='w+')

    def notify():
        print(readline_at_0(tfs))

    loop = asyncio.get_event_loop()
    kill = loop.run_until_complete(
        all.modules['battery']({
            'fs': tfs,
            'notify': notify
        })
    )

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        kill()
        loop.close()

