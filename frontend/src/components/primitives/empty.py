import flet as ft

@ft.component
def Empty() -> ft.Control:
	return ft.Container(
		margin=0,
		padding=ft.Padding(0, 0, 0, 0),
		width=0,
		height=0,
		expand=False,
	)
