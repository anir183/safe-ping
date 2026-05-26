import asyncio
import json
import sys
import time

import websockets

WS_URL = "ws://localhost:8000/ws/room_e2e"


async def client(name: str, received: list):
	ws = await websockets.connect(WS_URL)
	init = json.loads(await ws.recv())
	print(f"[{name}] init: {init.get('type')}, history={len(init.get('messages', []))}")

	async def listen():
		async for raw in ws:
			data = json.loads(raw)
			received.append(data)
			print(f"[{name}] recv: {data.get('type')} — {data.get('content', '')}")

	async def send(msg: dict):
		await ws.send(json.dumps(msg))
		print(f"[{name}] send: {msg.get('content', '')}")

	listen_task = asyncio.create_task(listen())
	return ws, send, listen_task


async def main():
	c1_msgs = []
	c2_msgs = []

	c1_ws, c1_send, c1_listen = await client("alice", c1_msgs)
	c2_ws, c2_send, c2_listen = await client("bob", c2_msgs)

	await asyncio.sleep(0.2)

	await c1_send({
		"type": "message",
		"id": "1",
		"sender_id": "alice_id",
		"sender_name": "Alice",
		"content": "Hello from Alice!",
		"timestamp": "12:00",
	})

	await asyncio.sleep(0.2)

	await c2_send({
		"type": "message",
		"id": "2",
		"sender_id": "bob_id",
		"sender_name": "Bob",
		"content": "Hey Alice!",
		"timestamp": "12:01",
	})

	await asyncio.sleep(0.3)

	c1_ws_close = c1_ws.close()
	c2_ws_close = c2_ws.close()
	c1_listen.cancel()
	c2_listen.cancel()
	await asyncio.gather(c1_ws_close, c2_ws_close, return_exceptions=True)

	print("\n=== RESULTS ===")
	print(f"Alice received {len(c1_msgs)} messages: {[m.get('content') for m in c1_msgs]}")
	print(f"Bob received   {len(c2_msgs)} messages: {[m.get('content') for m in c2_msgs]}")

	assert len(c1_msgs) == 1, f"Alice should have 1 msg, got {len(c1_msgs)}"
	assert len(c2_msgs) == 1, f"Bob should have 1 msg, got {len(c2_msgs)}"
	assert c1_msgs[0]["content"] == "Hey Alice!", f"Alice got wrong msg: {c1_msgs[0]}"
	assert c2_msgs[0]["content"] == "Hello from Alice!", f"Bob got wrong msg: {c2_msgs[0]}"

	print("\n=== ALL ASSERTIONS PASSED ===")


if __name__ == "__main__":
	asyncio.run(main())
