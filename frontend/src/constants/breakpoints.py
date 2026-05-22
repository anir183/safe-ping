from dataclasses import dataclass

import flet as ft


@dataclass(frozen=True)
class Breakpoints:
	SM: int = 640
	MD: int = 768
	LG: int = 1024
	XL: int = 1280


def get_width() -> ft.Number:
	return ft.context.page.width or 0


def is_small() -> bool:
	return get_width() < Breakpoints.MD


def is_medium() -> bool:
	return Breakpoints.MD <= get_width() < Breakpoints.LG


def is_large() -> bool:
	return get_width() >= Breakpoints.LG
