"""
fix_metadata.py — One-Time Batch Fixer for Existing JSON Outputs
================================================================
Retroactively corrects model_used_generation and date_of_generation
in ALL existing task JSON files in Output/json/.

model_used_generation -> "Gemini-3.1-pro"  (the actual model we use)
date_of_generation    -> today's actual date (2026-04-05)

Usage:
    python fix_metadata.py                  # Fix all files
    python fix_metadata.py --dry-run        # Show what would change, no writes
    python fix_metadata.py --date 2026-04-05  # Use specific date override
"""
import os
import sys
import json
import glob
import argparse
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_JSON_DIR = os.path.join(BASE_DIR, "Output", "json")

MODEL_CORRECT = "Gemini-3.1-pro"
DATE_CORRECT = datetime.now().strftime('%Y-%m-%d')


def fix_file(filepath, dry_run=False, date_override=None):
    target_date = date_override or DATE_CORRECT
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"  ❌ Could not parse {os.path.basename(filepath)}: {e}")
        return False, []

    if not isinstance(data, list) or len(data) == 0:
        print(f"  ⚠️ Skipping {os.path.basename(filepath)}: not a task array")
        return False, []

    task = data[0]
    changes = []

    old_model = task.get('model_used_generation', '<missing>')
    old_date  = task.get('date_of_generation',   '<missing>')

    if old_model != MODEL_CORRECT:
        changes.append(f"model: '{old_model}' → '{MODEL_CORRECT}'")
        if not dry_run:
            task['model_used_generation'] = MODEL_CORRECT

    if old_date != target_date:
        changes.append(f"date:  '{old_date}' → '{target_date}'")
        if not dry_run:
            task['date_of_generation'] = target_date

    if changes:
        if not dry_run:
            data[0] = task
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        return True, changes
    return False, []


def main():
    parser = argparse.ArgumentParser(description="Batch-fix model/date metadata in all task JSONs")
    parser.add_argument('--dry-run', action='store_true', help="Show changes without writing")
    parser.add_argument('--date', default=None, help="Override target date (YYYY-MM-DD)")
    args = parser.parse_args()

    json_files = sorted(glob.glob(os.path.join(OUTPUT_JSON_DIR, "*.json")))
    # Exclude backup files
    json_files = [f for f in json_files if '_backup_' not in os.path.basename(f) and '_raw_fail' not in os.path.basename(f)]

    mode = "DRY RUN" if args.dry_run else "LIVE FIX"
    print(f"\n{'═'*60}")
    print(f"  🔧 Batch Metadata Fixer [{mode}]")
    print(f"  📂 Directory: {OUTPUT_JSON_DIR}")
    print(f"  📋 Files found: {len(json_files)}")
    print(f"  🤖 Target model: {MODEL_CORRECT}")
    print(f"  📅 Target date:  {args.date or DATE_CORRECT}")
    print(f"{'═'*60}\n")

    fixed_count = 0
    unchanged_count = 0
    error_count = 0

    for filepath in json_files:
        name = os.path.basename(filepath)
        changed, changes = fix_file(filepath, dry_run=args.dry_run, date_override=args.date)
        if changed:
            fixed_count += 1
            prefix = "  [DRY] 🔄" if args.dry_run else "  ✅"
            print(f"{prefix} {name}")
            for c in changes:
                print(f"       {c}")
        else:
            unchanged_count += 1
            print(f"  ⏭️  {name} — already correct")

    print(f"\n{'─'*60}")
    if args.dry_run:
        print(f"  DRY RUN COMPLETE: {fixed_count} would change, {unchanged_count} already correct")
    else:
        print(f"  ✅ DONE: {fixed_count} files updated, {unchanged_count} already correct, {error_count} errors")
    print(f"{'═'*60}\n")


if __name__ == "__main__":
    main()
