# chat2iio.py
# Databasify converter script: chat format to instruction-input-output
# before: {"messages": [{"role": "user", "content": "user query"}, {"role": "assistant", "content": "assistant response"}]}
# after: {"instruction": "user query", "input": "", "output": "assistant response"}

import json

def chat2iio(data):
    return [{"instruction": item["messages"][0]["content"], "input": "", "output": item["messages"][1]["content"]} for item in data]

def convert_chat_to_iio(data):
    if isinstance(data, str):
        data = [json.loads(line) for line in data.split('\n') if line.strip()]
    return chat2iio(data)