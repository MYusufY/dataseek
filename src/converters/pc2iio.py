# pc2iio.py
# Databasify converter script: prompt-completion to instruction-input-output
# before: {"prompt": "user query", "completion": "assistant response"}
# after: {"instruction": "user query", "input": "", "output": "assistant response"}

import json

def pc2iio(data):
    return [{"instruction": item.get("prompt", ""), "input": "", "output": item.get("completion", "")} for item in data]

def convert_pc_to_iio(data):
    if isinstance(data, str):
        data = [json.loads(line) for line in data.split('\n') if line.strip()]
    return pc2iio(data)