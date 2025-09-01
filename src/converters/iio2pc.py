# iio2pc.py
# Databasify converter script: instruction-input-output to prompt-completion
# before: {"instruction": "user query", "input": "", "output": "assistant response"}
# after: {"prompt": "user query", "completion": "assistant response"}

import json

def iio2pc(data):
    return [{"prompt": item.get("instruction", ""), "completion": item.get("output", "")} for item in data]

def convert_iio_to_pc(data):
    if isinstance(data, str):
        data = [json.loads(line) for line in data.split('\n') if line.strip()]
    return iio2pc(data)