from dataclasses import dataclass


@dataclass(frozen=True)
class Spacing:
	NONE: int = 0
	XS: int = 6

	SM: int = 8
	MD: int = 12
	LG: int = 16

	XL: int = 20
	XXL: int = 24
