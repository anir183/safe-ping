import asyncio
import logging

import flet as ft

from components.app_bar import AppBar
from constants.dimensions import Dimensions
from constants.phrases import Titles
from constants.typography import FONT_FILES
from contexts.route import RouteContext, RouteContextValue
from contexts.theme import ThemeContext, ThemeContextValue
from pages.home import HomePage
from state.app_state import AppModel

logger = logging.getLogger(__name__)


@ft.component
def App():
	app, _ = ft.use_state(AppModel(route=ft.context.page.route))

	# subscribe to page events as soon as possible
	ft.context.page.on_route_change = app.route_change
	ft.context.page.on_view_pop = app.view_popped

	# stable callbacks (don’t change identity each render)
	toggle_mode = ft.use_callback(
		lambda: app.toggle_theme(), dependencies=[app.theme_mode]
	)

	# memoize the provided value so its identity changes only when mode changes
	theme_context = ft.use_memo(
		lambda: ThemeContextValue(
			mode=app.theme_mode,
			seed_color=app.theme_color,
			toggle_mode=toggle_mode,
		),
		dependencies=[
			app.theme_mode,
			app.theme_color,
			toggle_mode,
		],
	)

	navigate_callback = ft.use_callback(
		lambda new_route: app.navigate(new_route), dependencies=[app.route]
	)

	route_context = ft.use_memo(
		lambda: RouteContextValue(
			route=app.route,
			navigate=navigate_callback,
		),
		dependencies=[app.route],
	)

	page = HomePage()

	def on_mounted():
		page = ft.context.page

		logger.info(
			"mounted page",
			extra={
				"width": page.width,
				"height": page.height,
			},
		)

		page.services.append(app.prefs)

		page.title = Titles.APP_TITLE
		page.fonts = FONT_FILES

		# remove title bar and buttons on desktop
		page.window.title_bar_hidden = True
		page.window.title_bar_buttons_hidden = True
		page.window.frameless = False

		# minimum window size and defaults for desktop
		page.window.resizable = True
		page.window.maximized = False
		page.window.min_width = Dimensions.WINDOW_MIN_WIDTH
		page.window.min_height = Dimensions.WINDOW_MIN_HEIGHT

		_ = asyncio.create_task(app.load_theme())

	ft.on_mounted(on_mounted)

	def update_theme():
		logger.info(
			"theme mode changed",
			extra={
				"theme-mode": app.theme_mode,
				"theme-color": app.theme_color,
			},
		)

		ft.context.page.theme_mode = app.theme_mode
		ft.context.page.theme = ft.context.page.dark_theme = ft.Theme(
			color_scheme_seed=app.theme_color
		)

	ft.on_updated(update_theme, [app.theme_mode, app.theme_color])

	return RouteContext(
		route_context,
		lambda: ThemeContext(
			theme_context,
			lambda: ft.View(
				route="/",
				controls=[AppBar(), ft.SafeArea(expand=True, content=page)],
			),
		),
	)
