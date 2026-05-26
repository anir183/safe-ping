import asyncio
import json
import logging
from collections.abc import Callable
from typing import Any

import websockets

from constants.info import BACKEND_WS_URL

logger = logging.getLogger(__name__)


RECONNECT_DELAY = 3.0


class WsConnection:
	def __init__(self):
		self._ws = None
		self._listening = False
		self._task = None
		self._room_id: str | None = None
		self._user_id: str | None = None
		self._on_init: Callable[[list[dict]], None] | None = None
		self._on_message: Callable[[dict], None] | None = None

	async def connect(
		self,
		room_id: str,
		user_id: str,
		on_init: Callable[[list[dict]], None],
		on_message: Callable[[dict], None],
		auto_reconnect: bool = True,
	) -> bool:
		self._room_id = room_id
		self._user_id = user_id
		self._on_init = on_init
		self._on_message = on_message
		self._listening = True

		return await self._do_connect(auto_reconnect=auto_reconnect)

	async def _do_connect(self, auto_reconnect: bool = True) -> bool:
		try:
			assert self._room_id is not None
			assert self._user_id is not None
			self._ws = await websockets.connect(
				f"{BACKEND_WS_URL}/ws/{self._room_id}?user_id={self._user_id}"
			)

			async def listen():
				while self._listening and self._ws:
					try:
						raw = await self._ws.recv()
						data = json.loads(raw)
						msg_type = data.get("type")

						if msg_type == "init" and self._on_init:
							self._on_init(data.get("messages", []))
						elif msg_type == "message" and self._on_message:
							self._on_message(data)
					except websockets.ConnectionClosed:
						if self._listening and auto_reconnect:
							await self._reconnect()
						break
					except Exception as e:
						if self._listening:
							logger.error(
								"ws recv error",
								extra={"error": str(e)},
							)
						break

			self._task = asyncio.create_task(listen())
			logger.info(
				"ws connected",
				extra={"room": self._room_id},
			)
			return True

		except Exception as e:
			logger.warning(
				"ws connection failed",
				extra={"error": str(e)},
			)
			self._ws = None
			if auto_reconnect:
				_ = asyncio.create_task(self._reconnect())
			return False

	async def _reconnect(self) -> None:
		await asyncio.sleep(RECONNECT_DELAY)
		if not self._listening:
			return
		logger.info(
			"ws reconnecting",
			extra={"room": self._room_id},
		)
		_ = await self._do_connect(auto_reconnect=True)

	async def send(self, data: dict) -> None:
		if self._ws:
			try:
				await self._ws.send(json.dumps(data))
			except Exception as e:
				logger.error("ws send error", extra={"error": str(e)})

	async def disconnect(self) -> None:
		self._listening = False
		if self._task:
			self._task.cancel()
			self._task = None
		if self._ws:
			try:
				await self._ws.close()
			except Exception:
				pass
			self._ws = None

	@property
	def is_connected(self) -> bool:
		return self._ws is not None

	@property
	def room_id(self) -> str | None:
		return self._room_id
