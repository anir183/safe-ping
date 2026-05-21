import flet as ft

from app import App
from utils.logger import setup_logging

setup_logging()


def main(page: ft.Page):
	page.render_views(App)


_ = ft.run(main)
