#!/usr/bin/env python3
"""Apply a minimal MiB/KiB compatibility patch for online-judge-tools.

Behavior:
- If upstream already supports MiB/KiB, this script does nothing (no-op).
- Otherwise, it applies a minimal in-place patch to onlinejudge/service/atcoder.py.
"""

from __future__ import annotations

import argparse
import datetime as dt
import inspect
import re
import shutil
import sys
from pathlib import Path


def is_upstream_fixed(source: str) -> bool:
    regex_supports_mib = bool(
        re.search(
            r"parsed_memory_limit\s*=\s*re\.search\(\s*r['\"][^'\"]*(KB\|MB\|KiB\|MiB|KiB\|MiB)[^'\"]*['\"]",
            source,
        )
    )
    has_unit_branch = "memory_limit_unit == 'MiB'" in source or "memory_limit_unit == \"MiB\"" in source
    has_table_branch = "tds[3].text.endswith(' MiB')" in source or 'tds[3].text.endswith(" MiB")' in source
    return regex_supports_mib and has_unit_branch and has_table_branch


def apply_minimal_patch(source: str) -> tuple[str, bool]:
    changed = False
    patched = source

    old_table_block = (
        "        elif tds[3].text.endswith(' MB'):\n"
        "            memory_limit_byte = int(float(utils.remove_suffix(tds[3].text, ' MB')) * 1000 * 1000)  # TODO: confirm this is MB truly, not MiB\n"
    )
    add_table_block = (
        "        elif tds[3].text.endswith(' MB'):\n"
        "            memory_limit_byte = int(float(utils.remove_suffix(tds[3].text, ' MB')) * 1000 * 1000)  # TODO: confirm this is MB truly, not MiB\n"
        "        elif tds[3].text.endswith(' KiB'):\n"
        "            memory_limit_byte = int(float(utils.remove_suffix(tds[3].text, ' KiB')) * 1024)\n"
        "        elif tds[3].text.endswith(' MiB'):\n"
        "            memory_limit_byte = int(float(utils.remove_suffix(tds[3].text, ' MiB')) * 1024 * 1024)\n"
    )
    if "tds[3].text.endswith(' MiB')" not in patched:
        if old_table_block in patched:
            patched = patched.replace(old_table_block, add_table_block, 1)
            changed = True
        else:
            raise RuntimeError("Could not find table-row MB block to patch.")

    old_regex_line = "parsed_memory_limit = re.search(r'^(メモリ制限|Memory Limit): ([0-9.]+) (KB|MB)', memory_limit)"
    new_regex_line = "parsed_memory_limit = re.search(r'^(メモリ制限|Memory Limit): ([0-9.]+) (KB|MB|KiB|MiB)', memory_limit)"
    if "(KB|MB|KiB|MiB)" not in patched:
        if old_regex_line in patched:
            patched = patched.replace(old_regex_line, new_regex_line, 1)
            changed = True
        else:
            raise RuntimeError("Could not find parsed_memory_limit regex line to patch.")

    old_unit_block = (
        "        elif memory_limit_unit == 'MB':\n"
        "            memory_limit_byte = int(float(memory_limit_value) * 1000 * 1000)\n"
    )
    add_unit_block = (
        "        elif memory_limit_unit == 'MB':\n"
        "            memory_limit_byte = int(float(memory_limit_value) * 1000 * 1000)\n"
        "        elif memory_limit_unit == 'KiB':\n"
        "            memory_limit_byte = int(float(memory_limit_value) * 1024)\n"
        "        elif memory_limit_unit == 'MiB':\n"
        "            memory_limit_byte = int(float(memory_limit_value) * 1024 * 1024)\n"
    )
    if "memory_limit_unit == 'MiB'" not in patched:
        if old_unit_block in patched:
            patched = patched.replace(old_unit_block, add_unit_block, 1)
            changed = True
        else:
            raise RuntimeError("Could not find memory_limit_unit MB block to patch.")

    return patched, changed


def find_target_file() -> Path:
    import onlinejudge.service.atcoder as atcoder  # type: ignore

    file_path = inspect.getsourcefile(atcoder) or atcoder.__file__
    if not file_path:
        raise RuntimeError("Failed to locate onlinejudge.service.atcoder module file.")
    return Path(file_path).resolve()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Only check whether patch is needed.")
    parser.add_argument(
        "--backup-dir",
        default="/tmp",
        help="Directory where a backup file is saved when patching (default: /tmp).",
    )
    args = parser.parse_args()

    target = find_target_file()
    source = target.read_text(encoding="utf-8")

    if is_upstream_fixed(source):
        print(f"[NOOP] Upstream already supports MiB/KiB: {target}")
        return 0

    if args.check:
        print(f"[NEEDED] Patch is required: {target}")
        return 1

    patched, changed = apply_minimal_patch(source)
    if not changed:
        print(f"[NOOP] No changes required: {target}")
        return 0

    backup_dir = Path(args.backup_dir).resolve()
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = backup_dir / f"{target.name}.bak-mibpatch-{stamp}"
    shutil.copy2(target, backup_path)

    target.write_text(patched, encoding="utf-8")
    print(f"[PATCHED] {target}")
    print(f"[BACKUP]  {backup_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        raise SystemExit(2)
