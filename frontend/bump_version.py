#!/usr/bin/env python3

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent

PYPROJECT = ROOT / "pyproject.toml"
INFO = ROOT / "src/constants/info.py"


def get_git_hash() -> str:
	return (
		subprocess.check_output(
			["git", "rev-parse", "HEAD"],
			text=True,
		)
		.strip()[:10]
	)


def get_current_version() -> str:
	content = PYPROJECT.read_text(encoding="utf-8")

	match = re.search(
		r'^version\s*=\s*"(\d+\.\d+\.\d+)"$',
		content,
		flags=re.MULTILINE,
	)

	if match is None:
		raise RuntimeError("could not find version in pyproject.toml")

	return match.group(1)


def bump_patch(version: str) -> str:
	major, minor, patch = map(int, version.split("."))

	return f"{major}.{minor}.{patch + 1}"


def update_pyproject(version: str):
	content = PYPROJECT.read_text(encoding="utf-8")

	content = re.sub(
		r'^version\s*=\s*".*"$',
		f'version = "{version}"',
		content,
		flags=re.MULTILINE,
	)

	_ = PYPROJECT.write_text(content, encoding="utf-8")


def update_info(version: str, commit_hash: str):
	full_version = f"{version}:{commit_hash}"

	content = INFO.read_text(encoding="utf-8")

	content = re.sub(
		r'^(APP_VERSION\s*=\s*)".*"$',
		rf'\1"{full_version}"',
		content,
		flags=re.MULTILINE,
	)

	_ = INFO.write_text(content, encoding="utf-8")


def main():
	current_version = get_current_version()

	new_version = bump_patch(current_version)

	commit_hash = get_git_hash()

	update_pyproject(new_version)

	update_info(new_version, commit_hash)

	print(f"updated version -> {new_version}:{commit_hash}")


if __name__ == "__main__":
	main()
