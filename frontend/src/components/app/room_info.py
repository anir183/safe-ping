import asyncio

import flet as ft

from components.nav_drawer import NavDrawer
from components.nav_rail import NavRail
from components.primitives.avatar import CircAvatar
from components.primitives.empty import Empty
from components.primitives.user_entry import UserMenuExpanded, user_initials
from components.styles.button_style import ButtonStyle
from constants.fonts import FONT_HEADER
from constants.images import AVATAR_MD, ICON_MD, ICON_SM
from constants.room import (
	ROOM_SECTION_CHAT,
	ROOM_SECTION_NOTES,
	ROOM_SECTION_WHITEBOARD,
)
from constants.spacing import SPACE_NONE, SPACE_SM, SPACE_XL, SPACE_XS
from constants.styles import STYLE_RADIUS_MD
from contexts.room import RoomContext
from contexts.theme import ThemeContext
from repos.user import UserRepository
from utils.responsive import is_extra_large, is_large, is_medium, is_small


@ft.component
def RoomInfo(repo: UserRepository, compact: bool = False):
	room_context = ft.use_context(RoomContext)
	members, set_members = ft.use_state([])

	if room_context.room is None:
		return Empty()

	async def get_room_members():
		set_members(await repo.get_users())

	def fetch_members():
		_ = asyncio.create_task(get_room_members())

	ft.use_effect(
		fetch_members,
		[
			room_context.room,
			room_context.open_section,
		],
	)
	if is_small():
		fetch_members()

	if compact:
		theme_context = ft.use_context(ThemeContext)
		return ft.Column(
			expand=True,
			spacing=SPACE_SM,
			horizontal_alignment=ft.CrossAxisAlignment.CENTER,
			controls=[
				ft.Container(
					tooltip="Chat",
					border_radius=STYLE_RADIUS_MD,
					bgcolor=(
						ft.Colors.SURFACE_CONTAINER_HIGHEST
						if room_context.open_section == ROOM_SECTION_CHAT
						else None
					),
					padding=SPACE_SM,
					on_click=lambda: room_context.open(
						room_context.room and room_context.room.id,
						ROOM_SECTION_CHAT,
					),
					content=ft.Icon(
						ft.Icons.CHAT,
						size=ICON_SM,
						color=theme_context.primary.color_scheme_seed,
					),
				),
				ft.Container(
					tooltip="Whiteboard",
					border_radius=STYLE_RADIUS_MD,
					bgcolor=(
						ft.Colors.SURFACE_CONTAINER_HIGHEST
						if room_context.open_section == ROOM_SECTION_WHITEBOARD
						else None
					),
					padding=SPACE_SM,
					on_click=lambda: room_context.open(
						room_context.room and room_context.room.id,
						ROOM_SECTION_WHITEBOARD,
					),
					content=ft.Icon(
						ft.Icons.DRAW,
						size=ICON_SM,
						color=theme_context.primary.color_scheme_seed,
					),
				),
				ft.Container(
					tooltip="Notes",
					border_radius=STYLE_RADIUS_MD,
					bgcolor=(
						ft.Colors.SURFACE_CONTAINER_HIGHEST
						if room_context.open_section == ROOM_SECTION_NOTES
						else None
					),
					padding=SPACE_SM,
					on_click=lambda: room_context.open(
						room_context.room and room_context.room.id,
						ROOM_SECTION_NOTES,
					),
					content=ft.Icon(
						ft.Icons.NOTES,
						size=ICON_SM,
						color=theme_context.primary.color_scheme_seed,
					),
				),
				ft.Divider(),
				ft.Container(height=SPACE_NONE),
				ft.ListView(
					expand=True,
					spacing=SPACE_XL,
					controls=[
						*(
							[
								ft.Container(
									tooltip="Loading...",
									border_radius=STYLE_RADIUS_MD,
									padding=SPACE_SM,
									content=ft.Icon(
										ft.Icons.DOWNLOADING,
										size=ICON_MD,
										color=theme_context.primary.color_scheme_seed,
									),
								),
							]
							if len(members) <= 0
							else []
						),
						*[
							CircAvatar(
								fallback=user_initials(member),
								src=member.avatar_src,
								size=AVATAR_MD,
							)
							for member in members
						],
					],
				),
			],
		)

	return ft.Column(
		expand=True,
		spacing=SPACE_SM,
		horizontal_alignment=ft.CrossAxisAlignment.END,
		controls=[
			ft.TextButton(
				width=float("inf"),
				icon=ft.Icons.CHAT,
				content="Chat",
				on_click=lambda: room_context.open(
					room_context.room and room_context.room.id,
					ROOM_SECTION_CHAT,
				),
				style=ButtonStyle(
					bgcolor=(
						ft.Colors.SURFACE_CONTAINER_HIGHEST
						if room_context.open_section == ROOM_SECTION_CHAT
						else None
					),
				),
			),
			ft.TextButton(
				width=float("inf"),
				icon=ft.Icons.DRAW,
				content="Whiteboard",
				on_click=lambda: room_context.open(
					room_context.room and room_context.room.id,
					ROOM_SECTION_WHITEBOARD,
				),
				style=ButtonStyle(
					bgcolor=(
						ft.Colors.SURFACE_CONTAINER_HIGHEST
						if room_context.open_section == ROOM_SECTION_WHITEBOARD
						else None
					),
				),
			),
			ft.TextButton(
				width=float("inf"),
				icon=ft.Icons.NOTES,
				content="Notes",
				on_click=lambda: room_context.open(
					room_context.room and room_context.room.id,
					ROOM_SECTION_NOTES,
				),
				style=ButtonStyle(
					bgcolor=(
						ft.Colors.SURFACE_CONTAINER_HIGHEST
						if room_context.open_section == ROOM_SECTION_NOTES
						else None
					),
				),
			),
			ft.Divider(),
			ft.Text(
				"Members",
				margin=SPACE_XS,
				font_family=FONT_HEADER,
				align=ft.Alignment.CENTER_LEFT,
			),
			ft.ListView(
				expand=True,
				spacing=SPACE_SM,
				controls=[
					*(
						[
							ft.TextButton(
								width=float("inf"),
								icon=ft.Icons.DOWNLOADING,
								content="Loading...",
								style=ButtonStyle(),
							),
						]
						if len(members) <= 0
						else []
					),
					*[UserMenuExpanded(user=member) for member in members],
				],
			),
		],
	)


@ft.component
def RoomInfoBar(repo: UserRepository):
	room_context = ft.use_context(RoomContext)

	if room_context.room is None:
		return Empty()

	drawer_expanded, set_drawer_expanded = ft.use_state(
		is_large() or is_extra_large()
	)

	drawer = NavDrawer(
		is_dismissible=is_small() or is_medium(),
		is_hidden=lambda: drawer_expanded,
		is_right=True,
		set_hidden=set_drawer_expanded,
		controls=[RoomInfo(repo)],
	)

	rail = NavRail(
		expand=lambda: set_drawer_expanded(True),
		is_right=True,
		controls=[RoomInfo(repo, True)],
	)

	return drawer if drawer_expanded else rail
