import flet as ft

from state.app_state import AppState


def subscribeEvents(appState: AppState) -> None:
	page = ft.context.page

	page.on_route_change = appState.route_change
