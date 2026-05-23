from enum import Enum


class RoomSection(str, Enum):
	CHAT = "chat"
	WHITEBOARD = "whiteboard"
	NOTES = "notes"
