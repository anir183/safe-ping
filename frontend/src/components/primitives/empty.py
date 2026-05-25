import flet as ft

@ft.component
def Empty() -> ft.Control:
	return ft.Container(
		width=0,
		height=0,
	)
