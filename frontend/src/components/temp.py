import flet as ft

from components.platform import PlatformComponent
from components.responsive import ResponsiveComponent
from constants.spacing import SPACE_MD
from contexts.room import RoomContext
from contexts.theme import ThemeContext


@ft.component
def Temp() -> ft.Control:
	room_context = ft.use_context(RoomContext)
	theme_context = ft.use_context(ThemeContext)

	def change_room():
		if room_context.room_id is None:
			room_context.open_room("test", None)
		else:
			room_context.close_room()

	return ft.Container(
		expand=True,
		alignment=ft.Alignment.CENTER,
		content=ft.Column(
			expand=True,
			alignment=ft.MainAxisAlignment.CENTER,
			horizontal_alignment=ft.CrossAxisAlignment.CENTER,
			spacing=SPACE_MD,
			controls=[
				ft.Text(f"Room: {room_context.room_id}"),
				ft.Text(f"{ft.context.page.width} x {ft.context.page.height}"),
				PlatformComponent(
					desktop=lambda: ft.Text("Desktop"),
					mobile=lambda: ft.Text("Mobile"),
					web=lambda: ft.Text("Web"),
					fallback=lambda: ft.Text("Fallback"),
				),
				ResponsiveComponent(
					small=lambda: ft.Text("Small"),
					medium=lambda: ft.Text("Medium"),
					large=lambda: ft.Text("Large"),
					extra_large=lambda: ft.Text("XLarge"),
					fallback=lambda: ft.Text("Fallback"),
				),
				ft.Button(
					f"{theme_context.mode.value}",
					on_click=theme_context.toggle_mode,
				),
				ft.Button(
					"room",
					on_click=change_room,
				),
			],
		),
	)
