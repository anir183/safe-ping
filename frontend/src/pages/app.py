import flet as ft

from components.app.room_list import RoomsList
from components.nav_drawer import NavDrawer
from components.styles.button_style import ButtonStyle
from constants.routes import ROUTE_ROOT
from contexts.room import RoomContext, RoomContextValue
from repos.mock.room import MockRoomRepository
from state.room_state import RoomState


@ft.component
def AppPage() -> ft.Control:
	drawer_expanded, set_drawer_expanded = ft.use_state(True)

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

	room_wrapped = RoomContext(
		value=room_context,
		callback=lambda: NavDrawer(
			is_dismissible=True,
			is_hidden=lambda: drawer_expanded,
			set_hidden=set_drawer_expanded,
			controls=[
				ft.TextButton(
					width=float("inf"),
					icon=ft.Icons.DASHBOARD,
					content="Dashboard",
					on_click=lambda: ft.context.page.navigate(ROUTE_ROOT),
					style=ButtonStyle(),
				),
				ft.Divider(),
				ft.Text(room_context.room_id or "None"),
				RoomsList(repo=MockRoomRepository()),
			],
		),
	)

	return room_wrapped
