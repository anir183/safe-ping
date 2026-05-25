import asyncio
import logging

import flet as ft

from constants.dimensions import DIM_WIN_MIN_HEIGHT, DIM_WIN_MIN_WIDTH
from constants.fonts import FONT_FILES
from constants.info import APP_TITLE
from state.theme_state import ThemeState

logger = logging.getLogger(__name__)

__is_subscribed = False


def subscribe_events(theme_state: ThemeState) -> None:
	global __is_subscribed

	if __is_subscribed:
		return

	page = ft.context.page

	def update_theme():
		logger.info(
			"theme mode changed",
			extra={
				"theme-mode": theme_state.theme_mode,
				"theme-primary": theme_state.theme_primary,
				"theme-secondary": theme_state.theme_secondary,
			},
		)

		page.theme_mode = theme_state.theme_mode
		page.theme = page.dark_theme = theme_state.theme_primary

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

		_ = asyncio.create_task(theme_state.load_theme())

	page.on_resize = theme_state.on_resize
	ft.on_updated(
		update_theme,
		[
			theme_state.theme_mode,
			theme_state.theme_primary,
		],
	)
	ft.on_mounted(on_mounted)
	__is_subscribed = True
