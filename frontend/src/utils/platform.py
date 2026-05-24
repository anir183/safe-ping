import flet as ft

from constants.platforms import PLATFORMS_DESKTOP, PLATFORMS_MOBILE


def is_desktop() -> bool:
	return ft.context.page.platform in PLATFORMS_DESKTOP


def is_mobile() -> bool:
	return ft.context.page.platform in PLATFORMS_MOBILE


def is_web() -> bool:
	return ft.context.page.web
