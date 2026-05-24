from typing import Callable

import flet as ft

from contexts.route import RouteContext, RouteContextValue
from contexts.theme import ThemeContext, ThemeContextValue
from state.app_state import AppState


@ft.component
def ContextWrapper(
	app_state: AppState,
	callback: Callable[[], ft.Control],
):
	navigate_callback = ft.use_callback(
		fn=lambda new_route: app_state.push_route(new_route),
		dependencies=[app_state.route],
	)

	route_context = ft.use_memo(
		calculate_value=lambda: RouteContextValue(
			route=app_state.route,
			navigate=navigate_callback,
		),
		dependencies=[app_state.route],
	)

	toggle_mode = ft.use_callback(
		lambda: app_state.toggle_theme(),
		dependencies=[app_state.theme_mode],
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
		callback=callback,
	)

	route_wrapped = RouteContext(
		value = route_context,
		callback=lambda: theme_wrapped,
	)

	return route_wrapped

