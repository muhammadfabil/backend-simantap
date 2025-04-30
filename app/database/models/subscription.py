from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID

from uuid import uuid4

from app.database.session import Base

class PushSubscription(Base):
    __tablename__ = "push_subscription"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    user_id = Column(String, nullable=False)
    endpoint = Column(String, nullable=False)
    keys_p256dh = Column(String, nullable=False)
    keys_auth = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
