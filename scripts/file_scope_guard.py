#!/usr/bin/env python3
"""Verify changed files stay within an approved scope."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable


IGNORED_DIRS = {".git", ".hg", ".svn", "__pycache__", "node_modules"}


def run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def git_root(cwd: Path) -> Path | None:
    result = run_git(["rev-parse", "--show-toplevel"], cwd)
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip()).resolve()


def normalize_pattern(pattern: str) -> str:
    return pattern.strip().replace(os.sep, "/").lstrip("./")


def rel_path(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def path_matches(path: str, patterns: Iterable[str]) -> bool:
    normalized = normalize_pattern(path)
    for raw_pattern in patterns:
        pattern = normalize_pattern(raw_pattern)
        if not pattern:
            continue
        if normalized == pattern:
            return True
        if pattern.endswith("/") and normalized.startswith(pattern):
            return True
        if "/" not in pattern and fnmatch.fnmatch(normalized, pattern):
            return True
        if fnmatch.fnmatch(normalized, pattern):
            return True
        if fnmatch.fnmatch(normalized, f"{pattern}/**"):
            return True
    return False


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def walk_files(root: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for current_root, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in IGNORED_DIRS]
        current = Path(current_root)
        for filename in filenames:
            path = current / filename
            if path.is_file():
                files[rel_path(path, root)] = file_hash(path)
    return files


def load_snapshot(path: Path) -> dict[str, str]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict) or not isinstance(data.get("files"), dict):
        raise ValueError(f"Invalid snapshot file: {path}")
    return {str(key): str(value) for key, value in data["files"].items()}


def write_snapshot(path: Path, root: Path, scope: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "root": str(root),
        "scope": scope,
        "files": walk_files(root),
    }
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def changed_from_snapshot(root: Path, snapshot_path: Path) -> set[str]:
    before = load_snapshot(snapshot_path)
    after = walk_files(root)
    changed = set()
    for path, digest in after.items():
        if before.get(path) != digest:
            changed.add(path)
    for path in before:
        if path not in after:
            changed.add(path)
    try:
        changed.discard(rel_path(snapshot_path, root))
    except ValueError:
        pass
    return changed


def git_changed_files(root: Path) -> set[str]:
    changed: set[str] = set()

    status = run_git(["status", "--porcelain=v1", "-z", "--untracked-files=all"], root)
    if status.returncode != 0:
        raise RuntimeError(status.stderr.strip() or "git status failed")

    entries = [entry for entry in status.stdout.split("\0") if entry]
    index = 0
    while index < len(entries):
        entry = entries[index]
        code = entry[:2]
        path = entry[3:] if len(entry) > 3 else ""
        if not path:
            index += 1
            continue
        if "R" in code or "C" in code:
            changed.add(path)
            if index + 1 < len(entries):
                changed.add(entries[index + 1])
                index += 2
                continue
        else:
            changed.add(path)
        index += 1

    return changed


def check_scope(root: Path, scope: list[str], snapshot: Path | None) -> int:
    git_top = git_root(root)
    if git_top is not None:
        root = git_top
        changed = git_changed_files(root)
        mode = "git"
    elif snapshot is not None and snapshot.exists():
        changed = changed_from_snapshot(root, snapshot)
        mode = "snapshot"
    else:
        print(
            "No git repository found and no snapshot state exists. "
            "Run snapshot before editing.",
            file=sys.stderr,
        )
        return 2

    out_of_scope = sorted(path for path in changed if not path_matches(path, scope))
    in_scope = sorted(path for path in changed if path_matches(path, scope))

    print(f"mode: {mode}")
    print(f"changed files: {len(changed)}")
    if in_scope:
        print("in scope:")
        for path in in_scope:
            print(f"  {path}")
    if out_of_scope:
        print("out of scope:")
        for path in out_of_scope:
            print(f"  {path}")
        return 1
    print("all changed files are in scope")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default=".",
        help="Project root to inspect. Defaults to current directory.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    snapshot = subparsers.add_parser("snapshot", help="Record non-git baseline state.")
    snapshot.add_argument("--state", required=True, help="Snapshot JSON path.")
    snapshot.add_argument(
        "--scope",
        action="append",
        required=True,
        help="Allowed path or glob. Repeat for multiple scopes.",
    )

    check = subparsers.add_parser("check", help="Check changed files against scope.")
    check.add_argument("--state", help="Snapshot JSON path for non-git projects.")
    check.add_argument(
        "--scope",
        action="append",
        required=True,
        help="Allowed path or glob. Repeat for multiple scopes.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).resolve()
    if not root.exists() or not root.is_dir():
        print(f"Root is not a directory: {root}", file=sys.stderr)
        return 2

    if args.command == "snapshot":
        write_snapshot(Path(args.state), root, args.scope)
        print(f"snapshot written: {args.state}")
        return 0

    state = Path(args.state) if args.state else None
    return check_scope(root, args.scope, state)


if __name__ == "__main__":
    raise SystemExit(main())
