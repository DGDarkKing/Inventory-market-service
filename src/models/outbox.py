from typing import Any

from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column

from database import ModelBaseUuid, DateTimeNow


class OutboxOrm(ModelBaseUuid):
    __tablename__ = 'outbox'
    __table_args__ = (Index('outbox_main_index', "created_at", "is_processed"),)

    data: Mapped[dict[str, Any]]

    is_processed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[DateTimeNow]
