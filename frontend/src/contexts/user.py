from collections.abc import Callable
from dataclasses import dataclass

import flet as ft

from models.user import User


def _noop_set(_: User) -> None:
	pass


@dataclass(frozen=True)
class UserContextValue:
	user: User | None
	set_user: Callable[[User], None]
	clear_user: Callable[[], None]


UserContext = ft.create_context(
	UserContextValue(
		user=None,
		set_user=_noop_set,
		clear_user=lambda: None,
	)
)
