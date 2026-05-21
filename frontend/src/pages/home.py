import flet as ft


@ft.component
def HomePage():
	return ft.Container(
		expand=True, content=ft.Text("Home"), alignment=ft.Alignment.CENTER
	)
