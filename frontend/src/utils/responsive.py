import flet as ft

from constants.breakpoints import BREAKPOINT_LG, BREAKPOINT_MD, BREAKPOINT_SM

def get_width() -> ft.Number:
	return (ft.context.page.width or 0)

def is_small() -> bool:
	return get_width() <= BREAKPOINT_SM


def is_medium() -> bool:
	return get_width() > BREAKPOINT_SM and get_width() <= BREAKPOINT_MD


def is_large() -> bool:
	return get_width() > BREAKPOINT_MD and get_width() <= BREAKPOINT_LG

def is_extra_large() -> bool:
	return get_width() > BREAKPOINT_LG
