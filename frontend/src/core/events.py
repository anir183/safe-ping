import flet as ft

from state.app_state import AppState


def subscribe_events(app_state: AppState) -> None:
	page = ft.context.page

	page.on_route_change = app_state.on_route_change
