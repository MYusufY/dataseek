# Datasetify universal dataset format converter
# usage: python3 universal.py -i pc/iio/chat -o pc/iio/chat /path/to/your/dataset

import json
import argparse
import sys
from pathlib import Path

from pc2chat import convert_pc_to_chat
from pc2iio import convert_pc_to_iio
from iio2pc import convert_iio_to_pc
from iio2chat import convert_iio_to_chat
from chat2iio import convert_chat_to_iio
from chat2pc import convert_chat_to_pc

def load_jsonl_file(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data

def save_jsonl_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

def main():
    parser = argparse.ArgumentParser(description='Databasify format converter')
    parser.add_argument('-i', '--input-format', required=True, choices=['pc', 'iio', 'chat'], 
                       help='Input format: pc (prompt-completion), iio (instruction-input-output), chat')
    parser.add_argument('-o', '--output-format', required=True, choices=['pc', 'iio', 'chat'],
                       help='Output format: pc (prompt-completion), iio (instruction-input-output), chat')
    parser.add_argument('filename', help='Input JSONL filename')
    
    args = parser.parse_args()
    
    if not Path(args.filename).exists():
        print(f"Error: File '{args.filename}' not found")
        sys.exit(1)
    
    try:
        input_data = load_jsonl_file(args.filename)
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)
    
    conversion_map = {
        ('pc', 'iio'): convert_pc_to_iio,
        ('pc', 'chat'): convert_pc_to_chat,
        ('iio', 'pc'): convert_iio_to_pc,
        ('iio', 'chat'): convert_iio_to_chat,
        ('chat', 'iio'): convert_chat_to_iio,
        ('chat', 'pc'): convert_chat_to_pc
    }
    
    if (args.input_format, args.output_format) not in conversion_map:
        print(f"Error: Conversion from {args.input_format} to {args.output_format} is not supported")
        sys.exit(1)
    
    try:
        converter = conversion_map[(args.input_format, args.output_format)]
        output_data = converter(input_data)
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)
    
    input_stem = Path(args.filename).stem
    output_filename = f"{input_stem}-{args.input_format}2{args.output_format}.jsonl"
    
    try:
        save_jsonl_file(output_data, output_filename)
        print(f"Successfully converted {args.input_format} to {args.output_format}")
        print(f"Output saved to: {output_filename}")
    except Exception as e:
        print(f"Error saving output file: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()