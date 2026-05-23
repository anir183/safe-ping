from pathlib import Path

import flet as ft

from core.app import App
from utils.logging import setupLogging


def main(page: ft.Page):
	page.render_views(App)


setupLogging()
_ = ft.run(
	main,
	assets_dir=str(Path(__file__).resolve().parents[1] / "assets"),
)
