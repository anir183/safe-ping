from dataclasses import dataclass


@dataclass(frozen=True)
class Dimensions:
	APP_BAR_HEIGHT: int = 36

	NAV_RAIL_WIDTH: int = 72
	SIDEBAR_WIDTH: int = 280

	WINDOW_MIN_WIDTH: int = 900
	WINDOW_MIN_HEIGHT: int = 510
