import flet as ft

from core.events import subscribeEvents
from core.router import routedPage
from state.app_state import AppState


@ft.component
def App() -> ft.Control:
	appState, _ = ft.use_state(AppState(route=ft.context.page.route))

	subscribeEvents(appState=appState)

	return routedPage()
