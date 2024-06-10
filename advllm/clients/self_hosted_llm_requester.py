import requests
from fastapi import  WebSocket
from typing import List
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("websocket")

class SelfHostedLLMRequester:
    def __init__(self, base_url: str, headers: dict, model: str):
        self.base_url = base_url
        self.headers = headers
        self.model = model

    def send_request(self, message: str) -> dict:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }
        try:
            response = requests.post(self.base_url + "/v1/chat/completions", headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending request to self-hosted LLM: {e}")
            return {"error": str(e)}

class WebSocketConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New connection: {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Disconnected: {websocket.client}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
        logger.info(f"Sent message to {websocket.client}: {message}")

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
            logger.info(f"Broadcasted message: {message}")


class Message(BaseModel):
    content: str




