import json

class ConfigHF:
    """
    Configuration class for storing model parameters.

    Attributes:
        model_id (str): The ID of the Hugging Face model.
        api_token (str): The API token for accessing the Hugging Face Inference API.
    """
    
    def __init__(self, model_id, api_token):
        """
        Initializes the Config instance.

        Args:
            model_id (str): The ID of the Hugging Face model.
            api_token (str): The API token for accessing the Hugging Face Inference API.
        """
        self.model_id = model_id
        self.api_token = api_token

    @classmethod
    def from_json(cls, json_file):
        """
        Creates a Config instance from a JSON file.

        Args:
            json_file (str): The path to the JSON file containing model parameters.

        Returns:
            Config: An instance of the Config class.
        """
        with open(json_file, 'r') as f:
            config_data = json.load(f)
        return cls(config_data['model_id'], config_data['api_token'])





class ConfigLLM:
    """
    Class for storing configuration parameters.
    """

    def __init__(self, base_url, headers, prompt):
        """
        Initializes the Config instance.

        Args:
            base_url (str): The base URL of the self-hosted language model endpoint.
            headers (dict): The headers to be sent with the HTTP request.
            prompt (list): The list of prompt messages.
        """
        self.base_url = base_url
        self.headers = headers
        self.prompt_template = prompt

    def Prompt(self, model_name="llama2", messages=None):
        """
        Generates an example payload for sending a request to the self-hosted language model.

        Args:
            model_name (str, optional): The name of the model to query. Defaults to "llama2".
            messages (list, optional): A list of messages to send to the model. Defaults to None.

        Returns:
            dict: The example payload to be sent with the HTTP request.
        """
        if messages is None:
            messages = self.prompt_template
        return {
            "model": model_name,
            "messages": messages
        }



