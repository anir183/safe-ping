import flet as ft

from core.app import App


def main(page: ft.Page):
	page.render_views(App)


_ = ft.run(
	main,
	assets_dir=str(Path(__file__).resolve().parents[1] / "assets"),
)
