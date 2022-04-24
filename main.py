import wavy

import asyncio
import uvloop

if __name__ == "__main__":
    print(
        r"""
 _       __                        
| |     / /  ____ _ _   __   __  __
| | /| / /  / __ `/| | / /  / / / /
| |/ |/ /  / /_/ / | |/ /  / /_/ / 
|__/|__/   \__,_/  |___/   \__, /  
                          /____/   
                          """
    )
    # Create new uvloop event loop, set it as the default, and run the bot.
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(wavy.run(loop))
    except KeyboardInterrupt:
        loop.stop()
