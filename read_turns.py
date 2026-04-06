import json
with open('Output/json/Study_European-AI-Standards_FINAL_Turn8_Task2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('turns_proper.txt', 'w', encoding='utf-8') as fout:
    for i, conv in enumerate(data[0]['conversations']):
        fout.write(f'=== Turn {i} ({conv.get("role")}) ===\n')
        fout.write(conv.get("content", "") + '\n\n')
