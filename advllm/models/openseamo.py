import requests

class OpenSesameAPI:
    """
    Class for interacting with the OpenSeamo model to compute the intention of buying in a user API inference model hosted service.

    Attributes:
        config (Config): An instance of the Config class containing model parameters.
        api_url (str): The URL of the Hugging Face Inference API endpoint.
    """
    
    def __init__(self, config):
        """
        Initializes the OpenSeamoAPI instance.

        Args:
            config (Config): An instance of the Config class containing model parameters.
        """
        self.config = config
        self.api_url = f"https://api-inference.huggingface.co/models/{self.config.model_id}"

    def query(self, prompt):
        """
        Sends a query to the OpenSeamo model to compute the intention of buying.

        Args:
            prompt (str): The prompt to send to the model.

        Returns:
            dict: The response JSON returned by the model.
        """
        headers = {"Authorization": f"Bearer {self.config.api_token}"}
        payload = {"inputs": prompt}
        response = requests.post(self.api_url, headers=headers, json=payload)
        return response.json()
