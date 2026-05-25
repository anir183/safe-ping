import flet as ft

from components.app.room_info import RoomInfo, RoomInfoBar
from components.app.room_nav import RoomNav
from components.styles.button_style import ButtonStyle
from components.util.responsive import ResponsiveComponent
from constants.dimensions import DIM_APP_HEADER_HEIGHT
from constants.fonts import FONT_HEADER
from constants.spacing import SPACE_MD, SPACE_NONE
from contexts.room import RoomContext
from repos.mock.user import MockUserRepository
from utils.responsive import is_small


@ft.component
def ConditionalPage():
	return ft.Container(
		expand=True,
		content=ft.Placeholder(),
	)


@ft.component
def MainContent():
	room_context = ft.use_context(RoomContext)

	return ft.Column(
		expand=True,
		margin=SPACE_NONE,
		controls=[
			*(
				[
					ft.Row(
						margin=SPACE_NONE,
						alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
						controls=[
							ft.IconButton(
								icon=ft.Icons.ARROW_BACK,
								tooltip="back",
								style=ButtonStyle(),
								on_click=lambda: room_context.open(
									room_context.room and room_context.room.id,
									None,
								),
							),
							ft.Text(
								(
									room_context.room
									and room_context.room.name
									or "Dashboard"
								)
								+ " - "
								+ (room_context.open_section or "None"),
								font_family=FONT_HEADER,
								margin=SPACE_MD,
							),
						],
					),
				]
				if is_small()
				else []
			),
			ConditionalPage(),
		],
	)


@ft.component
def RoomPane():
	room_context = ft.use_context(RoomContext)

	if (
		is_small()
		and room_context.room is not None
		and room_context.open_section is not None
	):
		return MainContent()

	return ResponsiveComponent(
		small=lambda: ft.Row(
			expand=True,
			controls=[
				RoomNav(),
				RoomInfo(repo=MockUserRepository()),
			],
		),
		fallback=lambda: ft.Row(
			expand=True,
			controls=[
				RoomNav(),
				MainContent(),
				RoomInfoBar(repo=MockUserRepository()),
			],
		),
	)
