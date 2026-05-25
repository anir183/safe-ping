from collections.abc import Callable

import flet as ft

from utils.platform import is_desktop, is_web, is_mobile

def PlatformComponent(
	*,
	desktop: Callable[[], ft.Control] | None = None,
	mobile: Callable[[], ft.Control] | None = None,
	web: Callable[[], ft.Control] | None = None,
	fallback: Callable[[], ft.Control] | None = None,
) -> ft.Control:
	if is_web() and web:
		return web()

	if is_desktop() and desktop:
		return desktop()

	if is_mobile() and mobile:
		return mobile()

	if fallback is not None:
		return fallback()

	return ft.Container(
		width=0,
		height=0,
	)
