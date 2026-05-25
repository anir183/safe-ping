import flet as ft

from constants.images import ICON_SM
from contexts.theme import ThemeContext


@ft.component
def ThemeToggle() -> ft.Control:
	theme = ft.use_context(ThemeContext)

	return ft.IconButton(
		icon=(
			ft.Icons.DARK_MODE
			if theme.mode == ft.ThemeMode.DARK
			else ft.Icons.LIGHT_MODE
		),
		tooltip="toggle theme",
		icon_size=ICON_SM,
		on_click=lambda _: theme.toggle_mode(),
	)
