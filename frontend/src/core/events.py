import flet as ft

from constants.dimensions import DIM_WIN_MIN_HEIGHT, DIM_WIN_MIN_WIDTH
from constants.fonts import FONT_BODY, FONT_FILES
from constants.info import APP_TITLE
from state.app_state import AppState


def subscribe_events(app_state: AppState) -> None:
	page = ft.context.page

	def on_mounted():
		logger.info(
			"mounted page",
			extra={
				"width": page.width,
				"height": page.height,
			},
		)

		page.title = APP_TITLE
		page.fonts = FONT_FILES

		# remove title bar and buttons on desktop
		page.window.title_bar_hidden = True
		page.window.title_bar_buttons_hidden = True
		page.window.frameless = False

		# minimum window size and defaults for desktop
		page.window.resizable = True
		page.window.maximized = False
		page.window.min_width = DIM_WIN_MIN_WIDTH
		page.window.min_height = DIM_WIN_MIN_HEIGHT

	page.on_route_change = app_state.on_route_change
	page.on_view_pop = app_state.on_view_pop
	ft.on_mounted(on_mounted)
