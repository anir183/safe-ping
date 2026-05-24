import flet as ft

from core.events import subscribe_events
from core.router import routed_page
from state.app_state import AppState


@ft.component
def App() -> ft.Control:
	app_state, _ = ft.use_state(
		initial=AppState(route=ft.context.page.route),
	)

	subscribe_events(app_state)

	return routed_page()
