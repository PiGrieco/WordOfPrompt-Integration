from advllm.prompt_analyzer import PromptAnalyzer
from advllm.clients.inference_client import ConfigHF


# ConfigAPI =
# {
#     "model_id": "PiGrieco/OpenSesame",
#     "api_token": "hf_XXXXXXXX"
# }

prompt = "tell me which was the age of napoleon when he died"

config = ConfigHF.from_json("config.json")

prompt_analyzer = PromptAnalyzer(config, keywords_extracted=False) # 
is_match, keywords, intent_score, orignal_prompt  = prompt_analyzer.analyze_prompt(prompt)

print("Prompt Analysis Result:")
print(f"Is intent to buy: {is_match}")
print(f"Keywords: {keywords}")
print(f"Intent Score: {intent_score:.2f}")
print(f"Orignal Prompt: {orignal_prompt}")

   