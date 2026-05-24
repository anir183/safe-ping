import asyncio
import logging

import flet as ft

from constants.dimensions import DIM_WIN_MIN_HEIGHT, DIM_WIN_MIN_WIDTH
from constants.fonts import FONT_BODY, FONT_FILES
from constants.info import APP_TITLE
from state.app_state import AppState

logger = logging.getLogger(__name__)


def subscribe_events(app_state: AppState) -> None:
	page = ft.context.page

	def update_theme():
		logger.info(
			"theme mode changed",
			extra={
				"theme-mode": app_state.theme_mode,
				"theme-color": app_state.theme_color,
			},
		)

		page.theme_mode = app_state.theme_mode
		page.theme = page.dark_theme = ft.Theme(
			color_scheme_seed=app_state.theme_color,
			font_family=FONT_BODY,
		)

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

		_ = asyncio.create_task(app_state.load_theme())

	page.on_resize = app_state.on_resize
	ft.on_updated(update_theme, [app_state.theme_mode, app_state.theme_color])
	ft.on_mounted(on_mounted)
