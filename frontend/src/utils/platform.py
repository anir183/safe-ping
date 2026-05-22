from collections.abc import Callable

import flet as ft

DESKTOP_PLATFORMS = {
	ft.PagePlatform.WINDOWS,
	ft.PagePlatform.LINUX,
	ft.PagePlatform.MACOS,
}


MOBILE_PLATFORMS = {
	ft.PagePlatform.ANDROID,
	ft.PagePlatform.IOS,
}


def is_desktop() -> bool:
	return ft.context.page.platform in DESKTOP_PLATFORMS


def is_mobile() -> bool:
	return ft.context.page.platform in MOBILE_PLATFORMS


def is_web() -> bool:
	return ft.context.page.web


def platform_view(
	*,
	desktop: Callable[[], ft.Control] | None = None,
	mobile: Callable[[], ft.Control] | None = None,
	web: Callable[[], ft.Control] | None = None,
	fallback: Callable[[], ft.Control] | None = None,
) -> ft.Control:

	page = ft.context.page

	if page.web and web:
		return web()

	if is_desktop() and desktop:
		return desktop()

	if is_mobile() and mobile:
		return ft.SafeArea(expand=True, content=mobile())

	assert fallback is not None

	return fallback()
