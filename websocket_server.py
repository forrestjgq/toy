import asyncio
import websockets
import argparse

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)  # Send it back unchanged

async def main(port):
    server = await websockets.serve(echo, "localhost", port)
    await server.wait_closed()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default=8765, type=int)
    args = parser.parse_args()

    
    asyncio.run(main(args.port))
