from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.models.subscription import PushSubscription
from app.schemas.push import PushSubscriptionCreate
from app.schemas.push import PushNotificationPayload 
from app.middleware.jwt_handler import decode_access_token
from app.services.push_service import PushService

import uuid

router = APIRouter(prefix="/wp", tags=["WebPush"])
push_service = PushService()

@router.get("/vapid-public-key")
def get_public_key():
    return {"publicKey": push_service.get_public_key()}

@router.post("/push/subscribe")
def subscribe_push(
    subscription: PushSubscriptionCreate,
    db: Session = Depends(get_db),
    authorization: str = Header(...)
):
    try:
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid Authorization header")
        token = authorization.split(" ")[1]

        payload = decode_access_token(token)
        user_id = payload.get("sub")
        role = payload.get("role")

        if not user_id or not role:
            raise HTTPException(status_code=403, detail="Invalid token or role")

        if role == "mahasiswa":
            from app.services.mahasiswa_service import get_detail_mahasiswa
            mahasiswa = get_detail_mahasiswa(db, user_id)
            if not mahasiswa:
                raise HTTPException(status_code=404, detail="Mahasiswa not found")
            user_id = mahasiswa.nim  

        else:
            raise HTTPException(status_code=403, detail="Only mahasiswa can subscribe to push notifications")

        existing_subscription = db.query(PushSubscription).filter(
            PushSubscription.user_id == user_id
        ).first()

        if existing_subscription:
            existing_subscription.endpoint = subscription.endpoint
            existing_subscription.keys_p256dh = subscription.keys.p256dh
            existing_subscription.keys_auth = subscription.keys.auth
            db.commit()
            return {"message": "Subscription updated successfully"}

        new_subscription = PushSubscription(
            id=uuid.uuid4(),
            user_id=user_id,
            endpoint=subscription.endpoint,
            keys_p256dh=subscription.keys.p256dh,
            keys_auth=subscription.keys.auth
        )
        db.add(new_subscription)
        db.commit()

        return {"message": "Push subscription created successfully"}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid token or request")


@router.post("/push/send")
def push_test_message(
    payload: PushNotificationPayload,
    db: Session = Depends(get_db)
):
    subs = db.query(PushSubscription).all()    
    result = push_service.send_bulk_notification(
        subs,
        data=payload.model_dump()
    )

    return {"message": f"Sent {result['sent']} notifications, {result['failed']} failed"}