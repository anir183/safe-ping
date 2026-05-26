import asyncio
import logging

import flet as ft

from components.app_bar import MobileAppBar
from components.app_header import AppHeader
from constants.dimensions import DIM_WIN_MIN_HEIGHT, DIM_WIN_MIN_WIDTH
from constants.fonts import FONT_FILES
from constants.info import APP_TITLE
from constants.routes import ROUTE_ROOT
from contexts.theme import ThemeContext, ThemeContextValue
from contexts.user import UserContext, UserContextValue
from core.router import Router
from state.theme_state import ThemeState
from state.user_state import UserState

logger = logging.getLogger(__name__)


@ft.component
def App() -> ft.Control:
	theme_state, _ = ft.use_state(ThemeState(route=ft.context.page.route))
	user_state, _ = ft.use_state(UserState())

	page = ft.context.page

	def _on_mounted():
		logger.info(
			"mounted page",
			extra={
				"width": page.width,
				"height": page.height,
			},
		)

		page.on_resize = theme_state.on_resize
		page.title = APP_TITLE
		page.fonts = FONT_FILES

		page.window.title_bar_hidden = True
		page.window.title_bar_buttons_hidden = True
		page.window.frameless = False

		page.window.resizable = True
		page.window.maximized = False
		page.window.min_width = DIM_WIN_MIN_WIDTH
		page.window.min_height = DIM_WIN_MIN_HEIGHT

		_ = asyncio.create_task(theme_state.load_theme())

	ft.on_mounted(_on_mounted)

	def _update_theme():
		logger.info(
			"theme mode changed",
			extra={
				"theme-mode": theme_state.theme_mode,
				"theme-primary": theme_state.theme_primary.color_scheme_seed,
				"theme-secondary": theme_state.theme_secondary.color_scheme_seed,
			},
		)

		page.theme_mode = theme_state.theme_mode
		page.theme = page.dark_theme = theme_state.theme_primary

	ft.on_updated(
		_update_theme,
		[
			theme_state.theme_mode,
			theme_state.theme_primary,
		],
	)

	toggle_mode = ft.use_callback(
		lambda: theme_state.toggle_theme(),
		dependencies=[
			theme_state.theme_mode,
		],
	)

	theme_context = ft.use_memo(
		lambda: ThemeContextValue(
			mode=theme_state.theme_mode,
			primary=theme_state.theme_primary,
			secondary=theme_state.theme_secondary,
			toggle_mode=toggle_mode,
		),
		dependencies=[
			theme_state.theme_mode,
			theme_state.theme_primary,
			theme_state.theme_secondary,
			toggle_mode,
		],
	)

	set_user = ft.use_callback(
		lambda user: user_state.set_user(user),
		dependencies=[user_state.current_user],
	)

	clear_user = ft.use_callback(
		lambda: user_state.clear_user(),
		dependencies=[user_state.current_user],
	)

	user_context = ft.use_memo(
		lambda: UserContextValue(
			user=user_state.current_user,
			set_user=set_user,
			clear_user=clear_user,
		),
		dependencies=[
			user_state.current_user,
			set_user,
			clear_user,
		],
	)

	app_view = UserContext(
		value=user_context,
		callback=lambda: ThemeContext(
			value=theme_context,
			callback=lambda: ft.View(
				route=ROUTE_ROOT,
				appbar=MobileAppBar(),
				controls=[
					AppHeader(),
					ft.SafeArea(
						expand=True,
						content=Router(),
					),
				],
			),
		),
	)

	return app_view
