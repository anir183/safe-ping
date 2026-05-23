import flet as ft


@ft.component
def App() -> ft.Control:
	return ft.Container(
		expand=True,
		content=ft.Placeholder(),
	)
