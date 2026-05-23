from collections.abc import Callable
from dataclasses import dataclass

import flet as ft

from constants.navigation import NavID


@dataclass(frozen=True)
class NavigationContextValue:
	selected: NavID
	set_selected: Callable[[NavID], None]


NavigationContext = ft.create_context(
	NavigationContextValue(
		selected=NavID.DASH,
		set_selected=lambda _: None,
	)
)
