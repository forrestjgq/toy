import asyncio
import websockets

async def test_websocket():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        message = "Hello, WebSocket!"  # Example data block
        print(f"Sending: {message}")
        await websocket.send(message)

        response = await websocket.recv()
        print(f"Received from server: {response}")

if __name__ == "__main__":
    asyncio.run(test_websocket())
