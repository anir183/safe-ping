import flet as ft

from constants.fonts import FONT_HEADER, FONT_LG
from constants.images import LOGO, LOGO_SM
from constants.info import APP_TITLE
from contexts.theme import ThemeContext


@ft.component
def Logo() -> ft.Control:
	theme = ft.use_context(ThemeContext)

	return ft.Row(
		[
			ft.Image(
				src=LOGO,
				width=LOGO_SM,
				color=theme.primary.color_scheme_seed,
			),
			ft.Text(
				APP_TITLE,
				font_family=FONT_HEADER,
				size=FONT_LG,
			),
		]
	)
