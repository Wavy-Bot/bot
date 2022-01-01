import wavy

import asyncio
import uvloop

if __name__ == "__main__":
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(wavy.run(loop))
