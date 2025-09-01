# iio2chat.py
# Databasify converter script: instruction-input-output to chat format
# before: {"instruction": "user query", "input": "", "output": "assistant response"}
# after: {"messages": [{"role": "user", "content": "user query"}, {"role": "assistant", "content": "assistant response"}]}

import json

def iio2chat(data):
    return [{"messages": [{"role": "user", "content": item.get("instruction", "")}, {"role": "assistant", "content": item.get("output", "")}]} for item in data]

def convert_iio_to_chat(data):
    if isinstance(data, str):
        data = [json.loads(line) for line in data.split('\n') if line.strip()]
    return iio2chat(data)