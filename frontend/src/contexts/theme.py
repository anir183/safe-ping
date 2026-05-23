from collections.abc import Callable
from dataclasses import dataclass

import flet as ft

from constants.colors import Colors


@dataclass(frozen=True)
class ThemeContextValue:
	mode: ft.ThemeMode
	seed_color: ft.Colors
	toggle_mode: Callable[[], None]


ThemeContext = ft.create_context(
	ThemeContextValue(
		mode=ft.ThemeMode.DARK,
		seed_color=Colors.DARK_SEED_COLOR,
		toggle_mode=lambda: None,
	)
)
