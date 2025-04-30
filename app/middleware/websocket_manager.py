# app/middleware/websocket_manager.py
from typing import Dict
from typing import List
from fastapi import WebSocket
import datetime

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    def _log(self, message: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    async def connect_user(self, user_id: str, websocket: WebSocket):
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        self._log(f"🟢 Connected user '{user_id}'. Total connections: {len(self.active_connections[user_id])}")

    def disconnect_user(self, user_id: str, websocket: WebSocket):
        if user_id in self.active_connections and websocket in self.active_connections[user_id]:
            self.active_connections[user_id].remove(websocket)
            self._log(f"🔴 Disconnected user '{user_id}'. Remaining: {len(self.active_connections[user_id])}")
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_message(self, user_id: str, message: str):
        connections = self.active_connections.get(user_id, [])
        for ws in connections.copy():
            try:
                await ws.send_text(message)
            except Exception as e:
                self._log(f"⚠️ Failed to send to {user_id}: {e}")
                connections.remove(ws)

    async def send_json(self, user_id: str, data: dict):
        connections = self.active_connections.get(user_id, [])
        for ws in connections.copy():
            try:
                await ws.send_json(data)
            except Exception as e:
                self._log(f"⚠️ Failed to send JSON to {user_id}: {e}")
                connections.remove(ws)

    async def broadcast(self, message: dict):
        print("📢 Broadcasting to:", sum(len(v) for v in self.active_connections.values()))
        for user_id, connections in self.active_connections.items():
            for ws in connections.copy():
                try:
                    await ws.send_json(message)
                except Exception as e:
                    self._log(f"❌ Failed to send to {user_id}: {e}")
                    connections.remove(ws)

    async def broadcast_all(self, message: dict):
        print("🌐 Broadcasting to all unique connections")
        unique_connections = set()

        for connections in self.active_connections.values():
            for ws in connections:
                unique_connections.add(ws)

        for ws in unique_connections:
            try:
                await ws.send_json(message)
            except Exception as e:
                self._log(f"❌ Failed to broadcast: {e}")
                unique_connections.remove(ws)

        self._log(f"✅ Broadcasted to {len(unique_connections)} unique connections")

manager = WebSocketManager()