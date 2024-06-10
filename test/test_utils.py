import asyncio
import json
import websockets
import requests
from aiohttp import ClientSession

class SelfHostedLLMRequester:
    """
    Base class for sending requests to a self-hosted language model.
    """

    def __init__(self, base_url, headers, model):
        """
        Initializes the SelfHostedLLMRequester instance.

        Args:
            base_url (str): The base URL of the language model API.
            headers (dict): The headers to be sent with the HTTP request.
            model (str): The name of the language model to be used.
        """
        self.base_url = base_url
        self.headers = headers
        self.model = model

    def send_request(self, payload):
        """
        Sends a request to the self-hosted language model.

        Args:
            payload (dict): The payload to be sent with the HTTP request.

        Returns:
            dict: The response JSON returned by the model.
        """
        response = requests.post(self.base_url + "/v1/chat/completions", headers=self.headers, json=payload)
        return response.json()

class ListenerServer(SelfHostedLLMRequester):
    """
    Listener server for processing prompts and interacting with AgenticRAG.
    """

    def __init__(self, base_url, headers, model, agenticrag_url):
        """
        Initializes the ListenerServer instance.

        Args:
            base_url (str): The base URL of the language model API.
            headers (dict): The headers to be sent with the HTTP request.
            model (str): The name of the language model to be used.
            agenticrag_url (str): The URL of the AgenticRAG service.
        """
        super().__init__(base_url, headers, model)
        self.agenticrag_url = agenticrag_url

    async def listen_to_message_using_websockets(self, websocket, path):
        """
        Listens for messages on a WebSocket connection and processes them.

        Args:
            websocket (WebSocket): The WebSocket connection to listen on.
            path (str): The path for the WebSocket connection.
        """
        async for message in websocket:
            try:
                message_dict = json.loads(message)
                if 'content' in message_dict:
                    message_content = message_dict.get("content", "")
                    print(f"Received message: {message_content}")

                    # Process the message with AgenticRAG
                    updated_message = await self.process_with_agenticrag(message_content)

                    # Send the updated message to the LLM
                    payload = {
                        "model": self.model,
                        "messages": [
                            {
                                "role": "user",
                                "content": updated_message
                            }
                        ]
                    }

                    response = self.send_request(payload)
                    response_str = json.dumps(response)

                    await websocket.send(response_str)
                else:
                    print("Received message without 'content' field")

            except websockets.exceptions.ConnectionClosed:
                print("Connection closed")
                break
            except Exception as e:
                print(f"Error: {e}")
                await websocket.send(json.dumps({"error": str(e)}))

    async def process_with_agenticrag(self, message):
        """
        Processes the message with AgenticRAG to update the session state.

        Args:
            message (str): The message content to be processed.

        Returns:
            str: The updated message content.
        """
        async with ClientSession() as session:
            async with session.post(self.agenticrag_url, json={"message": message}) as response:
                response_data = await response.json()
                products = response_data.get("products", "")
                updated_message = f"{message} {products}"
                return updated_message

    def start_websocket_server(self, host='localhost', port=8765):
        """
        Starts the WebSocket server to listen for messages and process them.

        Args:
            host (str): The hostname for the WebSocket server.
            port (int): The port for the WebSocket server.
        """
        start_server = websockets.serve(self.listen_to_message_using_websockets, host, port)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_server)
        print(f"WebSocket server is running on ws://{host}:{port}")
        loop.run_forever()


