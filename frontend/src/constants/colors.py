from dataclasses import dataclass

import flet as ft


@dataclass(frozen=True)
class Colors:
	DARK_SEED_COLOR: ft.Colors = ft.Colors.LIME
	LIGHT_SEED_COLOR: ft.Colors = ft.Colors.LIME_900
