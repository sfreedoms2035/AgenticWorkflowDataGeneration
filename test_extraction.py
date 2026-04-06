import sys
import run_gemini_playwright_v2

raw_text = """!!!!!METADATA!!!!!
{
"TD_TD_ID": "TD-CODING-Study_European-AI-Standards_FINAL-T7t1-20260406-v1.0",
"prompt_version": "CodingTasks_v1.0",
"model_used_generation": "Gemini-3.1-pro",
"knowledge_source_date": "2025-03-24",
"task_classification": "REGULATORY",
"affected_role": "Senior DevOps Engineer",
"programming_language": "C++",
"difficulty": "84",
"task_type": "coding_task",
"conversations": [],
"key_words": ["Automotive AI", "ISO 26262"],
"summary": "Implement a real-time compliance validation engine",
"evaluation_criteria": ["C++ Production Quality"]
}
!!!!!REASONING!!!!!
1. Initial Query Analysis...
!!!!!REQUIREMENTS!!!!!
[
{
"req_id": "REQ-SW-001",
"description": "Compliance Engine must calculate statistical distance",
"pass_criteria": "Kullback-Leibler Divergence"
}
]
!!!!!ARCHITECTURE!!!!!
Our compliance verification architecture...
!!!!!CODE!!!!!
// Copyright by 4QDR.AI, AD knowledge Bot v1.0
#include <iostream>
int main() { return 0; }
!!!!!USAGE-EXAMPLES!!!!!
Our automotive compliance engine...
!!!!!DOCUMENTATION!!!!!
// Copyright by 4QDR.AI, AD knowledge Bot v1.0
# Automotive AI Compliance Verification Engine
!!!!!TEST-CRITERIA!!!!!
[
"REQ-SW-001 (Covariate Shift): Verify numerical stability"
]
!!!!!TURN-3-USER!!!!!
[No Thinking] How does the Mutex work?
!!!!!TURN-4-ASSISTANT_DATA!!!!!
!!!!!TURN-4-ASSISTANT!!!!!
The `std::lock_guard` strategy...
!!!!!TURN-5-USER!!!!!
[No Thinking] What is the worst-case?
!!!!!TURN-6-ASSISTANT_DATA!!!!!
!!!!!TURN-6-ASSISTANT!!!!!
The worst case is O(N).
"""

blocks = run_gemini_playwright_v2.extract_semantic_blocks(raw_text)
print("Extracted Blocks:", list(blocks.keys()))

metadata_raw = run_gemini_playwright_v2.clean_semantic_block(blocks.get("METADATA", "{}"))
print("Metadata Parsed:", metadata_raw)

import json_repair
try:
    print(json_repair.loads(metadata_raw))
except Exception as e:
    print("Metadata Error:", e)

# Test validate logic
assistant_content_obj = run_gemini_playwright_v2.validate_and_save_json(raw_text, "test_output.json")
if assistant_content_obj:
    print("VALIDATION SUCCESS")
else:
    print("VALIDATION FAILED")
