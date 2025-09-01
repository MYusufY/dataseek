# pc2chat.py
# Databasify converter script: prompt-completion to chat format
# before: {"prompt": "user query", "completion": "assistant response"}
# after: {"messages": [{"role": "user", "content": "user query"}, {"role": "assistant", "content": "assistant response"}]}

import json

def pc2chat(data):
    return [{"messages": [{"role": "user", "content": item.get("prompt", "")}, {"role": "assistant", "content": item.get("completion", "")}]} for item in data]

def convert_pc_to_chat(data):
    if isinstance(data, str):
        data = [json.loads(line) for line in data.split('\n') if line.strip()]
    return pc2chat(data)