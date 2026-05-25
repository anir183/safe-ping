import asyncio
from typing import override

from models.user import User
from repos.user import UserRepository


class MockUserRepository(UserRepository):
	@override
	async def get_users(self) -> list[User]:
		await asyncio.sleep(1)

		return [
			User("1", "Alice", "alice@test.com", "https://i.pravatar.cc/100"),
			User("2", "Bob", "bob@test.com", "https://i.pravatar.cc/100"),
			User("3", "Max", "max@test.com", "https://i.pravatar.cc/100"),
			User("4", "Tom", "tom@test.com", "https://i.pravatar.cc/100"),
			User("5", "Elise", "elise@test.com", "https://i.pravatar.cc/100"),
		]
