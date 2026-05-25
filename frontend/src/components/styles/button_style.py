import flet as ft

from constants.spacing import SPACE_LG, SPACE_MD
from constants.styles import STYLE_RADIUS_MD


class ButtonStyle(ft.ButtonStyle):
	padding: ft.ControlStateValue[ft.PaddingValue] | None
	alignment: ft.Alignment | None
	shape: ft.ControlStateValue[ft.OutlinedBorder] | None
	bgcolor: ft.ControlStateValue[ft.ColorValue] | None

	def __init__(
		self, bgcolor: ft.ControlStateValue[ft.ColorValue] | None = None
	):
		super().__init__()

		self.padding = ft.Padding.symmetric(
			horizontal=SPACE_MD,
			vertical=SPACE_LG,
		)
		self.alignment = ft.Alignment.CENTER_LEFT
		self.shape = ft.RoundedRectangleBorder(
			radius=STYLE_RADIUS_MD,
		)

		if bgcolor is not None:
			self.bgcolor = bgcolor
