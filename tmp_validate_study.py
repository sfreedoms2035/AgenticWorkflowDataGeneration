"""Quick validation of all Study_European outputs."""
import subprocess, json, os, glob

json_dir = "Output/json"
files = sorted(glob.glob(os.path.join(json_dir, "Study_European*.json")))
print(f"Found {len(files)} Study_European JSON files\n")

pass_count = 0
fail_count = 0

for f in files:
    bn = os.path.basename(f)
    result = subprocess.run(
        ["python", ".agent/scripts/validate_task.py", f],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    try:
        report = json.loads(result.stdout)
        status = report.get("overall_status", "?")
        stats = report.get("stats", {})
        cot = stats.get("cot_chars", "?")
        ans = stats.get("answer_chars", "?")
        code = stats.get("code_lines", "?")
        if status == "PASS":
            pass_count += 1
            print(f"  PASS {bn}: CoT={cot}, Ans={ans}, Code={code}")
        else:
            fail_count += 1
            print(f"  FAIL {bn}: CoT={cot}, Ans={ans}, Code={code}")
            for cat, data in report.get("metrics", {}).items():
                for v in data.get("violations", []):
                    print(f"       [{cat}] {v}")
    except Exception as e:
        fail_count += 1
        print(f"  ERR  {bn}: {e}")

# Also check thinking files
think_dir = "Output/thinking"
think_files = sorted(glob.glob(os.path.join(think_dir, "Study_European*.txt")))
print(f"\n--- Thinking Files ({len(think_files)}) ---")
for tf in think_files:
    bn = os.path.basename(tf)
    with open(tf, "r", encoding="utf-8", errors="ignore") as fh:
        content = fh.read().strip()
    length = len(content)
    sentinel = content in ("[NO_THINKING_SECTION]", "[EXTRACTION_FAILED]") or content.startswith("[EXTRACTION_ERROR]")
    status = "EMPTY/SENTINEL" if sentinel or length < 100 else "OK"
    print(f"  {status:>15s} {bn}: {length} chars")

print(f"\n--- Summary: {pass_count} PASS, {fail_count} FAIL out of {len(files)} ---")
