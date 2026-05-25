from collections.abc import Callable
from dataclasses import dataclass

import flet as ft

from constants.colors import COLOR_ALT_DARK, COLOR_PRIMARY_DARK
from constants.fonts import FONT_BODY


@dataclass(frozen=True)
class ThemeContextValue:
	mode: ft.ThemeMode
	primary: ft.Theme
	secondary: ft.Theme
	toggle_mode: Callable[[], None]


ThemeContext = ft.create_context(
	ThemeContextValue(
		mode=ft.ThemeMode.DARK,
		primary=ft.Theme(
			color_scheme_seed=COLOR_PRIMARY_DARK,
			font_family=FONT_BODY,
		),
		secondary=ft.Theme(
			color_scheme_seed=COLOR_ALT_DARK,
			font_family=FONT_BODY,
		),
		toggle_mode=lambda: None,
	)
)
