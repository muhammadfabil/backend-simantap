from fastapi import Depends
from pywebpush import webpush
from pywebpush import WebPushException
from sqlalchemy.orm import Session
from typing import List

from app.core.config import settings
from app.database.session import get_db
from app.database.models.subscription import PushSubscription

import json

class PushService:
    def __init__(self):
        self.vapid_private_key = settings.vapid_private_key
        self.vapid_public_key = settings.vapid_public_key
        self.vapid_claims = {
            "sub": "mailto:simantap.ifitera@gmail.com"
        }

    def get_public_key(self) -> str:
        return self.vapid_public_key

    def send_notification(self, subscription: dict, data: dict, db: Session = Depends(get_db)):
        try:
            webpush(
                subscription_info=subscription,
                data=json.dumps(data),
                vapid_private_key=self.vapid_private_key,
                vapid_claims=self.vapid_claims
            )
        except WebPushException as e:
            print(f"Web Push Failed: {e}")
            if db and subscription.endpoint and (e.response and e.response.status_code in (404, 410)):
                sub = db.query(PushSubscription).filter(PushSubscription.endpoint == subscription.endpoint).first()
                if sub:
                    db.delete(sub)
                    db.commit()
                    print(f"Deleted endpoint {subscription.endpoint} from database")
            raise e

    def send_bulk_notification(self, subcriptions: List[PushSubscription], data: dict) -> dict:
        sent = 0
        failed = 0
        for sub in subcriptions:
            try:
                self.send_notification({
                    "endpoint": sub.endpoint,
                    "keys": {
                        "p256dh": sub.keys_p256dh,
                        "auth": sub.keys_auth
                    }
                }, data)
                sent += 1
            except Exception as e:
                print(f"Failed to send to {sub['endpoint']}: {repr(e)}")
                failed += 1
        return {"sent": sent, "failed": failed}