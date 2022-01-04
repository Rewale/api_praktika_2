import asyncio
import datetime
import random


async def my_sleep_func():
    await asyncio.sleep(random.randint(0, 5))


async def display_date(num, event_loop):
    end_time = event_loop.time() + 50.0
    while True:
        print("Loop: {} Time: {}".format(num, datetime.datetime.now()))
        if (event_loop.time() + 1.0) >= end_time:
            break
        await my_sleep_func()


loop = asyncio.get_event_loop()

asyncio.ensure_future(display_date(1, loop))
asyncio.ensure_future(display_date(2, loop))

loop.run_forever()