"""
WebhookSession — lie un chat_id (Telegram/WhatsApp) à une affaire ARCEUS.
Persiste l'affaire active par canal, pour que les messages soient contextualisés.
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class WebhookSession(Base):
    __tablename__ = "webhook_sessions"
    __table_args__ = (UniqueConstraint("platform", "chat_id", name="uq_webhook_session"),)

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    platform: Mapped[str] = mapped_column(String(20), nullable=False, default="telegram")
    chat_id: Mapped[str] = mapped_column(String(128), nullable=False)

    # Affaire active sur ce canal (None = pas encore définie)
    affaire_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("affaires.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Utilisateur ARCEUS lié à ce canal (optionnel)
    user_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
