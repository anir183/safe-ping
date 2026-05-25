# import flet as ft
#
# from components.primitives.empty import Empty
# from constants.room import ROOM_SECTION_WHITEBOARD
# from contexts.room import RoomContext
#
#
# @ft.component
# def WhiteboardPage():
# 	room_context = ft.use_context(RoomContext)
#
# 	if (
# 		room_context.room is None
# 		or room_context.open_section != ROOM_SECTION_WHITEBOARD
# 	):
# 		return Empty()
#
# 	return ft.Container(
# 		expand=True,
# 		content=ft.Column(
# 			expand=True,
# 			alignment=ft.MainAxisAlignment.CENTER,
# 			horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# 			controls=[
# 				ft.Text(
# 					room_context.room and room_context.room.name,
# 					align=ft.Alignment.CENTER,
# 				),
# 				ft.Text(
# 					room_context.open_section,
# 					align=ft.Alignment.CENTER,
# 				),
# 			],
# 		),
# 	)

import flet as ft
import flet.canvas as cv

from components.primitives.empty import Empty
from constants.room import ROOM_SECTION_WHITEBOARD
from contexts.room import RoomContext


@ft.component
def WhiteboardPage():
	room_context = ft.use_context(RoomContext)

	if (
		room_context.room is None
		or room_context.open_section != ROOM_SECTION_WHITEBOARD
	):
		return Empty()

	paths, set_paths = ft.use_state([])
	current_path, set_current_path = ft.use_state([])
	current_color, set_current_color = ft.use_state(ft.Colors.BLACK)
	current_stroke, set_current_stroke = ft.use_state(3)

	canvas_ref = ft.Ref[ft.GestureDetector]()

	def start_draw(e: ft.DragStartEvent):
		set_current_path(
			[
				(e.local_position.x, e.local_position.y),
			]
		)

	def update_draw(e: ft.DragUpdateEvent):
		set_current_path(
			current_path
			+ [
				(e.local_position.x, e.local_position.y),
			]
		)

	def end_draw(_):
		if len(current_path) > 1:
			set_paths(
				paths
				+ [
					{
						"points": current_path,
						"color": current_color,
						"stroke": current_stroke,
					}
				]
			)

		set_current_path([])

	def clear_board(_):
		set_paths([])

	def build_lines():
		lines = []

		for path in paths:
			points = path["points"]

			for i in range(len(points) - 1):
				x1, y1 = points[i]
				x2, y2 = points[i + 1]

				lines.append(
					cv.Line(
						x1,
						y1,
						x2,
						y2,
						ft.Paint(
							stroke_width=path["stroke"],
							color=path["color"],
							style=ft.PaintingStyle.STROKE,
							stroke_cap=ft.StrokeCap.ROUND,
						),
					)
				)

		if len(current_path) > 1:
			for i in range(len(current_path) - 1):
				x1, y1 = current_path[i]
				x2, y2 = current_path[i + 1]

				lines.append(
					cv.Line(
						x1,
						y1,
						x2,
						y2,
						ft.Paint(
							stroke_width=current_stroke,
							color=current_color,
							style=ft.PaintingStyle.STROKE,
							stroke_cap=ft.StrokeCap.ROUND,
						),
					)
				)

		return lines

	return ft.Column(
		expand=True,
		spacing=0,
		controls=[
			ft.Container(
				padding=10,
				bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
				content=ft.Row(
					wrap=True,
					alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
					controls=[
						ft.Row(
							controls=[
								ft.IconButton(
									icon=ft.Icons.DELETE,
									tooltip="Clear",
									on_click=clear_board,
								),
								ft.VerticalDivider(),
								ft.Text("Brush"),
								ft.Slider(
									min=1,
									max=20,
									value=current_stroke,
									width=150,
									on_change=lambda e: set_current_stroke(
										int(e.control.value)
									),
								),
							],
						),
						ft.Row(
							controls=[
								ft.IconButton(
									icon=ft.Icons.CIRCLE,
									icon_color=ft.Colors.BLACK,
									on_click=lambda _: set_current_color(
										ft.Colors.BLACK
									),
								),
								ft.IconButton(
									icon=ft.Icons.CIRCLE,
									icon_color=ft.Colors.RED,
									on_click=lambda _: set_current_color(
										ft.Colors.RED
									),
								),
								ft.IconButton(
									icon=ft.Icons.CIRCLE,
									icon_color=ft.Colors.BLUE,
									on_click=lambda _: set_current_color(
										ft.Colors.BLUE
									),
								),
								ft.IconButton(
									icon=ft.Icons.CIRCLE,
									icon_color=ft.Colors.GREEN,
									on_click=lambda _: set_current_color(
										ft.Colors.GREEN
									),
								),
							],
						),
					],
				),
			),
			ft.GestureDetector(
				ref=canvas_ref,
				expand=True,
				drag_interval=1,
				on_pan_start=start_draw,
				on_pan_update=update_draw,
				on_pan_end=end_draw,
				content=ft.Container(
					expand=True,
					bgcolor=ft.Colors.WHITE,
					content=cv.Canvas(
						expand=True,
						shapes=build_lines(),
					),
				),
			),
		],
	)
