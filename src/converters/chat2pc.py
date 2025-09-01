# chat2pc.py
# Databasify converter script: chat format to prompt-completion
# before: {"messages": [{"role": "user", "content": "user query"}, {"role": "assistant", "content": "assistant response"}]}
# after: {"prompt": "user query", "completion": "assistant response"}

import json

def chat2pc(data):
    return [{"prompt": item["messages"][0]["content"], "completion": item["messages"][1]["content"]} for item in data]

def convert_chat_to_pc(data):
    if isinstance(data, str):
        data = [json.loads(line) for line in data.split('\n') if line.strip()]
    return chat2pc(data)