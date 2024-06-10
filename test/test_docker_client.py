import asyncio
import websockets
import json

async def send_message():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        message = {
            "content": input()
        }
        await websocket.send(json.dumps(message))
        
        response = await websocket.recv()
        print(f"Received response: {response}")

asyncio.get_event_loop().run_until_complete(send_message())
