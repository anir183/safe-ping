import flet as ft

from constants.fonts import FONT_MD
from constants.images import AVATAR_SM


@ft.component
def CircAvatar(
	fallback: str,
	src: str,
	size: int = AVATAR_SM,
):
	return ft.CircleAvatar(
		radius=size // 2,
		foreground_image_src=src,
		content=ft.Text(
			fallback,
			size=FONT_MD,
			weight=ft.FontWeight.BOLD,
		),
	)
