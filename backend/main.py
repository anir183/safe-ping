import json
import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query

logger = logging.getLogger(__name__)


class ConnectionManager:
	def __init__(self):
		self.rooms: dict[str, set[WebSocket]] = {}
		self.messages: dict[str, list[dict]] = {}
		self.user_map: dict[WebSocket, str] = {}

	async def connect(
		self, websocket: WebSocket, room_id: str, user_id: str
	) -> None:
		await websocket.accept()
		self.rooms.setdefault(room_id, set()).add(websocket)
		self.user_map[websocket] = user_id

		history = self.messages.get(room_id, [])
		await websocket.send_text(
			json.dumps({"type": "init", "messages": history})
		)

		logger.info(
			"ws client connected",
			extra={
				"room": room_id,
				"user_id": user_id,
				"history_count": len(history),
			},
		)

	def disconnect(self, websocket: WebSocket, room_id: str) -> None:
		self.rooms.get(room_id, set()).discard(websocket)
		self.user_map.pop(websocket, None)
		logger.info("ws client disconnected", extra={"room": room_id})

	async def broadcast(
		self,
		room_id: str,
		message_data: dict,
		exclude: WebSocket | None = None,
	) -> None:
		self.messages.setdefault(room_id, []).append(message_data)
		text = json.dumps({"type": "message", **message_data})

		for ws in list(self.rooms.get(room_id, set())):
			if ws != exclude:
				try:
					await ws.send_text(text)
				except Exception:
					pass


manager = ConnectionManager()

app = FastAPI()


@app.get("/")
async def read_root():
	return {"status": "ok"}


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(
	websocket: WebSocket,
	room_id: str,
	user_id: str = Query(...),
):
	await manager.connect(websocket, room_id, user_id)
	try:
		while True:
			data = await websocket.receive_text()
			parsed = json.loads(data)

			if parsed.get("type") == "message":
				if parsed.get("sender_id") != user_id:
					logger.warning(
						"rejected message: sender_id mismatch",
						extra={
							"expected": user_id,
							"got": parsed.get("sender_id"),
						},
					)
					continue

				await manager.broadcast(
					room_id,
					{
						"id": parsed["id"],
						"sender_id": parsed["sender_id"],
						"sender_name": parsed["sender_name"],
						"content": parsed["content"],
						"timestamp": parsed["timestamp"],
					},
					exclude=websocket,
				)
	except WebSocketDisconnect:
		manager.disconnect(websocket, room_id)
	except Exception as e:
		logger.error("ws error", extra={"error": str(e)})
		manager.disconnect(websocket, room_id)
