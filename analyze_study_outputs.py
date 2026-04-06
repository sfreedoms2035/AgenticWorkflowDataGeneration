"""Deep analysis of all Study_European-AI-Standards outputs and thinking files."""
import json
import os
import glob

OUTPUT_DIR = "Output/json"
THINKING_DIR = "Output/thinking"
EVAL_DIR = "Eval"

def analyze_thinking_file(path):
    """Check thinking file quality."""
    if not os.path.exists(path):
        return {"status": "MISSING", "chars": 0}
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if content.strip() == "[NO_THINKING_SECTION]":
        return {"status": "NO_THINKING", "chars": 0}
    if content.strip().startswith("[EXTRACTION"):
        return {"status": "EXTRACTION_FAILED", "chars": 0}
    return {"status": "OK", "chars": len(content)}

def analyze_json_task(path):
    """Analyze a single task JSON for quality issues."""
    issues = []
    if not os.path.exists(path):
        return {"exists": False, "issues": ["FILE_MISSING"]}
    
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not isinstance(data, list) or len(data) == 0:
        return {"exists": True, "issues": ["INVALID_STRUCTURE"]}
    
    task = data[0]
    convs = task.get("conversations", [])
    
    result = {
        "exists": True,
        "num_turns": len(convs),
        "issues": [],
    }
    
    # Check turn count
    if len(convs) != 6:
        result["issues"].append(f"WRONG_TURN_COUNT: {len(convs)}")
    
    # Check Turn 1 (user question)
    if len(convs) >= 1:
        t1 = convs[0].get("content", "")
        result["turn1_chars"] = len(t1)
        if len(t1) < 100:
            result["issues"].append(f"TURN1_TOO_SHORT: {len(t1)} chars")
    
    # Check Turn 2 (main assistant answer)
    if len(convs) >= 2:
        t2_content = convs[1].get("content", "")
        t2_reasoning = convs[1].get("reasoning", "")
        result["answer_chars"] = len(t2_content)
        result["reasoning_chars"] = len(t2_reasoning)
        
        # Check reasoning quality
        reasoning_clean = t2_reasoning.replace("<think>", "").replace("</think>", "").strip()
        if len(reasoning_clean) < 9000:
            result["issues"].append(f"COT_SHORT: {len(reasoning_clean)} chars (need 9000+)")
        
        # Check if content is valid JSON
        try:
            content_obj = json.loads(t2_content)
            if isinstance(content_obj, dict):
                code = content_obj.get("executable_code", "")
                code_lines = len(code.split("\\n")) if "\\n" in code else len(code.split("\n"))
                result["code_lines"] = code_lines
                if code_lines < 300:
                    result["issues"].append(f"CODE_SHORT: {code_lines} lines (need 300+)")
                
                reqs = content_obj.get("formal_requirements", [])
                result["req_count"] = len(reqs)
                if len(reqs) < 5:
                    result["issues"].append(f"FEW_REQUIREMENTS: {len(reqs)}")
                
                tests = content_obj.get("test_criteria", [])
                result["test_count"] = len(tests)
                if len(tests) < 5:
                    result["issues"].append(f"FEW_TESTS: {len(tests)}")
        except json.JSONDecodeError:
            result["issues"].append("ANSWER_NOT_JSON")
    
    # Check follow-up turns quality
    placeholder_patterns = [
        "Follow up", "Response 2", "TBD", "Logic verified",
        "How does this handle edge cases", "Follow up 2?",
        "(Write a", "(Ensure it", "BANNED VOCABULARY"
    ]
    
    for i in range(2, min(6, len(convs))):
        turn_content = convs[i].get("content", "")
        turn_num = i + 1
        result[f"turn{turn_num}_chars"] = len(turn_content)
        
        if len(turn_content) < 80:
            result["issues"].append(f"TURN{turn_num}_TOO_SHORT: {len(turn_content)} chars")
        
        for pattern in placeholder_patterns:
            if pattern.lower() in turn_content.lower():
                result["issues"].append(f"TURN{turn_num}_PLACEHOLDER: '{pattern}'")
                break
        
        # Check for word salad
        words = turn_content.lower().split()
        if len(words) > 20:
            from collections import Counter
            counts = Counter(words)
            top_word, top_freq = counts.most_common(1)[0]
            if top_freq > len(words) * 0.15 and top_word not in ["the", "a", "of", "to", "and", "in", "is", "for"]:
                result["issues"].append(f"TURN{turn_num}_WORDSALAD: '{top_word}' appears {top_freq}x in {len(words)} words")
    
    return result

# Analyze all Study files
print("=" * 80)
print("STUDY EUROPEAN AI STANDARDS - COMPREHENSIVE ANALYSIS")
print("=" * 80)

for turn in range(1, 9):
    for task_idx in range(1, 3):
        name = f"Study_European-AI-Standards_FINAL_Turn{turn}_Task{task_idx}"
        json_path = os.path.join(OUTPUT_DIR, f"{name}.json")
        think_path = os.path.join(THINKING_DIR, f"{name}.txt")
        
        print(f"\n{'─' * 60}")
        print(f"  {name}")
        print(f"{'─' * 60}")
        
        # Thinking analysis
        think = analyze_thinking_file(think_path)
        think_icon = "✅" if think["status"] == "OK" else "❌"
        print(f"  Thinking: {think_icon} {think['status']} ({think['chars']} chars)")
        
        # JSON analysis  
        result = analyze_json_task(json_path)
        if not result["exists"]:
            print(f"  JSON: ❌ FILE NOT FOUND")
            continue
        
        json_icon = "✅" if not result["issues"] else "⚠️"
        print(f"  JSON: {json_icon} {result.get('num_turns', '?')} turns")
        if "answer_chars" in result:
            print(f"    Answer: {result['answer_chars']} chars | CoT: {result['reasoning_chars']} chars")
        if "code_lines" in result:
            print(f"    Code: {result['code_lines']} lines | Reqs: {result.get('req_count', '?')} | Tests: {result.get('test_count', '?')}")
        for i in range(3, 7):
            if f"turn{i}_chars" in result:
                print(f"    Turn {i}: {result[f'turn{i}_chars']} chars")
        
        if result["issues"]:
            print(f"  ISSUES:")
            for issue in result["issues"]:
                print(f"    ❌ {issue}")

# Also analyze taxonomy for comparison
print(f"\n\n{'=' * 80}")
print("TAXONOMY THREAT MODELING - THINKING FILE CHECK")
print("=" * 80)

for turn in range(1, 9):
    for task_idx in range(1, 3):
        name = f"taxonomy-based_threat_modeling_Turn{turn}_Task{task_idx}"
        think_path = os.path.join(THINKING_DIR, f"{name}.txt")
        think = analyze_thinking_file(think_path)
        icon = "✅" if think["status"] == "OK" else "❌"
        print(f"  {icon} {name}: {think['status']} ({think['chars']} chars)")
