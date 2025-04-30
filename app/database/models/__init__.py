from app.database.models.admin import Admin
from app.database.models.antrian_bimbingan import AntrianBimbingan
from app.database.models.dosen import Dosen
from app.database.models.file import Files
from app.database.models.layanan import Layanan
from app.database.models.mahasiswa import Mahasiswa
from app.database.models.mahasiswa_dosen import MahasiswaDosen
from app.database.models.news import News
from app.database.models.subscription import PushSubscription
from app.database.models.waktu_bimbingan import WaktuBimbingan

from app.database.session import Base
from app.database.session import engine

Base.metadata.create_all(bind=engine)