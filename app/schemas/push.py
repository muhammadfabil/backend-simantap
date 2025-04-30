from pydantic import BaseModel
from typing import Optional

class PushSubscriptionKeys(BaseModel):
    p256dh: str
    auth: str

class PushSubscriptionCreate(BaseModel):
    # user_id: str
    endpoint: str
    keys: PushSubscriptionKeys

class PushNotificationPayload(BaseModel):
    title: str
    body: str
    url: Optional[str] = None