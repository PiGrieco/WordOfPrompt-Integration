import requests

class SelfHostedLLMRequester:
    """
    Class for sending requests to a self-hosted language model.
    """

    def __init__(self, config):
        """
        Initializes the SelfHostedLLMRequester instance.

        Args:
            config (Config): The configuration object containing base URL, headers, and prompt messages.
        """
        self.base_url = config.base_url
        self.headers = config.headers

    def send_request(self, payload):
        """
        Sends a request to the self-hosted language model.

        Args:
            payload (dict): The payload to be sent with the HTTP request.

        Returns:
            dict: The response JSON returned by the model.
        """
        response = requests.post(self.base_url, headers=self.headers, json=payload)
        return response.json()