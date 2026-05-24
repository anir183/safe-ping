import flet as ft

from core.contexts import ContextWrapper
from core.events import subscribe_events
from core.router import Router
from state.app_state import AppState


@ft.component
def App() -> ft.Control:
	app_state, _ = ft.use_state(
		initial=AppState(route=ft.context.page.route),
	)

	subscribe_events(app_state)

	return ContextWrapper(
		app_state=app_state,
		callback=Router
	)
