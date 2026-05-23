import flet as ft
from constants.images import ImageSizes
from constants.spacing import Spacing
from constants.typography import FontSize

def UserAvatar(radius=ImageSizes.AVATAR_SM, src="https://i.pravatar.cc/100"):
	return ft.CircleAvatar(
		radius=radius,
		foreground_image_src=src,
		content=ft.Icon(ft.Icons.PERSON)
	)

def on_user_action(e: ft.Event[ft.PopupMenuButton]):
	action = e.control.data

	if action == "settings":
		print("settings clicked")
	elif action == "logout":
		print("logout clicked")


def UserMenuCompact(on_select: ft.ControlEventHandler[ft.PopupMenuButton]):
	return ft.PopupMenuButton(
		content=UserAvatar(),
		items=[
			ft.PopupMenuItem(content="Settings", data="settings"),
			ft.PopupMenuItem(content="Logout", data="logout"),
		],
		on_select=on_select,
	)

def UserMenuExpanded(on_select: ft.ControlEventHandler[ft.PopupMenuButton]):
	return ft.PopupMenuButton(
		content=ft.Container(
			padding=ft.Padding.symmetric(horizontal=Spacing.SM, vertical=Spacing.XS),
			content=ft.Row(
				controls=[
					UserAvatar(),
					ft.Column(
						spacing=0,
						controls=[
							ft.Text(
								"anir183",
								size=FontSize.MD,
								weight=ft.FontWeight.W_500,
							),
							ft.Text("online", size=FontSize.SM, opacity=0.7),
						],
					),
				],
			),
		),
		items=[
			ft.PopupMenuItem(content="Settings", data="settings"),
			ft.PopupMenuItem(content="Logout", data="logout"),
		],
		on_select=on_select,
	)
