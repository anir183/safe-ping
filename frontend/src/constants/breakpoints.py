from dataclasses import dataclass


@dataclass(frozen=True)
class Breakpoints:
	SM: int = 640
	MD: int = 768
	LG: int = 1024
	XL: int = 1280
