from collections.abc import Callable

import flet as ft

from utils.responsive import is_extra_large, is_large, is_medium, is_small

def ResponsiveComponent(
	*,
	small: Callable[[], ft.Control] | None = None,
	medium: Callable[[], ft.Control] | None = None,
	large: Callable[[], ft.Control] | None = None,
	extra_large: Callable[[], ft.Control] | None = None,
	fallback: Callable[[], ft.Control] | None = None,
) -> ft.Control:
	if is_small() and small:
		return small()

	if is_medium() and medium:
		return medium()

	if is_large() and large:
		return large()

	if is_extra_large() and extra_large:
		return extra_large()

	if fallback is not None:
		return fallback()

	return ft.Container(
		width=0,
		height=0,
	)
