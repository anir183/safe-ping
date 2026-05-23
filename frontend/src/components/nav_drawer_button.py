from typing import Any, Callable

import flet as ft

from constants.spacing import Spacing


@ft.component
def NavDrawerButton(
	*,
	label: str,
	icon: ft.IconData,
	selected: bool = False,
	on_click: Callable[[ft.Event[ft.TextButton]], Any] | None = None,
):
	return ft.TextButton(
		width=float("inf"),
		icon=icon,
		content=label,
		on_click=on_click,
		style=ft.ButtonStyle(
			padding=ft.Padding.symmetric(
				horizontal=Spacing.MD,
				vertical=Spacing.LG,
			),
			alignment=ft.Alignment.CENTER_LEFT,
			shape=ft.RoundedRectangleBorder(radius=12),
			bgcolor=(ft.Colors.SURFACE_CONTAINER_HIGHEST if selected else None),
		),
	)
