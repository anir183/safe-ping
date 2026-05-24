import flet as ft

from constants.dimensions import DIM_INF
from constants.fonts import FONT_HEADER, FONT_XXL
from constants.routes import ROUTE_ROOT
from constants.spacing import SPACE_LG


@ft.component
def NotFound() -> ft.Control:
	return ft.Column(
		width=DIM_INF,
		expand=True,
		alignment=ft.MainAxisAlignment.CENTER,
		horizontal_alignment=ft.CrossAxisAlignment.CENTER,
		spacing=SPACE_LG,
		controls=[
			ft.Text(
				"404 Invalid Page",
				size=FONT_XXL,
				font_family=FONT_HEADER,
			),
			ft.Button(
				"Home",
				on_click=lambda: ft.context.page.navigate(ROUTE_ROOT),
			),
		],
	)
