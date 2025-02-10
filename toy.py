import asyncio
import websockets

# set pc to False to run on device instead of pc
pc = True
if pc:
    import record_pc as record
    import player_pc as player
else:
    import record
    import player


async def main():

    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        record_q = asyncio.Queue() # record -> websocket
        player_q = asyncio.Queue() # websocket -> player

        asyncio.create_task(player.play(player_q))
        asyncio.create_task(record.record(record_q))

        async def send_buf():
            while True:
                buf = await record_q.get()
                # print("send buf size ", len(buf))
                await websocket.send(buf)
        asyncio.create_task(send_buf())


        while True:
            data = await websocket.recv()
            # print("recv buf size ", len(data))
            player_q.put_nowait(data)



if __name__ == "__main__":
    asyncio.run(main())