#!/usr/bin/env python3
"""Safely publish the reviewed GitHub adapter mirror to Hugging Face.

Only the explicit artifact allow-list is uploaded. Remote-only files are not
deleted. The script rejects unresolved Git LFS pointers.
"""
from __future__ import annotations

import argparse
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
    "CITATION.cff",
    "SECURITY.md",
    "adapter_config.json",
    "adapter_model.safetensors",
    "chat_template.jinja",
    "tokenizer.json",
    "tokenizer_config.json",
    "training_config.template.yaml",
    "evaluation_status.json",
]

REQUIRED_FILES = [
    "LICENSE",
    "README.md",
    "CITATION.cff",
    "SECURITY.md",
    "adapter_config.json",
    "adapter_model.safetensors",
    "chat_template.jinja",
    "tokenizer.json",
    "tokenizer_config.json",
    "training_config.template.yaml",
    "evaluation_status.json",
]


def fail(message: str) -> None:
    raise SystemExit(f"PRE-FLIGHT FAILED: {message}")


def validate_local_artifacts() -> str:
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

    evaluation = json.loads((ROOT / "evaluation_status.json").read_text(encoding="utf-8"))
    if evaluation.get("model") != REPO_ID:
        fail("evaluation_status.json refers to a different model repository.")

    print(f"Local artifact pre-flight passed for {REPO_ID}")
    print(f"Declared base model: {base_model}")
    for relative in UPLOAD_FILES:
        path = ROOT / relative
        if path.is_file():
            print(f"  {relative}: {path.stat().st_size:,} bytes")
    return base_model


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Validate local artifacts without contacting Hugging Face or requiring a token.",
    )
    parser.add_argument(
        "--revision",
        default=os.environ.get("HF_REVISION", "main"),
        help="Hugging Face branch to update (main for baseline, candidate/v1.1 etc. for a versioned candidate).",
    )
    args = parser.parse_args()

    if not args.revision.strip():
        fail("Target Hugging Face revision cannot be empty.")

    validate_local_artifacts()
    if args.check_only:
        print("Check-only mode: no Hugging Face write was attempted.")
        return 0

    token = os.environ.get("HF_TOKEN")
    if not token:
        fail("HF_TOKEN secret is not configured.")

    api = HfApi(token=token)
    api.model_info(REPO_ID)  # Refuse to create or redirect to an unexpected repo.
    if args.revision != "main":
        api.create_branch(
            repo_id=REPO_ID,
            branch=args.revision,
            repo_type="model",
            exist_ok=True,
        )
    commit = api.upload_folder(
        repo_id=REPO_ID,
        repo_type="model",
        folder_path=str(ROOT),
        revision=args.revision,
        allow_patterns=UPLOAD_FILES,
        commit_message=(
            "Sync reviewed model artifacts from GitHub "
            + os.environ.get("GITHUB_SHA", "manual-dispatch")
        ),
    )

    # Verify that expected model files are present after the upload.
    info = api.model_info(REPO_ID, revision=args.revision, files_metadata=True)
    remote_files = {item.rfilename for item in (info.siblings or [])}
    missing = sorted(set(REQUIRED_FILES).difference(remote_files))
    if missing:
        fail(f"Post-upload verification did not find remote files: {missing}")

    print("Hugging Face upload completed.")
    print(f"Commit: {getattr(commit, 'oid', 'unknown')}")
    print(f"Model revision: https://huggingface.co/{REPO_ID}/tree/{args.revision}")
    print("Remote file inventory check: passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
