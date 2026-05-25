import asyncio

import flet as ft

from components.app.room_list import RoomList
from components.nav_drawer import NavDrawer
from components.nav_rail import NavRail
from components.primitives.user_entry import UserMenuCompact, UserMenuExpanded
from components.styles.button_style import ButtonStyle
from constants.dimensions import DIM_INF
from constants.images import ICON_SM
from constants.spacing import SPACE_NONE
from contexts.room import RoomContext
from contexts.theme import ThemeContext
from models.user import User
from utils.responsive import is_extra_large, is_large, is_medium, is_small


@ft.component
def RoomNav():
	drawer_expanded, set_drawer_expanded = ft.use_state(
		is_large() or is_extra_large()
	)
	room_context = ft.use_context(RoomContext)
	theme_context = ft.use_context(ThemeContext)

	ft.use_effect(lambda: asyncio.create_task(room_context.refresh()), [])

	drawer = NavDrawer(
		is_dismissible=is_small() or is_medium(),
		is_hidden=lambda: drawer_expanded,
		set_hidden=set_drawer_expanded,
		controls=[
			RoomList(
				rooms=room_context.rooms,
				compact=False,
			),
			ft.TextButton(
				width=DIM_INF,
				icon=ft.Icons.ADD_CIRCLE,
				content="Add Room",
				tooltip="Add Room",
				on_click=None,
				style=ButtonStyle(),
			),
			ft.Divider(),
			ft.Container(
				alignment=ft.Alignment.CENTER,
				content=UserMenuExpanded(
					User(
						"0",
						"anir183",
						"email",
						"https://i.pravatar.cc/100",
					),
					is_button=True,
				),
			),
		],
	)

	rail = NavRail(
		expand=lambda: set_drawer_expanded(True),
		controls=[
			RoomList(
				rooms=room_context.rooms,
				compact=True,
			),
			ft.IconButton(
				icon=ft.Icons.ADD_CIRCLE,
				tooltip="Add Room",
				icon_size=ICON_SM,
				on_click=None,
				icon_color=theme_context.primary.color_scheme_seed,
			),
			ft.Divider(),
			ft.Container(
				alignment=ft.Alignment.CENTER,
				content=UserMenuCompact(
					User(
						"0",
						"anir183",
						"email",
						"https://i.pravatar.cc/100",
					),
				),
			),
			ft.Container(height=SPACE_NONE),
		],
	)

	return drawer if drawer_expanded else rail
