import flet as ft


@ft.component
def HomePage() -> ft.Control:
	return ft.Container(
		expand=True,
		alignment=ft.Alignment.CENTER,
		content=ft.Text(f"{ft.context.page.width} x {ft.context.page.height}"),
	)
