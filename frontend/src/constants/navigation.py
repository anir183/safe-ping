from enum import StrEnum
from typing import TypedDict

import flet as ft


class NavID(StrEnum):
	DASH = "dash"
	CHAT_1 = "chat1"
	CHAT_2 = "chat2"
	CHAT_3 = "chat3"


class NavItem(TypedDict):
	id: NavID
	label: str
	icon: ft.IconData
	icon_outlined: ft.IconData


NAV_ITEMS: list[NavItem] = [
	{
		"id": NavID.DASH,
		"label": "Dashboard",
		"icon": ft.Icons.HOME,
		"icon_outlined": ft.Icons.HOME_OUTLINED,
	},
	{
		"id": NavID.CHAT_1,
		"label": "Chat 1",
		"icon": ft.Icons.CHAT,
		"icon_outlined": ft.Icons.CHAT_OUTLINED,
	},
	{
		"id": NavID.CHAT_2,
		"label": "Chat 2",
		"icon": ft.Icons.CHAT,
		"icon_outlined": ft.Icons.CHAT_OUTLINED,
	},
	{
		"id": NavID.CHAT_3,
		"label": "Chat 3",
		"icon": ft.Icons.CHAT,
		"icon_outlined": ft.Icons.CHAT_OUTLINED,
	},
]
