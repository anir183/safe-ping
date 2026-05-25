import flet as ft

from components.app_bar import MobileAppBar
from components.app_header import AppHeader
from constants.routes import ROUTE_ROOT
from contexts.theme import ThemeContext, ThemeContextValue
from core.events import subscribe_events
from core.router import Router
from state.theme_state import ThemeState


@ft.component
def App() -> ft.Control:
	theme_state, _ = ft.use_state(
		initial=ThemeState(route=ft.context.page.route),
	)

	subscribe_events(theme_state)

	toggle_mode = ft.use_callback(
		lambda: theme_state.toggle_theme(),
		dependencies=[
			theme_state.theme_mode,
		],
	)

	theme_context = ft.use_memo(
		lambda: ThemeContextValue(
			mode=theme_state.theme_mode,
			primary=theme_state.theme_primary,
			secondary=theme_state.theme_secondary,
			toggle_mode=toggle_mode,
		),
		dependencies=[
			theme_state.theme_mode,
			theme_state.theme_primary,
			theme_state.theme_secondary,
			toggle_mode,
		],
	)

	theme_wrapped = ThemeContext(
		value=theme_context,
		callback=lambda: ft.View(
			route=ROUTE_ROOT,
			appbar=MobileAppBar(),
			controls=[
				AppHeader(),
				ft.SafeArea(
					expand=True,
					content=Router(),
				),
			],
		),
	)

	return theme_wrapped
