import flet as ft

from components.primitives.avatar import CircAvatar
from components.styles.button_style import ButtonStyle
from constants.fonts import FONT_HEADER
from constants.images import AVATAR_MD, ICON_SM
from constants.room import ROOM_SECTION_CHAT
from constants.spacing import SPACE_LG, SPACE_SM, SPACE_XS
from constants.styles import STYLE_RADIUS_MD
from contexts.room import RoomContext
from contexts.theme import ThemeContext
from models.room import Room


@ft.component
def RoomList(
	*,
	rooms: list[Room],
	compact: bool = False,
):
	room_context = ft.use_context(RoomContext)
	theme_context = ft.use_context(ThemeContext)

	def switch_room(id: str):
		room_context.open(
			id,
			ROOM_SECTION_CHAT,
		)

	def room_initials(name: str) -> str:
		parts = name.strip().split()

		if len(parts) == 0:
			return "?"

		if len(parts) == 1:
			return parts[0][:2].upper()

		return (parts[0][0] + parts[-1][0]).upper()

	dashboard_selected = room_context.room is None

	if compact:
		return ft.ListView(
			expand=True,
			spacing=SPACE_SM,
			controls=[
				ft.Container(
					tooltip="Dashboard",
					border_radius=STYLE_RADIUS_MD,
					bgcolor=(
						ft.Colors.SURFACE_CONTAINER_HIGHEST
						if dashboard_selected
						else None
					),
					padding=SPACE_SM,
					on_click=lambda _: room_context.close(),
					content=ft.Icon(
						ft.Icons.DASHBOARD,
						size=ICON_SM,
						color=theme_context.primary.color_scheme_seed,
					),
				),
				ft.Divider(),
				*[
					ft.Container(
						tooltip=room.name,
						border_radius=STYLE_RADIUS_MD,
						bgcolor=(
							ft.Colors.SURFACE_CONTAINER_HIGHEST
							if room_context.room
							and room_context.room.name == room.name
							else None
						),
						padding=SPACE_XS,
						on_click=lambda _, id=room.id: switch_room(id),
						content=CircAvatar(
							room_initials(room.name),
							room.avatar,
							AVATAR_MD,
						),
					)
					for room in rooms
				],
			],
		)

	return ft.ListView(
		expand=True,
		spacing=SPACE_SM,
		controls=[
			ft.TextButton(
				width=float("inf"),
				icon=ft.Icons.DASHBOARD,
				content="Dashboard",
				on_click=room_context.close,
				style=ButtonStyle(
					bgcolor=(
						ft.Colors.SURFACE_CONTAINER_HIGHEST
						if dashboard_selected
						else None
					),
				),
			),
			ft.Divider(),
			ft.Text(
				"Chat Rooms",
				margin=SPACE_XS,
				font_family=FONT_HEADER,
			),
			*[
				ft.TextButton(
					width=float("inf"),
					content=ft.Row(
						spacing=SPACE_LG,
						controls=[
							CircAvatar(
								room_initials(room.name),
								room.avatar,
							),
							ft.Text(
								room.name,
								expand=True,
								overflow=(ft.TextOverflow.ELLIPSIS),
							),
						],
					),
					on_click=lambda _, id=room.id: switch_room(id),
					style=ButtonStyle(
						bgcolor=(
							ft.Colors.SURFACE_CONTAINER_HIGHEST
							if room_context.room
							and room_context.room.name == room.name
							else None
						),
					),
				)
				for room in rooms
			],
		],
	)
