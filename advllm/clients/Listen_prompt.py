import requests
import json
import websockets
import threading

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

class SelfHostedLLMWebsocketServer(SelfHostedLLMRequester):
    """
    Subclass of SelfHostedLLMRequester for starting a WebSocket server to listen for messages.
    """

    def __init__(self, base_url, headers, model):
        """
        Initializes the SelfHostedLLMWebsocketServer instance.

        Args:
            base_url (str): The base URL of the language model API.
            headers (dict): The headers to be sent with the HTTP request.
            model (str): The name of the language model to be used.
        """
        super().__init__(base_url, headers, model)

    def listen_to_message_using_websockets(self, ws_url, process_message_fn):
        """
        Listens for messages on a WebSocket connection and sends them to the language model.

        Args:
            ws_url (str): The URL of the WebSocket server to connect to.
            process_message_fn (callable): A function to process the message before sending it to the language model.
        """
        ws = websockets.connect(ws_url)

        while True:
            data = ws.recv()

            message_dict = json.loads(data)

            message = message_dict.get("content", "")

            processed_message = process_message_fn(message)

            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": processed_message
                    }
                ]
            }

            response = self.send_request(payload)

            response_str = json.dumps(response)

            ws.send(response_str)



    def start_websocket_server(self, process_message_fn=None):
        """
        Starts a WebSocket server to listen for messages and sends them to the language model.

        Args:
            process_message_fn (callable, optional): A function to process the message before sending it to the language model.
        """
        # convert the base URL from HTTP to WebSocket
        ws_url = self.base_url.replace("http://", "ws://")

        # use the subclass's listen_to_message_using_websockets method
        listen_thread = threading.Thread(target=self.listen_to_message_using_websockets, args=(ws_url, process_message_fn or self.process_message))
