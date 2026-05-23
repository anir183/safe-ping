import flet as ft

from constants.breakpoints import Breakpoints
from contexts.room import RoomContext


@ft.component
def RoughRoomShell():
	room = ft.use_context(RoomContext)

	width = ft.context.page.width or 0

	is_large = width >= Breakpoints.LG
	is_medium = width >= Breakpoints.MD and width < Breakpoints.LG
	# is_small = width < Breakpoints.MD

	def _chat_view():
		return ft.Container(content=ft.Text("Chat view"))


	def _whiteboard_view():
		return ft.Container(content=ft.Text("Whiteboard view"))


	def _notes_view():
		return ft.Container(content=ft.Text("Notes view"))

	def _build_mobile_view() -> ft.Control:
		section = room.active_section

		if section == "chat":
			return _chat_view()

		if section == "whiteboard":
			return _whiteboard_view()

		if section == "notes":
			return _notes_view()

		return ft.Container(content=ft.Text("Mobile root"))

	def _mobile_layout() -> ft.Control:
		return ft.Column(
			expand=True,
			controls=[
				_build_mobile_view(),
			],
		)

	def _tablet_layout() -> ft.Control:
		return ft.Row(
			expand=True,
			controls=[
				ft.Container(
					width=72,
					content=ft.Column(
						controls=[
							ft.Icon(ft.Icons.CHAT),
							ft.Icon(ft.Icons.DRAW),
							ft.Icon(ft.Icons.NOTE),
						],
					),
				),
				ft.VerticalDivider(width=1),
				_build_main_panel(),
			],
		)

	def _build_right_panel() -> ft.Control:
		return ft.Container(
			width=240,
			content=ft.Column(
				controls=[
					ft.Text("Members"),
					# later: room.members
				],
			),
		)

	def _build_main_panel() -> ft.Control:
		if room.active_section == "chat":
			return _chat_view()

		if room.active_section == "whiteboard":
			return _whiteboard_view()

		if room.active_section == "notes":
			return _notes_view()

		return ft.Container(content=ft.Text("Select something"))

	def _build_left_panel() -> ft.Control:
		return ft.Container(
			width=280,
			content=ft.Column(
				controls=[
					ft.Text("Chats"),
					ft.Text("Whiteboards"),
					ft.Text("Notes"),
				],
			),
		)

	def _desktop_layout() -> ft.Control:
		return ft.Row(
			expand=True,
			controls=[
				_build_left_panel(),
				ft.VerticalDivider(width=1),
				_build_main_panel(),
				ft.VerticalDivider(width=1),
				_build_right_panel(),
			],
		)

	def _build_layout() -> ft.Control:
		if is_large:
			return _desktop_layout()

		if is_medium:
			return _tablet_layout()

		return _mobile_layout()

	return ft.Row(
		expand=True,
		controls=[_build_layout()],
	)
