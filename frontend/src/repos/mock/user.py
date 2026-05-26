from typing import override

from models.user import User
from repos.user import UserRepository


class MockUserRepository(UserRepository):
	@override
	async def get_users(self) -> list[User]:
		return [
			User("1", "Alice", "alice@test.com", "https://picsum.photos/101"),
			User("2", "Bob", "bob@test.com", "https://picsum.photos/102"),
			User("3", "Max", "max@test.com", "https://picsum.photos/103"),
			User("4", "Tom", "tom@test.com", "https://picsum.photos/104"),
			User("5", "Elise", "elise@test.com", "https://picsum.photos/105"),
		]
