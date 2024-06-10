
from advllm.clients.self_hosted_llm_requester import ListenerServer

# Example usage

def start_websocket_server():
    base_url = "http://localhost:11434"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    model = "llama2"
    agenticrag_url = "http://localhost:5000/process_message"  # URL of the AgenticRAG service
    llm_requester = ListenerServer(base_url, headers, model, agenticrag_url)
    llm_requester.start_websocket_server()

if __name__ == "__main__":
    start_websocket_server()