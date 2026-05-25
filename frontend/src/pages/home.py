import flet as ft

from components.platform import PlatformComponent
from components.responsive import ResponsiveComponent
from contexts.room import RoomContext, RoomContextValue
from contexts.theme import ThemeContext
from state.room_state import RoomState


@ft.component
def temp() -> ft.Control:
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
				ft.Row(
					alignment=ft.MainAxisAlignment.CENTER,
					controls=[
						ft.Button(
							f"{theme_context.mode.value}",
							on_click=theme_context.toggle_mode
						),
						ft.Button(
							"Change Room",
							on_click=change_room
						),
					],
				),
			],
		),
	)


@ft.component
def HomePage() -> ft.Control:
	room_state, _ = ft.use_state(RoomState(room_id=None))

	open_room = ft.use_callback(
		lambda id, section: room_state.open_room(id, section),
		dependencies=[
			room_state.room_id,
			room_state.open_section,
		],
	)

	close_room = ft.use_callback(
		lambda: room_state.close_room(),
		dependencies=[
			room_state.room_id,
			room_state.open_section,
		],
	)

	room_context = ft.use_memo(
		lambda: RoomContextValue(
			room_id=room_state.room_id,
			open_section=room_state.open_section,
			open_room=open_room,
			close_room=close_room,
		),
		dependencies=[
			room_state.room_id,
			room_state.open_section,
			open_room,
			close_room,
		],
	)

	room_wrapped = RoomContext(value=room_context, callback=temp)

	return room_wrapped
