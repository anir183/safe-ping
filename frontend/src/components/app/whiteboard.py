import asyncio

import flet as ft
import flet.canvas as cv

from components.primitives.empty import Empty
from constants.room import ROOM_SECTION_WHITEBOARD
from contexts.room import RoomContext
from models.whiteboard import WhiteboardStroke
from repos.mock.whiteboard import MockWhiteboardRepository


@ft.component
def WhiteboardPage():
	room_context = ft.use_context(RoomContext)

	repo, _ = ft.use_state(MockWhiteboardRepository())

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

	def load_strokes():
		async def _load():
			if room_context.room is None:
				return
			strokes = await repo.get_strokes(room_context.room.id)
			set_paths(
				[
					{
						"points": list(s.points),
						"color": s.color,
						"stroke": s.stroke_width,
					}
					for s in strokes
				]
			)

		_ = asyncio.create_task(_load())

	ft.use_effect(
		load_strokes,
		[room_context.room.id if room_context.room else None],
	)

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
			new_paths = paths + [
				{
					"points": list(current_path),
					"color": current_color,
					"stroke": current_stroke,
				}
			]
			set_paths(new_paths)
			_ = asyncio.create_task(
				_save_after_draw(new_paths, room_context.room.id)
			)

		set_current_path([])

	async def _save_after_draw(all_paths, room_id):
		strokes = [
			WhiteboardStroke(
				id=str(i),
				room_id=room_id,
				points=list(p["points"]),
				color=p["color"],
				stroke_width=p["stroke"],
			)
			for i, p in enumerate(all_paths)
		]
		await repo.save_strokes(room_id, strokes)

	def clear_board(_):
		set_paths([])
		if room_context.room is not None:
			_ = asyncio.create_task(
				repo.save_strokes(room_context.room.id, [])
			)

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
