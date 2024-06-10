import requests
from pydantic import BaseModel, Field
from typing import Dict, Any

class Message(BaseModel):
    PROMPT: str = Field(...)
    INTENT: bool = Field(...)

class OpenTheVault:
    def __init__(self, api: str, Prompt: str, intent_Score: float, Statu: bool = False) -> None:
        self.ENDPOINT = api  # Replace with your actual endpoint
        self.Data = {
            "PROMPT": Prompt,
            "Intent_Score": intent_Score
        }
        self.Statu = Statu
        self.Headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer YOUR_API_KEY'  # Replace YOUR_API_KEY with your actual API key
        }

    @property
    def __getstate__(self) -> bool:
        return self.Statu

    def get_data(self) -> Message:
        if self.__getstate__:
            return Message(**self.Data)
        else:
            raise ValueError("State is not active")

    def send_request(self) -> Dict[str, Any]:
        if self.__getstate__:
            send_prompt = self.get_data().dict()
            try:
                response = requests.post(self.ENDPOINT, headers=self.Headers, json=send_prompt)
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                print(f"Error sending request: {e}")
                return {"error": str(e)}
        else:
            raise ValueError("State is not active")
