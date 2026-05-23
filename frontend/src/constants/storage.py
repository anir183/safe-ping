from dataclasses import dataclass


@dataclass(frozen=True)
class StorageKeys:
	THEME_MODE: str = "theme_mode"
