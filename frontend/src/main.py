import flet as ft


def main(page: ft.Page):
	page.add(
		ft.Container(
			expand=True,
			content=ft.Placeholder(),
		)
	)


_ = ft.run(main)
