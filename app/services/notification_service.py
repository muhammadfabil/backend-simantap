from sqlalchemy.orm import Session 

from app.database.models.subscription import PushSubscription
from app.schemas.push import PushNotificationPayload
from app.services.push_service import PushService

from datetime import datetime
from datetime import timedelta

from app.database.models.waktu_bimbingan import WaktuBimbingan
from app.database.models.antrian_bimbingan import AntrianBimbingan

push = PushService()

async def send_push_notification(
    db: Session,
    target_user_ids: list[str],
    push_payload: PushNotificationPayload
): 
    for user_id in target_user_ids:
        print(f"📪 Preparing WebPush for {user_id}")
        
        subscriptions = db.query(PushSubscription).filter(
            PushSubscription.user_id == user_id
        ).all()

        if subscriptions:
            push.send_bulk_notification(
                subscriptions,
                data={
                    "title": push_payload.title,
                    "body": push_payload.body,
                    "url": push_payload.url
                }
            )
        else:
            print(f"❗ No subscriptions found for {user_id}")


def send_upcoming_bimbingan_notifications(db: Session):
    now = datetime.now()
    thirty_minutes_later = now + timedelta(minutes=30)

    upcoming_sessions = db.query(WaktuBimbingan).filter(
        WaktuBimbingan.tanggal == now.date(),
        WaktuBimbingan.waktu_mulai.between(now.time(), thirty_minutes_later.time())
    ).all()

    for session in upcoming_sessions:
        for antrian in session.antrian_bimbingan:
            mahasiswa_nim = antrian.mahasiswa_nim

            subscription = db.query(PushSubscription).filter(
                PushSubscription.user_id == mahasiswa_nim
            ).first()

            if subscription:
                try:
                    push.send_notification(
                        subscription={
                            "endpoint": subscription.endpoint,
                            "keys": {
                                "p256dh": subscription.keys_p256dh,
                                "auth": subscription.keys_auth
                            }
                        },
                        data={
                            "title": "Pengingat Bimbingan",
                            "body": f"Bimbingan Anda akan dimulai pada {session.waktu_mulai.strftime('%H:%M')} di {session.lokasi}.",
                            "data": {
                                "bimbingan_id": session.bimbingan_id,
                                "tanggal": session.tanggal.isoformat(),
                                "waktu_mulai": session.waktu_mulai.strftime('%H:%M'),
                                "lokasi": session.lokasi
                            }
                        }
                    )
                except Exception as e:
                    print(f"Failed to send notification to {mahasiswa_nim}: {e}")