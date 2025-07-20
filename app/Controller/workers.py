# workers.py

import asyncio
from typing import Callable

task_queue = asyncio.Queue()

async def start_worker():
    while True:
        task = await task_queue.get()
        result = task['func']()
        task['future'].set_result(result)
        task_queue.task_done()


async def enqueue_task(func: Callable):
    loop = asyncio.get_event_loop()
    future = loop.create_future()
    await task_queue.put({'func': func, 'future': future})
    return await future
 