import logging
from dataclasses import dataclass, field

import flet as ft

from models.user import User

logger = logging.getLogger(__name__)


@ft.observable
@dataclass
class UserState:
	current_user: User | None = field(default=None)

	def set_user(self, user: User) -> None:
		self.current_user = user
		logger.info(
			"set current user",
			extra={"user_id": user.id, "user_name": user.name},
		)

	def clear_user(self) -> None:
		self.current_user = None
		logger.info("cleared current user")
