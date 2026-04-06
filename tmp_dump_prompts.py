import pipeline

# Generate a sample prompt
p = pipeline.build_generation_prompt(('Rust', 96, 'Formalize'), 4, 1, 'Study_Test.pdf', 'REGULATORY')

# Generate a sample repair prompt (mock)
mock_report = {
    'needs_regeneration': [
        {'category': 'richness_and_complexity', 'issue': 'CoT too short: 5000 chars (min 9000)'},
        {'category': 'cot_structure', 'issue': 'Missing CoT parent headers: 5., 6., 7., 8.'},
    ]
}
r = pipeline.build_repair_prompt(mock_report, p, json_out_path=None)

# Partial repair prompt
import sys
sys.path.insert(0, '.agent/scripts')
import partial_repair
pr = partial_repair.build_repair_prompt.__code__  # Just check it compiles

with open('tmp_prompts_utf8.txt', 'w', encoding='utf-8') as out:
    out.write(f'=== GENERATION PROMPT ({len(p)} chars) ===\n')
    out.write(p)
    out.write(f'\n\n=== REPAIR PROMPT (without prev output context, {len(r)} chars) ===\n')
    out.write(r)
    out.write('\n\n=== PARTIAL REPAIR PROMPT (template, from partial_repair.py) ===\n')
    # Read directly from source
    import re
    src = open('.agent/scripts/partial_repair.py', 'r', encoding='utf-8').read()
    # Extract the prompt string
    match = re.search(r'prompt = f"""(.+?)"""', src, re.DOTALL)
    if match:
        out.write(match.group(1))
    out.write('\n')

print(f'Generation: {len(p)} chars')
print(f'Repair: {len(r)} chars')
print('Written to tmp_prompts_utf8.txt')
