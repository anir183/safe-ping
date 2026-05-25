from dataclasses import dataclass


@dataclass
class User:
	id: int
	name: str
	email: str
	avatar_src: str
