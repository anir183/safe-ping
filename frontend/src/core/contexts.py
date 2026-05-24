from typing import Callable

import flet as ft

from contexts.route import RouteContext, RouteContextValue
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

	return RouteContext(
		value=route_context,
		callback=callback,
	)
