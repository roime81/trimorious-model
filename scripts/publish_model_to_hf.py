#!/usr/bin/env python3
"""Publish the reviewed GitHub model mirror to its Hugging Face model repo.

This uploads only the explicit model artifact allow-list. It does not delete
remote-only files, and it refuses Git LFS pointer files (which would otherwise
publish pointer text instead of the actual weights).
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from huggingface_hub import HfApi

ROOT = Path(__file__).resolve().parents[1]
REPO_ID = "roime81/trimorious-research-4B"

UPLOAD_FILES = [
    ".gitattributes",
    "LICENSE",
    "README.md",
    "adapter_config.json",
    "adapter_model.safetensors",
    "chat_template.jinja",
    "tokenizer.json",
    "tokenizer_config.json",
]

REQUIRED_FILES = [
    "LICENSE",
    "README.md",
    "adapter_config.json",
    "adapter_model.safetensors",
    "chat_template.jinja",
    "tokenizer.json",
    "tokenizer_config.json",
]


def fail(message: str) -> None:
    raise SystemExit(f"PRE-FLIGHT FAILED: {message}")


def main() -> int:
    token = os.environ.get("HF_TOKEN")
    if not token:
        fail("HF_TOKEN secret is not configured.")

    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.is_file():
            fail(f"Required model artifact is missing: {relative}")
        if path.stat().st_size == 0:
            fail(f"Required model artifact is empty: {relative}")

    # Git LFS files must be hydrated by actions/checkout with lfs: true.
    for relative in ("adapter_model.safetensors", "tokenizer.json"):
        path = ROOT / relative
        with path.open("rb") as handle:
            header = handle.read(200)
        if header.startswith(b"version https://git-lfs.github.com/spec/v1"):
            fail(
                f"{relative} is still an LFS pointer. Ensure checkout uses "
                "lfs: true and the GitHub LFS object is available."
            )
        if path.stat().st_size < 1024:
            fail(f"{relative} is unexpectedly small; refusing to publish.")

    adapter_config = json.loads((ROOT / "adapter_config.json").read_text(encoding="utf-8"))
    base_model = adapter_config.get("base_model_name_or_path")
    if not isinstance(base_model, str) or not base_model.strip():
        fail("adapter_config.json has no valid base_model_name_or_path.")

    print(f"Publishing adapter-only model mirror: {REPO_ID}")
    print(f"Declared base model: {base_model}")
    print("Files to upload:")
    for relative in UPLOAD_FILES:
        path = ROOT / relative
        if path.is_file():
            print(f"  {relative}: {path.stat().st_size:,} bytes")

    api = HfApi(token=token)
    api.model_info(REPO_ID)  # Refuse to create or redirect to an unexpected repo.
    commit = api.upload_folder(
        repo_id=REPO_ID,
        repo_type="model",
        folder_path=str(ROOT),
        allow_patterns=UPLOAD_FILES,
        commit_message=(
            "Sync reviewed model artifacts from GitHub "
            + os.environ.get("GITHUB_SHA", "manual-dispatch")
        ),
    )

    # Verify that expected model files are present after the upload.
    info = api.model_info(REPO_ID, files_metadata=True)
    remote_files = {item.rfilename for item in (info.siblings or [])}
    missing = sorted(set(REQUIRED_FILES).difference(remote_files))
    if missing:
        fail(f"Post-upload verification did not find remote files: {missing}")

    print("Hugging Face upload completed.")
    print(f"Commit: {getattr(commit, 'oid', 'unknown')}")
    print(f"Model: https://huggingface.co/{REPO_ID}")
    print("Remote file inventory check: passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
