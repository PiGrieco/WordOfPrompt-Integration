
from advllm.clients.self_hosted_llm_requester import ListenerServer

# Example usage

def start_websocket_server():
    base_url = "http://localhost:11434"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    model = "llama2"
    llm_requester = ListenerServer(base_url, headers, model)
    llm_requester.start_websocket_server()

if __name__ == "__main__":
    start_websocket_server()