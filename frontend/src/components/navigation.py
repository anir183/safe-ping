import logging
import flet as ft

from components.nav_drawer_button import NavDrawerButton
from components.user_menu import (
	UserMenuCompact,
	UserMenuExpanded,
	on_user_action,
)
from constants.breakpoints import Breakpoints
from constants.dimensions import Dimensions
from constants.images import ImageSizes
from constants.navigation import NAV_ITEMS
from constants.spacing import Spacing
from contexts.navigation import NavigationContext

logger = logging.getLogger(__name__)


@ft.component
def Navigation():
	nav = ft.use_context(NavigationContext)

	width, set_width = ft.use_state(ft.context.page.width or 0)
	expanded, set_expanded = ft.use_state(False)
	max_rail_items, set_max_rail_items = ft.use_state(10)

	is_large = width >= Breakpoints.LG

	def calc_rail_items_num() -> None:
		page = ft.context.page

		if not page.height:
			set_max_rail_items(5)
			return

		usable_height = page.height * 0.7
		available_for_items = usable_height - 150  # reserved footer + padding
		max_items = int(available_for_items // 45)
		set_max_rail_items(max_items)

	calc_rail_items_num()

	def on_resize(_):
		calc_rail_items_num()
		set_width(ft.context.page.width or 0)

	ft.context.page.on_resize = on_resize

	def rail_items():
		return NAV_ITEMS[:max_rail_items]

	def selected_index() -> int:
		for index, item in enumerate(rail_items()):
			if item["id"] == nav.selected:
				return index
		return 0

	def on_rail_change(e: ft.Event[ft.NavigationRail]):
		index = e.control.selected_index or 0
		items = rail_items()

		if index >= len(items):
			set_expanded(True)
			return

		if 0 <= index < len(items):
			nav.set_selected(items[index]["id"])

	def build_full_nav_items():
		items: list[ft.Control] = []

		for index, item in enumerate(NAV_ITEMS):
			if index == 1:
				items.append(ft.Divider())

			items.append(
				NavDrawerButton(
					label=item["label"],
					icon=item["icon"],
					selected=nav.selected == item["id"],
					on_click=lambda _, item_id=item["id"]: nav.set_selected(
						item_id
					),
				)
			)

		return items

	def sidebar(*, dismissible: bool) -> ft.Control:
		return ft.Container(
			width=Dimensions.SIDEBAR_WIDTH,
			padding=Spacing.MD,
			content=ft.Column(
				spacing=0,
				expand=True,
				controls=[
					*(
						[
							ft.IconButton(
								icon=ft.Icons.MENU_OPEN,
								tooltip="Close navigation",
								on_click=lambda _: set_expanded(False),
							)
						]
						if dismissible
						else []
					),
					ft.Container(
						expand=True,
						content=ft.ListView(
							spacing=Spacing.SM,
							expand=True,
							controls=build_full_nav_items(),
						),
					),
					ft.TextButton(
						width=float("inf"),
						icon=ft.Icons.ADD_CIRCLE,
						content="Add Room",
						tooltip="Add Room",
						on_click=new_room,
						style=ft.ButtonStyle(
							padding=ft.Padding.symmetric(
								horizontal=Spacing.MD,
								vertical=Spacing.LG,
							),
							alignment=ft.Alignment.CENTER_LEFT,
							shape=ft.RoundedRectangleBorder(radius=12),
						),
					),
					ft.Divider(),
					ft.Container(
						padding=Spacing.SM,
						content=UserMenuExpanded(on_user_action),
					),
				],
			),
		)

	def new_room():
		logger.info("new room")

	rail_destinations: list[ft.NavigationRailDestination] = []

	for item in rail_items():
		rail_destinations.append(
			ft.NavigationRailDestination(
				icon=item["icon_outlined"],
				selected_icon=item["icon"],
				tooltip=item["label"],
				label=item["label"],
			)
		)

	if len(NAV_ITEMS) > max_rail_items:
		rail_destinations.append(
			ft.NavigationRailDestination(
				icon=ft.Icons.MORE_VERT,
				selected_icon=ft.Icons.MORE_VERT,
				tooltip="More",
				label="More",
			)
		)

	if is_large:
		return ft.Row(
			controls=[
				sidebar(dismissible=False),
				ft.VerticalDivider(width=1),
			]
		)

	if expanded:
		return ft.Row(
			controls=[
				sidebar(dismissible=True),
				ft.VerticalDivider(width=1),
			]
		)

	return ft.Row(
		controls=[
			ft.Column(
				width=Dimensions.NAV_RAIL_WIDTH,
				expand=True,
				controls=[
					ft.NavigationRail(
						selected_index=selected_index(),
						label_type=ft.NavigationRailLabelType.NONE,
						on_change=on_rail_change,
						leading=ft.IconButton(
							icon=ft.Icons.MENU,
							tooltip="Open navigation",
							on_click=lambda _: set_expanded(True),
						),
						pin_trailing_to_bottom=True,
						trailing=ft.IconButton(
							icon=ft.Icons.ADD_CIRCLE,
							tooltip="Add Room",
							icon_size=ImageSizes.ICON_SM,
							on_click=new_room,
						),
						destinations=rail_destinations,
						expand=True,
					),
					ft.Container(
						padding=ft.Padding.symmetric(
							horizontal=Spacing.MD,
							vertical=Spacing.XXL,
						),
						alignment=ft.Alignment.CENTER,
						content=UserMenuCompact(on_user_action),
					),
				],
			),
			ft.VerticalDivider(width=1),
		]
	)
