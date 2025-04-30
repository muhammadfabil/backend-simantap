from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from sqlalchemy.orm import Session

from app.database.session import get_db
from app.middleware.websocket_manager import WebSocketManager
from app.middleware.jwt_handler import decode_access_token

from fastapi import HTTPException
from uuid import uuid4

router = APIRouter()
manager = WebSocketManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()

    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        role = payload.get("role")

        if not user_id or not role:
            await websocket.close(code=1008)
            return

        # Cek role
        if role == "mahasiswa":
            from app.services.mahasiswa_service import get_detail_mahasiswa

            mahasiswa = get_detail_mahasiswa(db, user_id)
            if not mahasiswa:
                await websocket.close(code=1008)
                return
            user_id = mahasiswa.nim

        elif role == "dosen":
            from app.services.dosen_service import get_detail_dosen

            dosen = get_detail_dosen(db, user_id)
            if not dosen:
                await websocket.close(code=1008)
                return
            user_id = dosen.alias  # Atau dosen.inisial sesuai field mu

        elif role == "admin":
            user_id = "adminSiMantap"

        else:
            # Role tidak dikenali
            await websocket.close(code=1008)
            return

    except HTTPException:
        await websocket.close(code=1008)
        return

    await manager.connect_user(user_id, websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect_user(user_id, websocket)
        print(f"❌ Disconnected user: {user_id}")

@router.websocket("/ws/public")
async def websocket_public(websocket: WebSocket):
    await websocket.accept()
    anon_id = str(uuid4())  # optional: give them a random ID
    await manager.connect_user(anon_id, websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect_user(anon_id, websocket)

# 👉 Testing endpoint: user connect manual pakai user_id
@router.websocket("/ws/test/{user_id}")
async def websocket_test_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()

    await manager.connect_user(user_id, websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect_user(user_id, websocket)
        print(f"❌ Disconnected (testing) user: {user_id}")