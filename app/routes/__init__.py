from app.routes.admin import router as admin_router
from app.routes.antrian_bimbingan import router as antrian_bimbingan_router
from app.routes.auth import router as auth_router
from app.routes.dosen import router as dosen_router
from app.routes.file import router as file_router
from app.routes.layanan import router as layanan_router
from app.routes.mahasiswa import router as mahasiswa_router
from app.routes.mahasiswa_dosen import router as mahasiswa_dosen_router
from app.routes.news import router as news_router
from app.routes.push_router import router as push_router
from app.routes.waktu_bimbingan import router as waktu_bimbingan_router
from app.routes.websocket_router import router as websocket_router


all_routers = [
    admin_router,
    antrian_bimbingan_router,
    auth_router,
    dosen_router,
    file_router,
    layanan_router,
    mahasiswa_router,
    mahasiswa_dosen_router,
    news_router,
    push_router,
    waktu_bimbingan_router,
    websocket_router
]