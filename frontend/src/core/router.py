import logging

import flet as ft

from contexts.user import UserContext
from pages.app import AppPage
from pages.login import LoginPage

logger = logging.getLogger(__name__)


@ft.component
def Router() -> ft.Control:
	user_context = ft.use_context(UserContext)

	if user_context.user is not None:
		return AppPage()

	return LoginPage()
