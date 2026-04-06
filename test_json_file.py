import json
try:
    with open('Output/json/Study_European-AI-Standards_FINAL_Turn8_Task2.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for i, conv in enumerate(data[0]['conversations']):
        print(f'Turn {i} Role: {conv.get("role")}')
        print(f'Content length: {len(conv.get("content", ""))}')
        print(f'Content preview: {repr(conv.get("content", "")[:50])}')
except Exception as e:
    print(e)
