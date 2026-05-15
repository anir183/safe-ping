import flet as ft


def main(page: ft.Page):
	page.add(
		ft.SafeArea(
			expand=True,
			content=ft.Container(
				content=ft.Text("Safe Ping"),
				alignment=ft.Alignment.CENTER,
			),
		)
	)


_ = ft.run(main)
