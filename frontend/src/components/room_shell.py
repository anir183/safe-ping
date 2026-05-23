import flet as ft

from constants.breakpoints import Breakpoints
from contexts.room import RoomContext


@ft.component
def RoomShell(id: str) -> ft.Control:
	room = ft.use_context(RoomContext)

	width, set_width = ft.use_state(ft.context.page.width or 0)

	def on_resize(_):
		set_width(ft.context.page.width or 0)

	ft.context.page.on_resize = on_resize

	is_large = width >= Breakpoints.LG
	is_medium = width >= Breakpoints.MD and width < Breakpoints.LG

	if is_large:
		return ft.Container(
			expand=True,
			alignment=ft.Alignment.CENTER,
			content=ft.Text(f"Large {id}"),
		)
	elif is_medium:
		return ft.Container(
			expand=True,
			alignment=ft.Alignment.CENTER,
			content=ft.Text(f"Medium {id}"),
		)

	return ft.Container(
		expand=True,
		alignment=ft.Alignment.CENTER,
		content=ft.Text(f"Small {id}"),
	)
