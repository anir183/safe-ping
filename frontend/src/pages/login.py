import asyncio
import logging

import flet as ft

from components.primitives.avatar import CircAvatar
from components.primitives.logo import Logo
from components.styles.button_style import ButtonStyle
from components.util.platform import PlatformComponent
from constants.fonts import FONT_HEADER, FONT_LG, FONT_SM
from constants.spacing import SPACE_LG, SPACE_MD, SPACE_SM, SPACE_XL
from constants.styles import STYLE_RADIUS_MD
from contexts.user import UserContext
from models.user import User
from repos.mock.user import MockUserRepository

logger = logging.getLogger(__name__)


def user_initials(user: User) -> str:
	parts = user.name.strip().split()
	if len(parts) == 0:
		return "?"
	if len(parts) == 1:
		return parts[0][:2].upper()
	return (parts[0][0] + parts[-1][0]).upper()


@ft.component
def LoginPage():
	user_context = ft.use_context(UserContext)

	users, set_users = ft.use_state([])
	loading, set_loading = ft.use_state(True)
	error, set_error = ft.use_state("")

	async def load_users():
		try:
			repo = MockUserRepository()
			result = await repo.get_users()
			set_users(result)
		except Exception as e:
			logger.exception("failed to load users")
			set_error(str(e))
		finally:
			set_loading(False)

	ft.use_effect(lambda: asyncio.create_task(load_users()), [])

	def select_user(user: User):
		user_context.set_user(user)

	def _build_body():
		if loading:
			return ft.Column(
				horizontal_alignment=ft.CrossAxisAlignment.CENTER,
				spacing=SPACE_LG,
				controls=[
					ft.Text(
						"Choose your profile",
						font_family=FONT_HEADER,
						size=FONT_LG,
					),
					ft.ProgressRing(),
				],
			)

		if error:
			return ft.Column(
				horizontal_alignment=ft.CrossAxisAlignment.CENTER,
				spacing=SPACE_LG,
				controls=[
					ft.Text("Failed to load users", size=FONT_SM, color=ft.Colors.ERROR),
					ft.Text(error, size=FONT_SM, color=ft.Colors.OUTLINE),
				],
			)

		return ft.Column(
			horizontal_alignment=ft.CrossAxisAlignment.CENTER,
			spacing=SPACE_LG,
			controls=[
				ft.Text(
					"Choose your profile",
					font_family=FONT_HEADER,
					size=FONT_LG,
				),
				ft.Text(
					"Pick a user to start chatting",
					size=FONT_SM,
					color=ft.Colors.OUTLINE,
				),
				ft.Divider(),
				ft.Column(
					spacing=SPACE_SM,
					controls=[
						ft.Container(
							border_radius=STYLE_RADIUS_MD,
							bgcolor=(
								ft.Colors.SURFACE_CONTAINER_HIGHEST
							),
							padding=SPACE_SM,
							content=ft.Column(
								spacing=SPACE_SM,
								controls=[
									ft.ListTile(
										leading=CircAvatar(
											user_initials(user),
											user.avatar_src,
										),
										title=ft.Text(user.name),
										subtitle=ft.Text(
											user.email,
											size=FONT_SM,
										),
										on_click=lambda _,
											u=user: select_user(u),
									),
								],
							),
						)
						for user in users
					],
				),
			],
		)

	return ft.Column(
		expand=True,
		alignment=ft.MainAxisAlignment.CENTER,
		horizontal_alignment=ft.CrossAxisAlignment.CENTER,
		spacing=SPACE_XL,
		controls=[
			Logo(),
			ft.Container(
				padding=ft.Padding.symmetric(
					horizontal=SPACE_XL,
					vertical=SPACE_LG,
				),
				bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
				border_radius=STYLE_RADIUS_MD,
				content=_build_body(),
			),
		],
	)
