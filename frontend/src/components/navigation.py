import flet as ft

from components.nav_drawer_button import NavDrawerButton
from components.user_menu import UserMenuCompact, UserMenuExpanded, on_user_action
from constants.breakpoints import Breakpoints
from constants.dimensions import Dimensions
from constants.navigation import NAV_ITEMS
from constants.spacing import Spacing
from contexts.navigation import NavigationContext


@ft.component
def Navigation():
	nav = ft.use_context(NavigationContext)

	width, set_width = ft.use_state(ft.context.page.width or 0)
	expanded, set_expanded = ft.use_state(False)

	is_large = width >= Breakpoints.LG

	def on_resize(_):
		set_width(ft.context.page.width or 0)

	ft.context.page.on_resize = on_resize

	def selected_index() -> int:
		for index, item in enumerate(NAV_ITEMS):
			if item["id"] == nav.selected:
				return index
		return 0

	def on_rail_change(e: ft.Event[ft.NavigationRail]):
		index = e.control.selected_index or 0

		if 0 <= index < len(NAV_ITEMS):
			nav.set_selected(NAV_ITEMS[index]["id"])

	def sidebar(*, dismissible: bool) -> ft.Control:
		controls: list[ft.Control] = []

		if dismissible:
			controls.append(
				ft.IconButton(
					icon=ft.Icons.MENU_OPEN,
					tooltip="Close navigation",
					on_click=lambda _: set_expanded(False),
				)
			)

		for index, item in enumerate(NAV_ITEMS):
			if index == 1:
				controls.append(ft.Divider())

			controls.append(
				NavDrawerButton(
					label=item["label"],
					icon=item["icon"],
					selected=nav.selected == item["id"],
					on_click=lambda _, item_id=item["id"]: nav.set_selected(item_id),
				)
			)

		return ft.Container(
			width=Dimensions.SIDEBAR_WIDTH,
			padding=Spacing.MD,
			content=ft.Column(
				controls=[
					ft.Column(
						controls=controls,
						spacing=Spacing.SM,
						expand=True,
					),
					ft.Divider(),

					# 👇 now delegated
					ft.Container(
						padding=Spacing.SM,
						content=UserMenuExpanded(on_user_action),
					),
				],
			),
		)

	rail_destinations: list[ft.NavigationRailDestination] = []

	for item in NAV_ITEMS:
		rail_destinations.append(
			ft.NavigationRailDestination(
				icon=item["icon_outlined"],
				selected_icon=item["icon"],
				tooltip=item["label"],
				label=item["label"],
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
