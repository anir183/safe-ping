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


def update_pyproject(version: str):
	content = PYPROJECT.read_text(encoding="utf-8")

	content = re.sub(
		r'^version\s*=\s*".*"$',
		f'version = "{version}"',
		content,
		flags=re.MULTILINE,
	)

	_ = PYPROJECT.write_text(content, encoding="utf-8")


def update_info(version: str):
	content = INFO.read_text(encoding="utf-8")

	content = re.sub(
		r'^(APP_VERSION\s*=\s*)".*"$',
		rf'\1"{version}"',
		content,
		flags=re.MULTILINE,
	)

	_ = INFO.write_text(content, encoding="utf-8")


def main():
	version = get_git_hash()

	update_pyproject(version)
	update_info(version)

	print(f"updated version -> {version}")


if __name__ == "__main__":
	main()
