import re
import run_gemini_playwright_v2 as rg

text = r"""!!!!!METADATA!!!!!
```json
{
  "training_data_id": "TD-CODING-Study_European-AI-Standards",
  "prompt_version": "CodingTasks_v1.0"
}
```

!!!!!REASONING!!!!!
1. Initial Query Analysis & Scoping... (snip)

!!!!!TURN-1-USER!!!!!
[Thinking] ELITE AUTOMOTIVE Senior Requirements Engineering Manager...

!!!!!REQUIREMENTS!!!!!
```json
[
  {
    "req_id": "REQ-SW-VALID- perception-001"
  }
]
```

!!!!!ARCHITECTURE!!!!!
### AI Act Compliance Validation

!!!!!CODE!!!!!
```cpp
// Copyright by 4QDR.AI
```

!!!!!USAGE-EXAMPLES!!!!!
[Thinking] As the Senior Requirements...

!!!!!DOCUMENTATION!!!!!
// Copyright by 4QDR.AI, AD knowledge Bot v1.0

!!!!!TEST-CRITERIA!!!!!
```json
[
  "Boundary Test 1...",
  "Boundary Test 6..."
]
```

!!!!!TURN-3-USER!!!!!
[No Thinking] How is the framework's time complexity $O(N \cdot M)$ guaranteed...

!!!!!TURN-4-ASSISTANT!!!!!
[Thinking] Gemini-3.1-pro identified $O(N \cdot M)$ complexity...

!!!!!TURN-5-USER!!!!!
[No Thinking] I'm auditing our SOTIF gap results...

!!!!!TURN-6-ASSISTANT!!!!!
[Thinking] Gemini-3.1-pro specifically...
"""

print('=== Extracting Blocks ===')
blocks = rg.extract_semantic_blocks(text)
for k, v in blocks.items():
    print(f'Block: {k} (len {len(v)})')

print('\n=== Heuristic Extraction ===')
h_blocks = rg.heuristic_extract_blocks(text)
for k, v in h_blocks.items():
    print(f'Block: {k} (len {len(v)})')
