import logging

import flet as ft

from core.app import App
from utils.paths import get_asset_dir
from utils.logging import setupLogging

setupLogging()


def main(page: ft.Page):
	page.render_views(App)


assets_dir = str(get_asset_dir())
logging.getLogger(__name__).info(
	"resolved assets dir",
	extra={"path": assets_dir},
)
_ = ft.run(main, assets_dir=assets_dir)
