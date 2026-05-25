import logging

import flet as ft

from components.primitives.avatar import CircAvatar
from components.styles.button_style import ButtonStyle
from constants.fonts import FONT_MD, FONT_SM
from constants.images import AVATAR_MD, AVATAR_SM
from constants.spacing import SPACE_LG, SPACE_SM, SPACE_XS
from constants.styles import STYLE_RADIUS_MD
from models.user import User

logger = logging.getLogger(__name__)


def user_initials(user: User) -> str:
	fallback_initials = user.name.strip().split()

	if len(fallback_initials) == 0:
		return "?"

	if len(fallback_initials) == 1:
		return fallback_initials[0][:2].upper()

	return (fallback_initials[0][0] + fallback_initials[-1][0]).upper()


def __on_menu_select(e: ft.Event[ft.PopupMenuButton]):
	action = e.control.data

	if action == "logout":
		logger.info("logout clicked")


def UserMenuCompact(user: User):
	return ft.PopupMenuButton(
		style=ButtonStyle(),
		content=CircAvatar(
			fallback=user_initials(user),
			src=user.avatar_src,
			size=AVATAR_MD,
		),
		items=[
			ft.PopupMenuItem(
				content="Logout", icon=ft.Icons.LOGOUT, data="logout"
			),
		],
		on_select=__on_menu_select,
	)


def UserMenuExpanded(
	user: User,
	is_button: bool = False,
):
	user_data = ft.Container(
		border_radius=STYLE_RADIUS_MD,
		padding=ft.Padding.symmetric(
			horizontal=SPACE_SM,
			vertical=SPACE_XS,
		),
		content=ft.Row(
			spacing=SPACE_LG,
			controls=[
				CircAvatar(
					fallback=user_initials(user),
					src=user.avatar_src,
					size=AVATAR_SM,
				),
				ft.Column(
					spacing=0,
					controls=[
						ft.Text(
							user.name,
							size=FONT_MD,
							weight=ft.FontWeight.W_500,
						),
						ft.Text("online", size=FONT_SM, opacity=0.7),
					],
				),
			],
		),
	)

	if not is_button:
		return user_data

	return ft.PopupMenuButton(
		style=ButtonStyle(),
		tooltip="User Menu",
		content=user_data,
		items=[
			ft.PopupMenuItem(
				content="Logout",
				icon=ft.Icons.LOGOUT,
				data="logout",
			),
		],
		on_select=__on_menu_select,
	)
