import flet as ft

from constants.routes import ROUTE_ROOT
from contexts.theme import ThemeContext, ThemeContextValue
from core.events import subscribe_events
from core.router import Router
from state.app_state import AppState


@ft.component
def App() -> ft.Control:
	app_state, _ = ft.use_state(
		initial=AppState(route=ft.context.page.route),
	)

	subscribe_events(app_state)

	toggle_mode = ft.use_callback(
		lambda: app_state.toggle_theme(),
	)

	theme_context = ft.use_memo(
		lambda: ThemeContextValue(
			mode=app_state.theme_mode,
			seed_color=app_state.theme_color,
			toggle_mode=toggle_mode,
		),
		dependencies=[
			app_state.theme_mode,
			app_state.theme_color,
			toggle_mode,
		],
	)

	theme_wrapped = ThemeContext(
		value=theme_context,
		callback=lambda: ft.View(
			route=ROUTE_ROOT,
			appbar=None,
			controls=[
				ft.SafeArea(
					expand=True,
					content=Router(),
				),
			],
		),
	)

	return theme_wrapped
