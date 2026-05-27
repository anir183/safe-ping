# SafePing

A secure workspace and chat application built with Python. The frontend uses Flet (a Flutter-based UI framework for Python) and the backend is a FastAPI WebSocket server.

## Architecture

### Frontend — Flet Python App (`frontend/`)

A reactive single-page application organized in layers:

- **State layer** — Three observable state classes (`UserState`, `ThemeState`, `RoomState`) drive the entire UI. Fields are decorated with `@ft.observable` so any change automatically propagates to dependent components.
- **Context layer** — Three Flet contexts (`UserContext`, `ThemeContext`, `RoomContext`) bridge state to the component tree. Components read context values via `ft.use_context()` and re-render when values change.
- **Pages** — `LoginPage` (select a user profile) gates entry to `AppPage` (the main workspace). Routing is purely context-based — the `Router` component checks `UserContext` to decide which page to render.
- **Workspace** — Once inside `AppPage`, a `RoomContext` drives the entire workspace. It tracks the active room, the open section (Chat / Whiteboard / Notes), and the full room list. Components like `ChatPage`, `WhiteboardPage`, and `NotesPage` each check `room_context.open_section` — if it doesn't match, they return an invisible `Empty()` control. This is how sections are toggled without URL-based routing.
- **Responsive layout** — The app adapts to four breakpoints (SM ≤700px, MD ≤1200px, LG ≤2000px, XL >2000px). `RoomPane` automatically switches between a compact nav rail, an expanded drawer, and a full three-panel layout (nav + content + info sidebar).
- **Repository pattern** — Abstract interfaces (`RoomsRepository`, `MessagesRepository`, `NotesRepository`, `WhiteboardRepository`, `UserRepository`) are backed by mock implementations. These are designed to be swapped for real API calls.
- **Services** — `WsConnection` manages WebSocket lifecycle (connect, reconnect, init-history, message events). `SharedPrefs` persists preferences via Flet's native key-value store.

### Backend — FastAPI Server (`backend/`)

A lightweight FastAPI server with a single WebSocket endpoint:

- `GET /` — Health check
- `WebSocket /ws/{room_id}?user_id=...` — Real-time messaging per room
- `ConnectionManager` — Tracks connected clients per room, stores message history in-memory, broadcasts messages to all peers (excluding the sender), and validates `sender_id` on each message.

## Security

- Messages are encrypted client-side before transmission using a PBKDF2-derived key with an HMAC-based stream cipher. The server receives already-encrypted payloads.
- The backend verifies that `sender_id` matches the authenticated `user_id` query parameter, rejecting mismatched messages.
- A shared passphrase (`safe-ping-demo-2026`) is used for the demo; in production this would be replaced with per-user key exchange.

## Features

- **Multi-room chat** — Real-time messaging with WebSocket transport and message history
- **Collaborative notes** — Per-room rich text notes with save/load
- **Whiteboard** — Freehand drawing with brush size and color controls, persists strokes per room
- **Dashboard** — Landing view when no room is selected
- **Theme system** — Light/dark mode with distinct color seeds (Lime for dark, Purple for light), persisted across sessions
- **Responsive design** — Adapts layout across desktop, tablet, and mobile viewports
- **User profiles** — Select from mock users to enter the workspace; each user has name, email, and avatar

## Project Structure

```
safe_ping/main/
├── docs/README.md             ← you are here
├── frontend/
│   ├── pyproject.toml
│   ├── src/
│   │   ├── main.py            # Entry point
│   │   ├── core/
│   │   │   ├── app.py         # App shell — wires states, contexts, window config
│   │   │   └── router.py      # Context-based router (Login vs App)
│   │   ├── state/             # Observable state dataclasses
│   │   │   ├── user_state.py
│   │   │   ├── theme_state.py
│   │   │   └── room_state.py
│   │   ├── contexts/          # Flet context definitions
│   │   │   ├── user.py
│   │   │   ├── theme.py
│   │   │   └── room.py
│   │   ├── pages/             # Login, App, NotFound
│   │   ├── components/        # UI components
│   │   │   ├── app/           # Room, chat, notes, whiteboard, dashboard, nav
│   │   │   ├── primitives/    # Avatar, logo, empty, theme_toggle, user_entry
│   │   │   ├── dialogs/       # Info dialog
│   │   │   ├── styles/        # ButtonStyle
│   │   │   └── util/          # ResponsiveComponent, PlatformComponent
│   │   ├── models/            # User, Room, Message, Note, WhiteboardStroke
│   │   ├── repos/             # Repository interfaces + mock implementations
│   │   ├── services/          # WebSocket client, SharedPreferences
│   │   ├── constants/         # Design tokens, routes, configuration
│   │   └── utils/             # Crypto, logging, paths, responsive, platform
│   └── docs/README.md         # Build and run instructions
└── backend/
    ├── pyproject.toml
    ├── main.py                # FastAPI WebSocket server
    └── docs/README.md         # Server run instructions
```

## Quick Start

### Prerequisites

- Python ≥3.10 (frontend), Python ≥3.14 (backend)
- [uv](https://docs.astral.sh/uv/) package manager

### Backend

```bash
cd backend
uv run fastapi dev
```

### Frontend

```bash
cd frontend
uv run flet run          # desktop
uv run flet run --web    # web browser
```

See `frontend/docs/README.md` and `backend/docs/README.md` for detailed build/run instructions.
